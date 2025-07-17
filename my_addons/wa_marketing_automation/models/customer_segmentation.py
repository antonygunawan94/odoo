import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class CustomerSegmentation(models.Model):
    _name = "wa_marketing_automation.customer_segmentation"
    _description = "Customer Segmentation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_names_search = ["name", "description"]

    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Text(string="Description")
    type = fields.Selection(
        [("manual", "Manually"), ("rules", "Rule Based")],
        string="How we segment our customers?",
        default="manual",
        tracking=True,
    )
    selected_customers = fields.Many2many(
        "res.partner",
        string="Selected Customers",
        tracking=True,
    )
    rules = fields.Char(
        string="Rules",
        default="['&', '|' , ('phone', '!=', False), ('mobile', '!=', False), ('name', 'ilike', '')]",
        tracking=True,
    )

    @api.constrains("type", "rules")
    def _check_rules(self):
        for record in self:
            _logger.info(f"check rules dipanggil {record.type}")

            if record.type != "rules":
                return

            try:
                evaluated_rules = safe_eval(record.rules)
            except Exception as e:
                raise ValidationError(
                    _("Customer segmentation rules contain invalid syntax: %s") % str(e)
                )

            has_phone_mobile = self._check_phone_mobile_in_domain(evaluated_rules)
            _logger.info(f"has_phone_mobile: {has_phone_mobile}")
            if not has_phone_mobile:
                raise ValidationError(
                    _(
                        f"Customer segmentation '{record.name}' rules do not ensure customers have contact information. "
                        "Please include conditions that require customers to have phone or mobile fields set "
                        "(e.g., phone != False or mobile != False) to ensure WhatsApp messages can be sent."
                    )
                )

            try:
                # Try to safely evaluate the rules to check if they're valid
                safe_eval(record.rules)
            except Exception as e:
                raise ValidationError(
                    _("Customer segmentation rules contain invalid syntax: %s") % str(e)
                )

    def _check_phone_mobile_in_domain(self, domain):
        """
        Check if domain ensures customers have at least one contact method (phone OR mobile).

        This ensures we only send WhatsApp campaigns to customers who have contact info.
        """
        if not isinstance(domain, list):
            return False

        return self._has_phone_mobile_filter(domain)

    def _has_phone_mobile_filter(self, domain):
        """
        Recursively check if domain has conditions that ensure customers have
        phone or mobile contact information set (not empty/false).
        """
        if not isinstance(domain, list):
            return False

        # Check each item in the domain
        for item in domain:
            # Check if item is a domain clause (tuple with field, operator, value)
            if isinstance(item, (tuple, list)) and len(item) == 3:
                field_name, operator, value = item
                _logger.info(f"Checking clause: {field_name} {operator} {value}")

                # Check if this clause ensures customer has phone/mobile contact info
                if field_name in ["phone", "mobile"] and self._is_non_empty_filter(
                    operator, value
                ):
                    _logger.info(
                        f"Found contact info requirement: {field_name} {operator} {value}"
                    )
                    return True

            # Check if item is a nested domain (list of domain clauses)
            elif isinstance(item, list):
                if self._has_phone_mobile_filter(item):
                    return True
            # Skip logical operators (strings like '&', '|', '!')
            elif isinstance(item, str):
                _logger.info(f"Processing logical operator: {item}")
                continue
        return False

    def _is_non_empty_filter(self, operator, value):
        """
        Check if the operator and value combination ensures the field is not empty/null
        This means the condition will include customers who HAVE this contact info set
        """
        # Conditions that ensure field is not empty/null (i.e., customer HAS contact info)
        non_empty_conditions = [
            (operator == "!=" and value in [False, "", None]),  # field != False/empty
            (
                operator == "not in"
                and isinstance(value, list)
                and any(v in [False, "", None] for v in value)
            ),  # field not in [False, empty, None]
            (operator == ">" and value == ""),  # field > empty string
            (
                operator == ">=" and value and value != ""
            ),  # field >= something non-empty
            (
                operator == "=" and value and value not in [False, "", None]
            ),  # field = something non-empty
            (
                operator == "in"
                and isinstance(value, list)
                and all(v not in [False, "", None] for v in value)
            ),  # field in [non-empty values]
            (operator == "like" and value and value != ""),  # field like something
            (operator == "ilike" and value and value != ""),  # field ilike something
        ]

        _logger.info(
            f"Checking if {operator} {value} ensures non-empty field: {any(non_empty_conditions)}"
        )
        return any(non_empty_conditions)

    @api.ondelete(at_uninstall=False)
    def _check_used_in_campaigns(self):
        for rec in self:
            campaigns = self.env["wa_marketing_automation.campaign"].search(
                [
                    ("customer_segmentation_id", "=", rec.id),
                ]
            )
            if campaigns:
                campaign_names: list[str] = []
                for campaign in campaigns:
                    campaign_names.append(campaign.name)

                campaign_names_str: str = "\n".join(campaign_names)
                raise UserError(
                    _(
                        "You cannot delete this customer segmentation because it is used in the following campaigns:\n%s"
                        % campaign_names_str
                    )
                )
