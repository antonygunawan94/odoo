# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class CustomerDemographicsReport(models.Model):
    _name = "wa_marketing_automation.customer_demographics_report"
    _description = "Customer Demographics Analysis Report"
    _auto = False
    _order = "customer_age_group_display, last_purchase_date DESC"

    # Customer Info
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    name = fields.Char(string='Customer Name', readonly=True)
    
    # Age Demographics
    age = fields.Integer(string='Age', readonly=True)
    
    # Dynamic Age Groups (using configurable age groups)
    customer_age_group = fields.Char(string='Customer Age Group', readonly=True)
    customer_age_group_display = fields.Char(string='Age Group Details', readonly=True)
    
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
    
    # Customer Spending Tier (dynamic from configuration)
    customer_spending_tier = fields.Char(string='Customer Spending Tier', readonly=True)
    customer_spending_tier_name = fields.Char(string='Spending Tier Name', readonly=True)
    
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
                    
                    
                    rp.date_of_birth as date_of_birth,
                    
                    -- Dynamic Age Groups (using configurable age groups)
                    rp.customer_age_group as customer_age_group,
                    rp.customer_age_group_display as customer_age_group_display,
                    
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
                    
                    -- Recency Segmentation (based on corrected RFM recency_score)
                    CASE 
                        WHEN rp.customer_rank = 0 THEN 'new'  -- No purchases
                        WHEN COALESCE(rp.recency_score, 1) >= 4 THEN 'active'    -- Score 4-5
                        WHEN COALESCE(rp.recency_score, 1) = 3 THEN 'recent'     -- Score 3
                        WHEN COALESCE(rp.recency_score, 1) = 2 THEN 'dormant'    -- Score 2
                        ELSE 'lost'  -- Score 1
                    END as recency_segment,
                    
                    -- Frequency Segmentation (based on corrected RFM frequency_score)
                    CASE 
                        WHEN COALESCE(rp.frequency_score, 0) >= 4 THEN 'high'      -- Score 4-5
                        WHEN COALESCE(rp.frequency_score, 0) = 3 THEN 'medium'     -- Score 3
                        WHEN COALESCE(rp.frequency_score, 0) = 2 THEN 'low'        -- Score 2
                        WHEN COALESCE(rp.frequency_score, 0) = 1 THEN 'one_time'   -- Score 1
                        ELSE 'none'  -- Score 0
                    END as frequency_segment,
                    
                    -- Customer Spending Tier (dynamic from configuration)
                    COALESCE(rp.customer_spending_tier, 'UNCLASSIFIED') as customer_spending_tier,
                    -- Dynamic tier names from configuration table
                    COALESCE(
                        (SELECT stc.display_name 
                         FROM wa_marketing_automation_customer_spending_tier_config stc 
                         WHERE stc.tier_code = rp.customer_spending_tier AND stc.active = true),
                        'Unclassified'
                    ) as customer_spending_tier_name,
                    
                    -- Customer Score (use corrected RFM score directly)
                    COALESCE(rp.rfm_score, 0) as customer_score,
                    
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
                
                WHERE rp.is_company = false
                AND rp.active = true
            )
        """)
        
        _logger.info("Customer Demographics Report view created successfully")

    @api.model
    def get_age_distribution(self):
        """Get age distribution data for dashboard - use dynamic age groups"""
        # This method is deprecated - use get_customer_age_group_distribution instead
        return self.get_customer_age_group_distribution()

    @api.model
    def get_spending_tier_distribution(self):
        """Get spending tier distribution data for dashboard"""
        self.flush_model()
        query = """
            SELECT 
                customer_spending_tier,
                customer_spending_tier_name,
                COUNT(*) as customer_count,
                SUM(total_spent) as total_revenue,
                AVG(total_spent) as avg_spent_per_customer,
                AVG(customer_score) as avg_customer_score,
                MIN(total_spent) as min_spending,
                MAX(total_spent) as max_spending
            FROM wa_marketing_automation_customer_demographics_report
            WHERE customer_spending_tier != 'UNCLASSIFIED'
            GROUP BY customer_spending_tier, customer_spending_tier_name
            ORDER BY avg_spent_per_customer DESC
        """
        
        self._cr.execute(query)
        return self._cr.dictfetchall()

    @api.model
    def get_customer_age_group_distribution(self):
        """Get customer age group distribution using configurable age groups"""
        self.flush_model()
        query = """
            SELECT 
                customer_age_group,
                customer_age_group_display,
                COUNT(*) as customer_count,
                SUM(total_spent) as total_revenue,
                AVG(total_spent) as avg_spent_per_customer,
                AVG(customer_score) as avg_customer_score,
                AVG(age) as avg_age,
                MIN(age) as min_age,
                MAX(age) as max_age,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage_of_total
            FROM wa_marketing_automation_customer_demographics_report
            WHERE customer_age_group != 'UNCLASSIFIED' AND customer_age_group IS NOT NULL
            GROUP BY customer_age_group, customer_age_group_display
            ORDER BY avg_age ASC
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
                customer_spending_tier,
                customer_spending_tier_name,
                COUNT(*) as customer_count,
                SUM(total_spent) as total_revenue,
                AVG(customer_score) as avg_score
            FROM wa_marketing_automation_customer_demographics_report
            GROUP BY recency_segment, frequency_segment, customer_spending_tier, customer_spending_tier_name
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
                customer_age_group_display,
                days_since_last_purchase,
                total_orders,
                total_spent,
                customer_score,
                customer_spending_tier,
                customer_spending_tier_name
            FROM wa_marketing_automation_customer_demographics_report
            WHERE recency_segment IN ('dormant', 'lost')
            AND frequency_segment IN ('high', 'medium')
            AND customer_spending_tier NOT IN ('UNCLASSIFIED', 'entry', 'basic')  -- Exclude entry/basic tiers
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