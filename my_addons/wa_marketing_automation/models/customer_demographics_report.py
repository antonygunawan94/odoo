# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class CustomerDemographicsReport(models.Model):
    _name = "wa_marketing_automation.customer_demographics_report"
    _description = "Customer Demographics Analysis Report"
    _auto = False
    _order = "age_group, last_purchase_date DESC"

    # Customer Info
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    name = fields.Char(string='Customer Name', readonly=True)
    
    # Age Demographics
    age = fields.Integer(string='Age', readonly=True)
    age_group = fields.Selection([
        ('18-25', '18-25 years'),
        ('26-35', '26-35 years'),
        ('36-50', '36-50 years'),
        ('51-65', '51-65 years'),
        ('65+', '65+ years'),
        ('unknown', 'Unknown Age')
    ], string='Age Group', readonly=True)
    
    date_of_birth = fields.Date(string='Date of Birth', readonly=True)
    
    # Geographic Info
    country_id = fields.Many2one('res.country', string='Country', readonly=True)
    state_id = fields.Many2one('res.country.state', string='State', readonly=True)
    city = fields.Char(string='City', readonly=True)
    
    # Purchase Behavior - RFM Analysis
    last_purchase_date = fields.Datetime(string='Last Purchase Date', readonly=True)
    days_since_last_purchase = fields.Integer(string='Days Since Last Purchase', readonly=True)
    total_orders = fields.Integer(string='Total Orders', readonly=True)
    total_spent = fields.Float(string='Total Spent', readonly=True)
    average_order_value = fields.Float(string='Average Order Value', readonly=True)
    
    # Recency Segmentation
    recency_segment = fields.Selection([
        ('active', 'Active (0-30 days)'),
        ('recent', 'Recent (31-90 days)'),
        ('dormant', 'Dormant (91-365 days)'),
        ('lost', 'Lost (365+ days)'),
        ('new', 'New Customer (No orders)')
    ], string='Recency Segment', readonly=True)
    
    # Frequency Segmentation
    frequency_segment = fields.Selection([
        ('high', 'High Frequency (10+ orders)'),
        ('medium', 'Medium Frequency (5-9 orders)'),
        ('low', 'Low Frequency (2-4 orders)'),
        ('one_time', 'One-time (1 order)'),
        ('none', 'No orders')
    ], string='Frequency Segment', readonly=True)
    
    # Monetary Segmentation
    monetary_segment = fields.Selection([
        ('high_value', 'High Value (Top 20%)'),
        ('medium_value', 'Medium Value (Middle 60%)'),
        ('low_value', 'Low Value (Bottom 20%)'),
        ('no_value', 'No Value')
    ], string='Monetary Segment', readonly=True)
    
    # Customer Scoring
    customer_score = fields.Float(string='Customer Score', readonly=True, help="RFM Score (1-10)")
    
    # Marketing Insights
    whatsapp_campaigns_sent = fields.Integer(string='WhatsApp Campaigns Sent', readonly=True)
    whatsapp_campaigns_opened = fields.Integer(string='WhatsApp Campaigns Opened', readonly=True)
    whatsapp_engagement_rate = fields.Float(string='WhatsApp Engagement Rate (%)', readonly=True)
    
    # Company
    company_id = fields.Many2one('res.company', string='Company', readonly=True)

    def init(self):
        """Create the view for customer demographics analysis"""
        tools.drop_view_if_exists(self._cr, self._table)
        
        self._cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY rp.id) as id,
                    
                    -- Customer Info
                    rp.id as partner_id,
                    rp.name as name,
                    
                    -- Age Demographics
                    CASE 
                        WHEN rp.date_of_birth IS NOT NULL THEN
                            EXTRACT(YEAR FROM AGE(CURRENT_DATE, rp.date_of_birth))
                        ELSE NULL
                    END as age,
                    
                    CASE 
                        WHEN rp.date_of_birth IS NULL THEN 'unknown'
                        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, rp.date_of_birth)) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, rp.date_of_birth)) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, rp.date_of_birth)) BETWEEN 36 AND 50 THEN '36-50'
                        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, rp.date_of_birth)) BETWEEN 51 AND 65 THEN '51-65'
                        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, rp.date_of_birth)) > 65 THEN '65+'
                        ELSE 'unknown'
                    END as age_group,
                    
                    rp.date_of_birth as date_of_birth,
                    
                    -- Geographic Info
                    rp.country_id as country_id,
                    rp.state_id as state_id,
                    rp.city as city,
                    
                    -- Purchase Behavior
                    sales_data.last_purchase_date,
                    CASE 
                        WHEN sales_data.last_purchase_date IS NOT NULL THEN
                            EXTRACT(DAYS FROM (CURRENT_TIMESTAMP - sales_data.last_purchase_date))
                        ELSE NULL
                    END as days_since_last_purchase,
                    
                    COALESCE(sales_data.total_orders, 0) as total_orders,
                    COALESCE(sales_data.total_spent, 0) as total_spent,
                    CASE 
                        WHEN COALESCE(sales_data.total_orders, 0) > 0 THEN
                            COALESCE(sales_data.total_spent, 0) / sales_data.total_orders
                        ELSE 0
                    END as average_order_value,
                    
                    -- Recency Segmentation
                    CASE 
                        WHEN sales_data.last_purchase_date IS NULL THEN 'new'
                        WHEN EXTRACT(DAYS FROM (CURRENT_TIMESTAMP - sales_data.last_purchase_date)) <= 30 THEN 'active'
                        WHEN EXTRACT(DAYS FROM (CURRENT_TIMESTAMP - sales_data.last_purchase_date)) <= 90 THEN 'recent'
                        WHEN EXTRACT(DAYS FROM (CURRENT_TIMESTAMP - sales_data.last_purchase_date)) <= 365 THEN 'dormant'
                        ELSE 'lost'
                    END as recency_segment,
                    
                    -- Frequency Segmentation
                    CASE 
                        WHEN COALESCE(sales_data.total_orders, 0) >= 10 THEN 'high'
                        WHEN COALESCE(sales_data.total_orders, 0) >= 5 THEN 'medium'
                        WHEN COALESCE(sales_data.total_orders, 0) >= 2 THEN 'low'
                        WHEN COALESCE(sales_data.total_orders, 0) = 1 THEN 'one_time'
                        ELSE 'none'
                    END as frequency_segment,
                    
                    -- Monetary Segmentation (will be computed via percentiles)
                    CASE 
                        WHEN COALESCE(sales_data.total_spent, 0) = 0 THEN 'no_value'
                        WHEN COALESCE(sales_data.total_spent, 0) >= (
                            SELECT PERCENTILE_CONT(0.8) WITHIN GROUP (ORDER BY total_spent) 
                            FROM (
                                SELECT partner_id, SUM(price_subtotal) as total_spent
                                FROM sale_order_line sol
                                JOIN sale_order so ON sol.order_id = so.id
                                WHERE so.state IN ('sale', 'done')
                                GROUP BY partner_id
                            ) spent_data
                        ) THEN 'high_value'
                        WHEN COALESCE(sales_data.total_spent, 0) >= (
                            SELECT PERCENTILE_CONT(0.2) WITHIN GROUP (ORDER BY total_spent) 
                            FROM (
                                SELECT partner_id, SUM(price_subtotal) as total_spent
                                FROM sale_order_line sol
                                JOIN sale_order so ON sol.order_id = so.id
                                WHERE so.state IN ('sale', 'done')
                                GROUP BY partner_id
                            ) spent_data
                        ) THEN 'medium_value'
                        ELSE 'low_value'
                    END as monetary_segment,
                    
                    -- Customer Score (RFM Score calculation)
                    CASE 
                        WHEN sales_data.last_purchase_date IS NULL THEN 1
                        ELSE (
                            -- Recency Score (1-3)
                            CASE 
                                WHEN EXTRACT(DAYS FROM (CURRENT_TIMESTAMP - sales_data.last_purchase_date)) <= 30 THEN 3
                                WHEN EXTRACT(DAYS FROM (CURRENT_TIMESTAMP - sales_data.last_purchase_date)) <= 90 THEN 2
                                ELSE 1
                            END +
                            -- Frequency Score (1-3)
                            CASE 
                                WHEN COALESCE(sales_data.total_orders, 0) >= 10 THEN 3
                                WHEN COALESCE(sales_data.total_orders, 0) >= 5 THEN 2
                                WHEN COALESCE(sales_data.total_orders, 0) >= 1 THEN 1
                                ELSE 0
                            END +
                            -- Monetary Score (1-4)
                            CASE 
                                WHEN COALESCE(sales_data.total_spent, 0) >= 1000 THEN 4
                                WHEN COALESCE(sales_data.total_spent, 0) >= 500 THEN 3
                                WHEN COALESCE(sales_data.total_spent, 0) >= 100 THEN 2
                                WHEN COALESCE(sales_data.total_spent, 0) > 0 THEN 1
                                ELSE 0
                            END
                        )
                    END as customer_score,
                    
                    -- Marketing Insights (temporarily set to 0 - will add back later)
                    0 as whatsapp_campaigns_sent,
                    0 as whatsapp_campaigns_opened,
                    0 as whatsapp_engagement_rate,
                    
                    -- Company
                    rp.company_id as company_id
                    
                FROM res_partner rp
                
                -- Sales Data Aggregation
                LEFT JOIN (
                    SELECT 
                        so.partner_id,
                        MAX(so.date_order) as last_purchase_date,
                        COUNT(so.id) as total_orders,
                        SUM(sol.price_subtotal) as total_spent
                    FROM sale_order so
                    JOIN sale_order_line sol ON so.id = sol.order_id
                    WHERE so.state IN ('sale', 'done')
                    GROUP BY so.partner_id
                ) sales_data ON rp.id = sales_data.partner_id
                
                -- TODO: WhatsApp Marketing Data (temporarily disabled due to Many2many relationship complexity)
                -- Need to properly handle the selected_customers Many2many field from customer_segmentation
                -- Will add back after basic report is working
                -- LEFT JOIN (
                --     SELECT 
                --         cs_partner.res_partner_id as partner_id,
                --         COUNT(DISTINCT wc.id) as campaigns_sent,
                --         COUNT(DISTINCT CASE WHEN wal.success = true THEN wc.id END) as campaigns_opened
                --     FROM wa_marketing_automation_customer_segmentation cs
                --     JOIN wa_marketing_automation_customer_segmentation_res_partner_rel cs_partner 
                --         ON cs.id = cs_partner.wa_marketing_automation_customer_segmentation_id
                --     JOIN wa_marketing_automation_campaign wc ON cs.id = wc.customer_segmentation_id
                --     LEFT JOIN wa_marketing_automation_whatsapp_api_log wal ON wc.id = wal.campaign_id
                --     WHERE wc.state = 'sent'
                --     GROUP BY cs_partner.res_partner_id
                -- ) wa_data ON rp.id = wa_data.partner_id
                
                WHERE rp.is_company = false
                AND rp.active = true
                -- AND rp.customer_rank > 0  -- Temporarily relaxed to show all contacts
            )
        """)
        
        _logger.info("Customer Demographics Report view created successfully")

    @api.model
    def get_age_distribution(self):
        """Get age distribution data for dashboard"""
        self.flush_model()
        query = """
            SELECT 
                age_group,
                COUNT(*) as customer_count,
                SUM(total_spent) as total_revenue,
                AVG(total_spent) as avg_spent_per_customer,
                AVG(customer_score) as avg_customer_score
            FROM wa_marketing_automation_customer_demographics_report
            WHERE age_group != 'unknown'
            GROUP BY age_group
            ORDER BY 
                CASE age_group
                    WHEN '18-25' THEN 1
                    WHEN '26-35' THEN 2
                    WHEN '36-50' THEN 3
                    WHEN '51-65' THEN 4
                    WHEN '65+' THEN 5
                    ELSE 6
                END
        """
        
        self._cr.execute(query)
        return self._cr.dictfetchall()

    @api.model
    def get_rfm_analysis(self):
        """Get RFM analysis data"""
        self.flush_model()
        query = """
            SELECT 
                recency_segment,
                frequency_segment,
                monetary_segment,
                COUNT(*) as customer_count,
                SUM(total_spent) as total_revenue,
                AVG(customer_score) as avg_score
            FROM wa_marketing_automation_customer_demographics_report
            GROUP BY recency_segment, frequency_segment, monetary_segment
            ORDER BY avg_score DESC
        """
        
        self._cr.execute(query)
        return self._cr.dictfetchall()

    @api.model
    def get_churn_risk_customers(self):
        """Get customers at risk of churn"""
        self.flush_model()
        query = """
            SELECT 
                partner_id,
                name,
                age_group,
                days_since_last_purchase,
                total_orders,
                total_spent,
                customer_score
            FROM wa_marketing_automation_customer_demographics_report
            WHERE recency_segment IN ('dormant', 'lost')
            AND frequency_segment IN ('high', 'medium')
            AND monetary_segment IN ('high_value', 'medium_value')
            ORDER BY customer_score DESC, days_since_last_purchase DESC
            LIMIT 100
        """
        
        self._cr.execute(query)
        return self._cr.dictfetchall()

    def action_view_partner(self):
        """Open the partner record"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'current',
        }