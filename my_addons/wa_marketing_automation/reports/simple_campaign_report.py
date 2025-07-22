from odoo import api, fields, models, tools

class SimpleCampaignReport(models.Model):
    """Simple campaign report for demonstration purposes"""
    _name = 'wa_marketing_automation.simple_campaign_report'
    _description = 'Simple Campaign Report'
    _auto = False  # Don't create table, we'll use SQL view
    _rec_name = 'campaign_name'
    _order = 'date desc'

    # Report fields
    campaign_id = fields.Many2one('wa_marketing_automation.campaign', string='Campaign', readonly=True)
    campaign_name = fields.Char(string='Campaign Name', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')
    ], string='Status', readonly=True)
    
    campaign_type = fields.Selection([
        ('time_based', 'Time Based'),
        ('forever', 'Forever')
    ], string='Campaign Type', readonly=True)
    
    # Simple metrics
    messages_sent = fields.Integer(string='Messages Sent', readonly=True)
    messages_failed = fields.Integer(string='Messages Failed', readonly=True)
    
    @api.model
    def init(self):
        """Create or replace the SQL view"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () AS id,
                    c.id AS campaign_id,
                    c.name AS campaign_name,
                    COALESCE(c.end_date::date, current_date) AS date,
                    c.state AS state,
                    c.type AS campaign_type,
                    
                    -- Simple message metrics
                    COALESCE((
                        SELECT COUNT(*) 
                        FROM wa_marketing_automation_whatsapp_api_log 
                        WHERE campaign_id = c.id AND status = 'success'
                    ), 0) AS messages_sent,
                    
                    COALESCE((
                        SELECT COUNT(*) 
                        FROM wa_marketing_automation_whatsapp_api_log 
                        WHERE campaign_id = c.id AND status = 'error'
                    ), 0) AS messages_failed
                    
                FROM wa_marketing_automation_campaign c
                WHERE c.state != 'draft'
            )
        """ % self._table)