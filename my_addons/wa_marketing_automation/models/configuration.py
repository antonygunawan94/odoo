import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from ..utils import show_notification


class Configuration(models.Model):
    _name = "wa_marketing_automation.configuration"
    _description = "Configuration"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name",
        default="WhatsApp Configuration",
        required=True,
    )
    base_url = fields.Char(
        string="WhatsApp Base API URL",
        required=True,
        tracking=True,
    )
    access_token = fields.Char(string="Access Token", tracking=True)
    send_path_url = fields.Char(
        string="Send Message URL Path",
        default="/send-message",
        required=True,
        tracking=True,
    )
    health_check_path_url = fields.Char(
        string="Health Check URL Path",
        default="/health",
        required=True,
        tracking=True,
    )
    test_customer_id = fields.Many2one(
        "res.partner",
        string="Test Customer",
        help="This is the customer that will be used to test the message template.",
        required=True,
        tracking=True,
    )

    @api.model
    def get_config(self):
        """Get the singleton configuration record"""
        config = self.search([], limit=1)
        if not config:
            config = self._create_default_config()
        return config

    @api.model
    def _create_default_config(self):
        """Create default configuration if none exists"""
        return self.create(
            {
                "name": "WhatsApp Configuration",
                "base_url": "http://localhost:8000",
                "send_path_url": "/send-message",
                "health_check_path_url": "/health",
            }
        )

    @api.model
    def action_open_configuration(self):
        """Action to open the configuration (always opens existing or creates one)"""
        config = self.get_config()
        return {
            "type": "ir.actions.act_window",
            "name": "Configuration",
            "res_model": "wa_marketing_automation.configuration",
            "res_id": config.id,
            "view_mode": "form",
            "target": "current",
            "context": {"create": False, "edit": True},
        }

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to ensure only one record exists"""
        # Check if a record already exists
        existing = self.search([], limit=1)
        if existing:
            raise UserError(
                _(
                    "Only one WhatsApp configuration is allowed. "
                    "Please edit the existing configuration instead."
                )
            )

        # Ensure we only create one record even if multiple vals are passed
        if len(vals_list) > 1:
            raise UserError(_("Cannot create multiple WhatsApp configurations."))

        return super().create(vals_list)

    def unlink(self):
        """Override unlink to prevent deletion of the configuration"""
        raise UserError(_("WhatsApp configuration cannot be deleted."))

    def write(self, vals):
        """Override write to add validation"""
        # Prevent changing the name if you want to keep it fixed
        if "name" in vals and vals["name"] != "WhatsApp Configuration":
            vals["name"] = "WhatsApp Configuration"
        return super().write(vals)

    @api.model
    def default_get(self, fields_list):
        """Override default_get to return the singleton record if it exists"""
        res = super().default_get(fields_list)

        # If we're creating a new record but one already exists, redirect to edit
        existing = self.search([], limit=1)
        if existing and self._context.get("default_id") != existing.id:
            # Return the existing record's values
            for field in fields_list:
                if hasattr(existing, field):
                    res[field] = existing[field]

        return res

    def action_test_connection(self):
        """Test the WhatsApp API connection"""
        self.ensure_one()

        try:
            response = requests.get(
                f"{self.base_url}{self.health_check_path_url}", timeout=10
            )
            response.raise_for_status()
            return show_notification(
                title=_("Success"),
                message=_("Connection to WhatsApp API successful!"),
                type="success",
            )
        except requests.exceptions.SSLError:
            return show_notification(
                title=_("SSL Certificate Error"),
                message=_(
                    "There's an issue with the SSL certificate. "
                    "This could mean:\n"
                    "• The API server's SSL certificate is invalid or expired\n"
                    "• Your system's certificate store needs updating\n"
                    "• Try using 'http://' instead of 'https://' for testing"
                ),
                type="danger",
            )
        except requests.exceptions.Timeout:
            return show_notification(
                title=_("Connection Timeout"),
                message=_(
                    "The WhatsApp API server is taking too long to respond. "
                    "This might indicate:\n"
                    "• Server overload or slow response\n"
                    "• Network connectivity issues\n"
                    "• Try again in a few moments"
                ),
                type="warning",
            )
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                error_msg = _(
                    "The WhatsApp API endpoint was not found (404). "
                    "Please check:\n"
                    "• The health check URL path is correct\n"
                    "• The API server supports this endpoint"
                )
            elif status_code == 401:
                error_msg = _(
                    "Authentication failed (401). "
                    "Please check your access token configuration."
                )
            elif status_code == 403:
                error_msg = _(
                    "Access forbidden (403). "
                    "Your access token may not have the required permissions."
                )
            elif status_code >= 500:
                error_msg = (
                    _(
                        "The WhatsApp API server is experiencing issues (Error %s). "
                        "Please try again later or contact your API provider."
                    )
                    % status_code
                )
            else:
                error_msg = (
                    _(
                        "The WhatsApp API returned an error (HTTP %s). "
                        "Please check your configuration and try again."
                    )
                    % status_code
                )

            return show_notification(
                title=_("API Error"),
                message=error_msg,
                type="danger",
            )
        except requests.exceptions.InvalidURL:
            return show_notification(
                title=_("Invalid URL"),
                message=_(
                    "The API URL format is invalid. "
                    "Please check:\n"
                    "• The URL starts with http:// or https://\n"
                    "• No spaces or special characters in the URL\n"
                    "• The URL format is correct"
                ),
                type="danger",
            )
        except requests.exceptions.ConnectionError:
            return show_notification(
                title=_("Connection Failed"),
                message=_(
                    "Unable to connect to the WhatsApp API server. "
                    "Please check:\n"
                    "• Your internet connection\n"
                    "• The API server URL is correct\n"
                    "• The WhatsApp API server is running"
                ),
                type="danger",
            )
        except Exception as e:
            return show_notification(
                title=_("Unexpected Error"),
                message=_(
                    "An unexpected error occurred while testing the connection. "
                    "Technical details: %s\n\n"
                    "Please contact your system administrator if this problem persists."
                )
                % str(e),
                type="danger",
            )

    @api.constrains("base_url")
    def _check_api_base_url(self):
        """Validate API base URL format"""
        for record in self:
            if record.base_url and not record.base_url.startswith(
                ("http://", "https://")
            ):
                raise ValidationError(
                    _("API Base URL must start with http:// or https://")
                )
