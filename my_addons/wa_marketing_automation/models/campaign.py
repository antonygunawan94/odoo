from odoo import api, fields, models


class Campaign(models.Model):
    _name = "wa_marketing_automation.campaign"
    _description = "Campaign"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
