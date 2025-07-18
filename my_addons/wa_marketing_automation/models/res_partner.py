from odoo import fields, models, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    date_of_birth = fields.Date(
        string='Date of Birth',
        help='Date of birth of the contact',
        tracking=True,
    )
    
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
        help='Age in years, computed from date of birth',
    )
    
    age_display = fields.Char(
        string='Age Display',
        compute='_compute_age_display',
        store=True,
        help='Age display in human readable format',
    )

    # RFM Analysis Fields
    days_since_last_purchase = fields.Integer(
        string='Days Since Last Purchase',
        compute='_compute_rfm_data',
        store=True,
        help='Number of days since the last purchase',
    )
    
    purchase_count = fields.Integer(
        string='Purchase Count',
        compute='_compute_rfm_data',
        store=True,
        help='Total number of confirmed purchases in the last 12 months',
    )
    
    total_spent = fields.Float(
        string='Total Spent',
        compute='_compute_rfm_data',
        store=True,
        help='Total amount spent in the last 12 months',
    )
    
    recency_score = fields.Integer(
        string='Recency Score',
        compute='_compute_rfm_scores',
        store=True,
        help='Recency score (1-5): How recently the customer made a purchase',
    )
    
    frequency_score = fields.Integer(
        string='Frequency Score',
        compute='_compute_rfm_scores',
        store=True,
        help='Frequency score (1-5): How often the customer makes purchases',
    )
    
    monetary_score = fields.Integer(
        string='Monetary Score',
        compute='_compute_rfm_scores',
        store=True,
        help='Monetary score (1-5): How much the customer spends',
    )
    
    rfm_score = fields.Integer(
        string='RFM Score',
        compute='_compute_rfm_scores',
        store=True,
        help='Combined RFM score (3-15): Sum of Recency, Frequency, and Monetary scores',
    )
    
    rfm_segment = fields.Selection([
        ('champions', 'Champions'),
        ('loyal_customers', 'Loyal Customers'),
        ('potential_loyalists', 'Potential Loyalists'),
        ('new_customers', 'New Customers'),
        ('promising', 'Promising'),
        ('need_attention', 'Need Attention'),
        ('about_to_sleep', 'About to Sleep'),
        ('at_risk', 'At Risk'),
        ('cannot_lose_them', 'Cannot Lose Them'),
        ('hibernating', 'Hibernating'),
        ('lost', 'Lost'),
    ], string='RFM Segment', compute='_compute_rfm_scores', store=True,
        help='Customer segment based on RFM analysis')

    # Engagement Score Fields
    email_engagement_score = fields.Float(
        string='Email Engagement Score',
        compute='_compute_engagement_metrics',
        store=True,
        help='Score based on email opens, clicks, and responses (0-100)',
    )
    
    website_engagement_score = fields.Float(
        string='Website Engagement Score',
        compute='_compute_engagement_metrics',
        store=True,
        help='Score based on website visits, session duration, and page views (0-100)',
    )
    
    whatsapp_engagement_score = fields.Float(
        string='WhatsApp Engagement Score',
        compute='_compute_engagement_metrics',
        store=True,
        help='Score based on WhatsApp campaign responses and interactions (0-100)',
    )
    
    overall_engagement_score = fields.Float(
        string='Overall Engagement Score',
        compute='_compute_engagement_metrics',
        store=True,
        help='Combined engagement score across all channels (0-100)',
    )
    
    engagement_level = fields.Selection([
        ('very_low', 'Very Low (0-20)'),
        ('low', 'Low (21-40)'),
        ('medium', 'Medium (41-60)'),
        ('high', 'High (61-80)'),
        ('very_high', 'Very High (81-100)'),
    ], string='Engagement Level', compute='_compute_engagement_metrics', store=True,
        help='Overall engagement level classification')

    # Customer Journey Stage
    customer_journey_stage = fields.Selection([
        ('awareness', 'Awareness'),
        ('consideration', 'Consideration'),
        ('purchase', 'Active Customer'),
        ('loyalty', 'Loyal Customer'),
        ('advocacy', 'Brand Advocate'),
        ('dormant', 'Dormant'),
    ], string='Customer Journey Stage', compute='_compute_journey_stage', store=True,
        help='Current stage in the customer journey')

    # Multi-Channel Behavior Score
    multichannel_touchpoints = fields.Integer(
        string='Multi-Channel Touchpoints',
        compute='_compute_multichannel_behavior',
        store=True,
        help='Number of different channels customer has interacted with',
    )
    
    multichannel_consistency_score = fields.Float(
        string='Multi-Channel Consistency Score',
        compute='_compute_multichannel_behavior',
        store=True,
        help='Consistency of behavior across channels (0-100)',
    )
    
    preferred_channel = fields.Selection([
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('website', 'Website'),
        ('phone', 'Phone'),
        ('social_media', 'Social Media'),
        ('mixed', 'Mixed/No Clear Preference'),
    ], string='Preferred Channel', compute='_compute_multichannel_behavior', store=True,
        help='Customer\'s preferred communication channel')

    # Churn Prediction
    churn_risk_score = fields.Float(
        string='Churn Risk Score',
        compute='_compute_churn_prediction',
        store=True,
        help='Probability of customer churning in next 90 days (0-100)',
    )
    
    churn_risk_level = fields.Selection([
        ('very_low', 'Very Low Risk (0-20)'),
        ('low', 'Low Risk (21-40)'),
        ('medium', 'Medium Risk (41-60)'),
        ('high', 'High Risk (61-80)'),
        ('very_high', 'Very High Risk (81-100)'),
    ], string='Churn Risk Level', compute='_compute_churn_prediction', store=True,
        help='Churn risk classification')

    # Values-Driven Purchase Propensity
    sustainability_preference_score = fields.Float(
        string='Sustainability Preference Score',
        compute='_compute_values_driven_propensity',
        store=True,
        help='Likelihood to purchase sustainable/eco-friendly products (0-100)',
    )
    
    premium_product_propensity = fields.Float(
        string='Premium Product Propensity',
        compute='_compute_values_driven_propensity',
        store=True,
        help='Likelihood to purchase premium/luxury products (0-100)',
    )
    
    social_responsibility_score = fields.Float(
        string='Social Responsibility Score',
        compute='_compute_values_driven_propensity',
        store=True,
        help='Preference for socially responsible brands (0-100)',
    )

    # Social Commerce Integration
    social_media_source = fields.Selection([
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
        ('none', 'None'),
    ], string='Social Media Source', compute='_compute_social_commerce_metrics', store=True,
        help='Primary social media source for this customer')

    social_referral_count = fields.Integer(
        string='Social Referral Count',
        compute='_compute_social_commerce_metrics',
        store=True,
        help='Number of referrals from social media',
    )
    
    social_engagement_score = fields.Float(
        string='Social Engagement Score',
        compute='_compute_social_commerce_metrics',
        store=True,
        help='Engagement score based on social media interactions (0-100)',
    )
    
    social_conversion_rate = fields.Float(
        string='Social Conversion Rate',
        compute='_compute_social_commerce_metrics',
        store=True,
        help='Conversion rate from social media traffic (0-100)',
    )

    # BNPL and Mobile Commerce Behavior
    bnpl_usage_frequency = fields.Selection([
        ('never', 'Never Used'),
        ('rarely', 'Rarely (1-2 times)'),
        ('sometimes', 'Sometimes (3-5 times)'),
        ('frequently', 'Frequently (6-10 times)'),
        ('always', 'Always (10+ times)'),
    ], string='BNPL Usage Frequency', compute='_compute_bnpl_mobile_behavior', store=True,
        help='How often customer uses Buy Now Pay Later options')

    bnpl_preference_score = fields.Float(
        string='BNPL Preference Score',
        compute='_compute_bnpl_mobile_behavior',
        store=True,
        help='Preference for BNPL payment options (0-100)',
    )
    
    mobile_commerce_score = fields.Float(
        string='Mobile Commerce Score',
        compute='_compute_bnpl_mobile_behavior',
        store=True,
        help='Mobile vs desktop commerce behavior score (0-100)',
    )
    
    mobile_device_preference = fields.Selection([
        ('smartphone', 'Smartphone'),
        ('tablet', 'Tablet'),
        ('desktop', 'Desktop'),
        ('mixed', 'Mixed/No Clear Preference'),
    ], string='Mobile Device Preference', compute='_compute_bnpl_mobile_behavior', store=True,
        help='Preferred device for shopping')

    average_order_value_mobile = fields.Float(
        string='Avg Order Value (Mobile)',
        compute='_compute_bnpl_mobile_behavior',
        store=True,
        help='Average order value on mobile devices',
    )
    
    average_order_value_desktop = fields.Float(
        string='Avg Order Value (Desktop)',
        compute='_compute_bnpl_mobile_behavior',
        store=True,
        help='Average order value on desktop devices',
    )
    
    mobile_conversion_rate = fields.Float(
        string='Mobile Conversion Rate',
        compute='_compute_bnpl_mobile_behavior',
        store=True,
        help='Conversion rate on mobile devices (0-100)',
    )

    @api.depends('date_of_birth')
    def _compute_age(self):
        """Compute age from date of birth"""
        today = date.today()
        for partner in self:
            if partner.date_of_birth:
                # Check if date of birth is not in the future
                if partner.date_of_birth > today:
                    partner.age = 0
                else:
                    # Calculate age using relativedelta for accurate leap year handling
                    delta = relativedelta(today, partner.date_of_birth)
                    partner.age = delta.years
            else:
                partner.age = 0

    @api.depends('age')
    def _compute_age_display(self):
        """Compute age display string"""
        for partner in self:
            if partner.age > 0:
                partner.age_display = f"{partner.age} years"
            else:
                partner.age_display = ""

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        """Validate date of birth"""
        for partner in self:
            if partner.date_of_birth:
                if partner.date_of_birth > date.today():
                    raise models.ValidationError(
                        "Date of birth cannot be in the future."
                    )
                # Check for reasonable age limit (e.g., 150 years)
                if partner.date_of_birth < date.today() - relativedelta(years=150):
                    raise models.ValidationError(
                        "Date of birth cannot be more than 150 years ago."
                    )

    @api.depends('sale_order_ids.date_order', 'sale_order_ids.state', 'sale_order_ids.amount_total')
    def _compute_rfm_data(self):
        """Compute raw RFM data: days since last purchase, purchase count, total spent"""
        today = date.today()
        twelve_months_ago = today - timedelta(days=365)
        
        for partner in self:
            # Check if sale_order_ids field exists (sale module might not be installed)
            if not hasattr(partner, 'sale_order_ids'):
                partner.days_since_last_purchase = 9999
                partner.purchase_count = 0
                partner.total_spent = 0
                continue
                
            # Get confirmed sale orders in the last 12 months
            confirmed_orders = partner.sale_order_ids.filtered(
                lambda order: order.state in ('sale', 'done') and 
                order.date_order and 
                order.date_order.date() >= twelve_months_ago
            )
            
            # Calculate days since last purchase
            if confirmed_orders:
                last_order_date = max(confirmed_orders.mapped('date_order')).date()
                partner.days_since_last_purchase = (today - last_order_date).days
            else:
                # Check if there are any historical orders
                all_orders = partner.sale_order_ids.filtered(
                    lambda order: order.state in ('sale', 'done') and order.date_order
                )
                if all_orders:
                    last_order_date = max(all_orders.mapped('date_order')).date()
                    partner.days_since_last_purchase = (today - last_order_date).days
                else:
                    partner.days_since_last_purchase = 9999  # No purchases ever
            
            # Calculate purchase count (last 12 months)
            partner.purchase_count = len(confirmed_orders)
            
            # Calculate total spent (last 12 months)
            partner.total_spent = sum(confirmed_orders.mapped('amount_total'))

    @api.depends('days_since_last_purchase', 'purchase_count', 'total_spent')
    def _compute_rfm_scores(self):
        """Compute RFM scores and segment classification"""
        # Get all active customers for percentile calculation
        all_customers = self.env['res.partner'].search([
            ('is_company', '=', False),
            ('customer_rank', '>', 0),
            ('active', '=', True)
        ])
        
        if not all_customers:
            # No customers to compare against
            for partner in self:
                partner.recency_score = 0
                partner.frequency_score = 0
                partner.monetary_score = 0
                partner.rfm_score = 0
                partner.rfm_segment = 'lost'
            return
        
        # Calculate percentiles for scoring
        recency_values = [p.days_since_last_purchase for p in all_customers if p.days_since_last_purchase < 9999]
        frequency_values = [p.purchase_count for p in all_customers if p.purchase_count > 0]
        monetary_values = [p.total_spent for p in all_customers if p.total_spent > 0]
        
        # Calculate quintile thresholds
        recency_thresholds = self._calculate_quintiles(recency_values, reverse=True)  # Lower days = higher score
        frequency_thresholds = self._calculate_quintiles(frequency_values)
        monetary_thresholds = self._calculate_quintiles(monetary_values)
        
        for partner in self:
            # Calculate individual scores
            partner.recency_score = self._get_score(partner.days_since_last_purchase, recency_thresholds, reverse=True)
            partner.frequency_score = self._get_score(partner.purchase_count, frequency_thresholds)
            partner.monetary_score = self._get_score(partner.total_spent, monetary_thresholds)
            
            # Calculate combined score
            partner.rfm_score = partner.recency_score + partner.frequency_score + partner.monetary_score
            
            # Determine segment
            partner.rfm_segment = self._get_rfm_segment(
                partner.recency_score, 
                partner.frequency_score, 
                partner.monetary_score
            )

    def _calculate_quintiles(self, values, reverse=False):
        """Calculate quintile thresholds for scoring"""
        if not values:
            return [0, 0, 0, 0, 0]
        
        sorted_values = sorted(values, reverse=reverse)
        n = len(sorted_values)
        
        return [
            sorted_values[int(n * 0.2)] if n > 0 else 0,
            sorted_values[int(n * 0.4)] if n > 0 else 0,
            sorted_values[int(n * 0.6)] if n > 0 else 0,
            sorted_values[int(n * 0.8)] if n > 0 else 0,
            sorted_values[-1] if n > 0 else 0,
        ]

    def _get_score(self, value, thresholds, reverse=False):
        """Get RFM score (1-5) based on value and thresholds"""
        if value == 0 or (reverse and value >= 9999):
            return 1
        
        for i, threshold in enumerate(thresholds):
            if value <= threshold:
                return i + 1
        return 5

    def _get_rfm_segment(self, r, f, m):
        """Determine RFM segment based on individual scores"""
        # Champions: High RFM scores
        if r >= 4 and f >= 4 and m >= 4:
            return 'champions'
        
        # Loyal Customers: High R&F, moderate M
        if r >= 3 and f >= 4 and m >= 3:
            return 'loyal_customers'
        
        # Potential Loyalists: Recent customers with good frequency
        if r >= 4 and f >= 2 and m >= 2:
            return 'potential_loyalists'
        
        # New Customers: Very recent, low frequency
        if r >= 4 and f <= 2 and m <= 2:
            return 'new_customers'
        
        # Promising: Recent customers with potential
        if r >= 3 and f <= 2 and m >= 2:
            return 'promising'
        
        # Need Attention: Moderate across all dimensions
        if r >= 2 and f >= 2 and m >= 2:
            return 'need_attention'
        
        # About to Sleep: Declining recency but good history
        if r >= 2 and f >= 3 and m >= 3:
            return 'about_to_sleep'
        
        # At Risk: Good monetary value but declining
        if r <= 2 and f >= 2 and m >= 3:
            return 'at_risk'
        
        # Cannot Lose Them: High value but very low recency
        if r <= 2 and f >= 4 and m >= 4:
            return 'cannot_lose_them'
        
        # Hibernating: Low recency and frequency but some value
        if r <= 2 and f <= 2 and m >= 2:
            return 'hibernating'
        
        # Lost: Low across all dimensions
        return 'lost'

    @api.depends('message_ids', 'sale_order_ids', 'opportunity_ids')
    def _compute_engagement_metrics(self):
        """Compute engagement scores across all channels"""
        for partner in self:
            # Get data for scoring
            messages = partner.message_ids
            campaigns = self.env['wa_marketing_automation.campaign'].search([
                ('customer_segmentation_id.selected_customers', 'in', partner.ids)
            ])
            
            # Email engagement (based on messages and activities)
            email_score = 0.0
            if partner.email:
                # Count email-related messages in last 90 days
                ninety_days_ago = date.today() - timedelta(days=90)
                email_messages = messages.filtered(
                    lambda m: m.date and m.date.date() >= ninety_days_ago and 
                    m.message_type == 'email'
                )
                # Score based on email activity (0-100)
                email_score = min(len(email_messages) * 5, 100)
            
            # Website engagement (based on sale orders and activities)
            website_score = 0.0
            if partner.customer_rank > 0:
                # Recent orders indicate website engagement
                recent_orders = partner.sale_order_ids.filtered(
                    lambda o: o.date_order and 
                    o.date_order.date() >= date.today() - timedelta(days=90)
                )
                # Score based on order frequency and recency
                if recent_orders:
                    website_score = min(len(recent_orders) * 15 + 20, 100)
                elif partner.sale_order_ids:
                    website_score = 30  # Has historical orders
            
            # WhatsApp engagement (based on campaigns)
            whatsapp_score = 0.0
            if partner.mobile:
                # Count WhatsApp campaigns sent to this customer
                whatsapp_campaigns = campaigns.filtered(
                    lambda c: c.state in ('completed', 'running')
                )
                # Score based on campaign participation
                if whatsapp_campaigns:
                    whatsapp_score = min(len(whatsapp_campaigns) * 10 + 30, 100)
            
            # Overall engagement (weighted average)
            channels_with_score = 0
            total_score = 0
            
            if partner.email:
                channels_with_score += 1
                total_score += email_score
            if partner.customer_rank > 0:
                channels_with_score += 1
                total_score += website_score
            if partner.mobile:
                channels_with_score += 1
                total_score += whatsapp_score
            
            overall_score = total_score / channels_with_score if channels_with_score > 0 else 0
            
            # Set values
            partner.email_engagement_score = email_score
            partner.website_engagement_score = website_score
            partner.whatsapp_engagement_score = whatsapp_score
            partner.overall_engagement_score = overall_score
            
            # Determine engagement level
            if overall_score >= 81:
                partner.engagement_level = 'very_high'
            elif overall_score >= 61:
                partner.engagement_level = 'high'
            elif overall_score >= 41:
                partner.engagement_level = 'medium'
            elif overall_score >= 21:
                partner.engagement_level = 'low'
            else:
                partner.engagement_level = 'very_low'

    @api.depends('rfm_segment', 'days_since_last_purchase', 'customer_rank', 'sale_order_count')
    def _compute_journey_stage(self):
        """Compute customer journey stage based on purchase behavior"""
        for partner in self:
            # Check if sale module is available
            if not hasattr(partner, 'sale_order_count'):
                partner.customer_journey_stage = 'awareness'
                continue
                
            if not partner.is_company:
                if partner.customer_rank == 0:
                    # Never purchased
                    partner.customer_journey_stage = 'awareness'
                elif partner.sale_order_count == 1:
                    # First-time customer
                    partner.customer_journey_stage = 'consideration'
                elif partner.rfm_segment in ('champions', 'loyal_customers'):
                    # High-value loyal customers
                    partner.customer_journey_stage = 'advocacy'
                elif partner.days_since_last_purchase <= 90:
                    # Active customers
                    partner.customer_journey_stage = 'purchase'
                elif partner.days_since_last_purchase <= 180:
                    # Recent customers building loyalty
                    partner.customer_journey_stage = 'loyalty'
                else:
                    # Dormant customers
                    partner.customer_journey_stage = 'dormant'
            else:
                # Company logic (B2B)
                if partner.customer_rank == 0:
                    partner.customer_journey_stage = 'awareness'
                elif partner.sale_order_count >= 5:
                    partner.customer_journey_stage = 'loyalty'
                else:
                    partner.customer_journey_stage = 'purchase'

    @api.depends('email', 'mobile', 'phone', 'message_ids', 'sale_order_ids')
    def _compute_multichannel_behavior(self):
        """Compute multi-channel behavior metrics"""
        for partner in self:
            # Check if sale module is available
            if not hasattr(partner, 'sale_order_ids'):
                partner.multichannel_touchpoints = 0
                partner.preferred_channel = 'email' if partner.email else 'phone'
                partner.multichannel_consistency_score = 0.0
                continue
                
            # Count available channels
            channels = []
            if partner.email:
                channels.append('email')
            if partner.mobile:
                channels.append('whatsapp')
            if partner.phone:
                channels.append('phone')
            if partner.sale_order_ids:
                channels.append('website')
            
            # Count touchpoints
            partner.multichannel_touchpoints = len(channels)
            
            # Determine preferred channel based on activity
            if partner.sale_order_ids and len(partner.sale_order_ids) >= 3:
                partner.preferred_channel = 'website'
            elif partner.mobile and partner.message_ids:
                partner.preferred_channel = 'whatsapp'
            elif partner.email:
                partner.preferred_channel = 'email'
            elif partner.phone:
                partner.preferred_channel = 'phone'
            else:
                partner.preferred_channel = 'mixed'
            
            # Consistency score (how active across channels)
            if partner.multichannel_touchpoints >= 3:
                partner.multichannel_consistency_score = 85.0
            elif partner.multichannel_touchpoints == 2:
                partner.multichannel_consistency_score = 60.0
            elif partner.multichannel_touchpoints == 1:
                partner.multichannel_consistency_score = 30.0
            else:
                partner.multichannel_consistency_score = 0.0

    @api.depends('rfm_segment', 'days_since_last_purchase', 'overall_engagement_score', 'customer_journey_stage')
    def _compute_churn_prediction(self):
        """Compute churn risk score using multiple factors"""
        for partner in self:
            if not partner.is_company and partner.customer_rank > 0:
                churn_score = 0.0
                
                # RFM-based risk (40% weight)
                if partner.rfm_segment in ('lost', 'hibernating'):
                    churn_score += 40.0
                elif partner.rfm_segment in ('cannot_lose_them', 'at_risk'):
                    churn_score += 30.0
                elif partner.rfm_segment in ('about_to_sleep', 'need_attention'):
                    churn_score += 20.0
                elif partner.rfm_segment in ('promising', 'new_customers'):
                    churn_score += 10.0
                
                # Recency factor (30% weight)
                if partner.days_since_last_purchase > 365:
                    churn_score += 30.0
                elif partner.days_since_last_purchase > 180:
                    churn_score += 20.0
                elif partner.days_since_last_purchase > 90:
                    churn_score += 10.0
                
                # Engagement factor (20% weight)
                if partner.overall_engagement_score < 20:
                    churn_score += 20.0
                elif partner.overall_engagement_score < 40:
                    churn_score += 15.0
                elif partner.overall_engagement_score < 60:
                    churn_score += 10.0
                
                # Journey stage factor (10% weight)
                if partner.customer_journey_stage == 'dormant':
                    churn_score += 10.0
                elif partner.customer_journey_stage == 'consideration':
                    churn_score += 5.0
                
                partner.churn_risk_score = min(churn_score, 100.0)
                
                # Determine risk level
                if partner.churn_risk_score >= 81:
                    partner.churn_risk_level = 'very_high'
                elif partner.churn_risk_score >= 61:
                    partner.churn_risk_level = 'high'
                elif partner.churn_risk_score >= 41:
                    partner.churn_risk_level = 'medium'
                elif partner.churn_risk_score >= 21:
                    partner.churn_risk_level = 'low'
                else:
                    partner.churn_risk_level = 'very_low'
            else:
                partner.churn_risk_score = 0.0
                partner.churn_risk_level = 'very_low'

    @api.depends('sale_order_ids.order_line.product_id', 'sale_order_ids.amount_total')
    def _compute_values_driven_propensity(self):
        """Compute values-driven purchase propensity based on product preferences"""
        for partner in self:
            # Check if sale_order_ids field exists (sale module might not be installed)
            if not hasattr(partner, 'sale_order_ids'):
                partner.sustainability_preference_score = 25.0
                partner.premium_product_propensity = 25.0
                partner.social_responsibility_score = 25.0
                continue
                
            if partner.sale_order_ids:
                # Analyze product purchases for patterns
                order_lines = partner.sale_order_ids.mapped('order_line')
                products = order_lines.mapped('product_id')
                
                # Sustainability score (based on product categories and names)
                sustainability_score = 0.0
                sustainability_keywords = ['eco', 'organic', 'sustainable', 'green', 'bio', 'natural']
                sustainable_products = products.filtered(
                    lambda p: any(keyword in p.name.lower() for keyword in sustainability_keywords) if p.name else False
                )
                if products:
                    sustainability_score = (len(sustainable_products) / len(products)) * 100
                
                # Premium product propensity (based on price points)
                premium_score = 0.0
                if order_lines:
                    avg_price = sum(order_lines.mapped('price_unit')) / len(order_lines)
                    # Score based on average price point (adjust thresholds as needed)
                    if avg_price > 500:
                        premium_score = 90.0
                    elif avg_price > 200:
                        premium_score = 70.0
                    elif avg_price > 100:
                        premium_score = 50.0
                    elif avg_price > 50:
                        premium_score = 30.0
                    else:
                        premium_score = 10.0
                
                # Social responsibility score (based on brand preferences)
                social_score = 0.0
                social_keywords = ['fair', 'ethical', 'charity', 'community', 'social']
                social_products = products.filtered(
                    lambda p: any(keyword in p.name.lower() for keyword in social_keywords) if p.name else False
                )
                if products:
                    social_score = (len(social_products) / len(products)) * 100
                
                # Boost scores for loyal customers
                if partner.rfm_segment in ('champions', 'loyal_customers'):
                    sustainability_score = min(sustainability_score * 1.2, 100)
                    premium_score = min(premium_score * 1.1, 100)
                    social_score = min(social_score * 1.2, 100)
                
                partner.sustainability_preference_score = sustainability_score
                partner.premium_product_propensity = premium_score
                partner.social_responsibility_score = social_score
            else:
                # Default scores for customers without purchase history
                partner.sustainability_preference_score = 25.0
                partner.premium_product_propensity = 25.0
                partner.social_responsibility_score = 25.0

    @api.depends('sale_order_ids.source_id', 'sale_order_ids.campaign_id', 'sale_order_ids.medium_id')
    def _compute_social_commerce_metrics(self):
        """Compute social commerce integration metrics based on UTM sources"""
        for partner in self:
            # Check if sale module is available
            if not hasattr(partner, 'sale_order_ids'):
                partner.social_media_source = 'none'
                partner.social_referral_count = 0
                partner.social_engagement_score = 0.0
                partner.social_conversion_rate = 0.0
                continue
                
            if partner.sale_order_ids:
                # Analyze UTM sources from sales orders
                orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
                
                social_sources = []
                social_order_count = 0
                
                # Check for social media sources in UTM data
                for order in orders:
                    if order.source_id:
                        source_name = order.source_id.name.lower()
                        if 'facebook' in source_name or 'fb' in source_name:
                            social_sources.append('facebook')
                            social_order_count += 1
                        elif 'instagram' in source_name or 'ig' in source_name:
                            social_sources.append('instagram')
                            social_order_count += 1
                        elif 'twitter' in source_name:
                            social_sources.append('twitter')
                            social_order_count += 1
                        elif 'linkedin' in source_name:
                            social_sources.append('linkedin')
                            social_order_count += 1
                        elif 'tiktok' in source_name:
                            social_sources.append('tiktok')
                            social_order_count += 1
                        elif 'youtube' in source_name:
                            social_sources.append('youtube')
                            social_order_count += 1
                        elif any(social in source_name for social in ['social', 'share', 'referral']):
                            social_sources.append('other')
                            social_order_count += 1
                
                # Determine primary social media source
                if social_sources:
                    from collections import Counter
                    most_common = Counter(social_sources).most_common(1)
                    partner.social_media_source = most_common[0][0]
                else:
                    partner.social_media_source = 'none'
                
                # Calculate social referral count
                partner.social_referral_count = social_order_count
                
                # Calculate social engagement score
                if len(orders) > 0:
                    social_engagement = (social_order_count / len(orders)) * 100
                    partner.social_engagement_score = min(social_engagement, 100)
                else:
                    partner.social_engagement_score = 0
                
                # Calculate social conversion rate (simplified)
                if social_order_count > 0:
                    # Base conversion rate on social engagement
                    partner.social_conversion_rate = min(social_engagement * 0.8, 100)
                else:
                    partner.social_conversion_rate = 0
                    
            else:
                partner.social_media_source = 'none'
                partner.social_referral_count = 0
                partner.social_engagement_score = 0
                partner.social_conversion_rate = 0

    @api.depends('sale_order_ids.payment_term_id', 'sale_order_ids.amount_total')
    def _compute_bnpl_mobile_behavior(self):
        """Compute BNPL and mobile commerce behavior metrics"""
        for partner in self:
            # Check if sale module is available
            if not hasattr(partner, 'sale_order_ids'):
                partner.bnpl_usage_frequency = 'never'
                partner.bnpl_preference_score = 0.0
                partner.mobile_device_preference = 'unknown'
                partner.mobile_commerce_score = 0.0
                partner.average_order_value_mobile = 0.0
                partner.average_order_value_desktop = 0.0
                partner.mobile_conversion_rate = 0.0
                continue
                
            if partner.sale_order_ids:
                orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
                
                # BNPL Analysis (based on payment terms)
                bnpl_orders = 0
                bnpl_keywords = ['installment', 'split', 'bnpl', 'klarna', 'afterpay', 'sezzle', 'affirm']
                
                for order in orders:
                    if order.payment_term_id:
                        payment_term_name = order.payment_term_id.name.lower()
                        if any(keyword in payment_term_name for keyword in bnpl_keywords):
                            bnpl_orders += 1
                
                # Determine BNPL usage frequency
                if bnpl_orders == 0:
                    partner.bnpl_usage_frequency = 'never'
                elif bnpl_orders <= 2:
                    partner.bnpl_usage_frequency = 'rarely'
                elif bnpl_orders <= 5:
                    partner.bnpl_usage_frequency = 'sometimes'
                elif bnpl_orders <= 10:
                    partner.bnpl_usage_frequency = 'frequently'
                else:
                    partner.bnpl_usage_frequency = 'always'
                
                # Calculate BNPL preference score
                if len(orders) > 0:
                    bnpl_preference = (bnpl_orders / len(orders)) * 100
                    partner.bnpl_preference_score = min(bnpl_preference, 100)
                else:
                    partner.bnpl_preference_score = 0
                
                # Mobile Commerce Analysis (simplified - based on order patterns)
                # In a real implementation, you would track device type from web analytics
                
                # Simulate mobile behavior based on order characteristics
                mobile_orders = 0
                desktop_orders = 0
                mobile_total = 0
                desktop_total = 0
                
                for order in orders:
                    # Heuristic: smaller orders and certain times suggest mobile
                    order_hour = order.date_order.hour if order.date_order else 12
                    
                    # Mobile indicators: off-hours, smaller amounts, certain products
                    if (order_hour < 9 or order_hour > 18) and order.amount_total < 200:
                        mobile_orders += 1
                        mobile_total += order.amount_total
                    else:
                        desktop_orders += 1
                        desktop_total += order.amount_total
                
                # Calculate mobile commerce score
                total_orders = mobile_orders + desktop_orders
                if total_orders > 0:
                    mobile_score = (mobile_orders / total_orders) * 100
                    partner.mobile_commerce_score = mobile_score
                else:
                    partner.mobile_commerce_score = 50  # Default neutral score
                
                # Determine device preference
                if mobile_orders > desktop_orders * 1.5:
                    partner.mobile_device_preference = 'smartphone'
                elif desktop_orders > mobile_orders * 1.5:
                    partner.mobile_device_preference = 'desktop'
                elif mobile_orders > desktop_orders:
                    partner.mobile_device_preference = 'tablet'
                else:
                    partner.mobile_device_preference = 'mixed'
                
                # Calculate average order values
                partner.average_order_value_mobile = mobile_total / mobile_orders if mobile_orders > 0 else 0
                partner.average_order_value_desktop = desktop_total / desktop_orders if desktop_orders > 0 else 0
                
                # Calculate mobile conversion rate (simplified)
                if mobile_orders > 0:
                    # Base on mobile engagement and order frequency
                    partner.mobile_conversion_rate = min(partner.mobile_commerce_score * 0.9, 100)
                else:
                    partner.mobile_conversion_rate = 0
                    
            else:
                partner.bnpl_usage_frequency = 'never'
                partner.bnpl_preference_score = 0
                partner.mobile_commerce_score = 50
                partner.mobile_device_preference = 'mixed'
                partner.average_order_value_mobile = 0
                partner.average_order_value_desktop = 0
                partner.mobile_conversion_rate = 0
    
    def _force_analytics_computation(self):
        """Force computation of all analytics fields for existing customers"""
        import logging
        _logger = logging.getLogger(__name__)
        
        _logger.info(f"Force computing analytics for {len(self)} customers")
        
        # Compute all analytics fields
        compute_methods = [
            '_compute_age',
            '_compute_rfm_data', 
            '_compute_engagement_metrics',
            '_compute_journey_stage',
            '_compute_multichannel_behavior',
            '_compute_churn_prediction',
            '_compute_values_driven_propensity',
            '_compute_social_commerce_metrics',
            '_compute_bnpl_mobile_behavior'
        ]
        
        for method_name in compute_methods:
            if hasattr(self, method_name):
                try:
                    _logger.info(f"Computing {method_name}...")
                    method = getattr(self, method_name)
                    method()
                    _logger.info(f"✓ {method_name} completed")
                except Exception as e:
                    _logger.error(f"✗ Error in {method_name}: {e}")
        
        # Force RFM scoring computation
        try:
            _logger.info("Computing RFM scores...")
            self._compute_rfm_scores()
            _logger.info("✓ RFM scores computed")
        except Exception as e:
            _logger.error(f"✗ Error computing RFM scores: {e}")
        
        _logger.info("Analytics computation complete")