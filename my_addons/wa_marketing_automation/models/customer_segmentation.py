from odoo import api, fields, models


class CustomerSegmentation(models.Model):
    _name = "wa_marketing_automation.customer_segmentation"
    _description = "Customer Segmentation"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    segments = fields.Char(string="Segments", widget="domain")
