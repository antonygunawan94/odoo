from odoo import fields, models


class WhatsappApiLog(models.Model):
    _name = "wa_marketing_automation.whatsapp_api_log"
    _description = "Whatsapp API Log"
    _rec_name = "message"
    _order = "at desc"

    message = fields.Text(string="Message", required=True)
    status = fields.Selection(
        [("success", "Success"), ("error", "Error")],
        string="Status",
        required=True,
    )
    at = fields.Datetime(string="At", required=True, default=fields.Datetime.now)
    campaign_id = fields.Many2one(
        "wa_marketing_automation.campaign",
        string="Campaign",
        help="Campaign that triggered this API call",
    )
    recipients_count = fields.Integer(
        string="Recipients Count", help="Number of recipients in this API call"
    )
    execution_type = fields.Selection(
        [
            ("manual", "Manual Execution"),
            ("initial", "Initial Message Sending"),
            ("scheduled", "Recurring Message Sending"),
            ("test", "Test Execution"),
        ],
        string="Execution Type",
        default="manual",
    )
