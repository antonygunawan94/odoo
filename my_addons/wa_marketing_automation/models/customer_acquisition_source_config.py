# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CustomerAcquisitionSourceConfig(models.Model):
    _name = "wa_marketing_automation.customer_acquisition_source_config"
    _description = "Customer Acquisition Source Configuration"
    _order = "sequence, name"
    _rec_name = "display_name"

    # Core fields
    name = fields.Char(
        string="Source Name",
        required=True,
        help="Internal name for this acquisition source",
    )
    display_name = fields.Char(
        string="Display Name",
        required=True,
        help="Customer-friendly name shown in reports and analytics",
    )
    code = fields.Char(
        string="Source Code",
        required=True,
        help="Unique code to identify this source (e.g., social_media, direct)",
    )
    description = fields.Text(
        string="Description", help="Detailed description of this acquisition source"
    )

    # Configuration fields
    sequence = fields.Integer(
        string="Sequence", default=10, help="Order in which sources appear in lists"
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Deactivate to hide this source without deleting",
    )
    is_digital = fields.Boolean(
        string="Is Digital Channel",
        default=False,
        help="Check if this is a digital/online acquisition channel",
    )
    is_social = fields.Boolean(
        string="Is Social Media",
        default=False,
        help="Check if this is a social media platform",
    )

    # Analytics fields
    icon = fields.Char(
        string="Icon", help="Font Awesome icon class (e.g., fa-instagram, fa-store)"
    )
    color = fields.Integer(
        string="Color Index",
        default=1,
        help="Color for visual representation in reports",
    )

    # Tracking fields
    customer_count = fields.Integer(
        string="Customer Count",
        compute="_compute_customer_count",
        store=True,
        help="Number of customers from this source",
    )

    @api.depends("active")
    def _compute_customer_count(self):
        """Compute number of customers for each acquisition source"""
        for source in self:
            source.customer_count = self.env["res.partner"].search_count(
                [
                    ("acquisition_source_id", "=", source.id),
                    ("customer_rank", ">", 0),
                    ("is_company", "=", False),
                ]
            )

    @api.constrains("code")
    def _check_unique_code(self):
        """Ensure code is unique across all sources"""
        for record in self:
            if (
                self.search_count([("code", "=", record.code), ("id", "!=", record.id)])
                > 0
            ):
                raise ValidationError(
                    f"Source code '{record.code}' already exists. Please use a unique code."
                )

    @api.model
    def get_source_by_code(self, code):
        """Helper method to get source by code"""
        return self.search([("code", "=", code)], limit=1)

    def name_get(self):
        """Override to show display name"""
        result = []
        for record in self:
            result.append((record.id, record.display_name or record.name))
        return result
