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
        ('unknown', 'Unknown (Disabled)'),
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
        ('unknown', 'Unknown (Disabled)'),
    ], string='Churn Risk Level', compute='_compute_churn_prediction', store=True,
        help='Churn risk classification')

    # Values-Driven Purchase Propensity
    sustainability_preference_score = fields.Float(
        string='Eco-Friendly Score',
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

    # Configuration Visibility Fields
    metrics_engagement_enabled = fields.Boolean(
        string='Engagement Metrics Enabled',
        compute='_compute_metrics_configuration',
        help='Whether engagement scoring is enabled in configuration',
    )
    
    metrics_churn_enabled = fields.Boolean(
        string='Churn Prediction Enabled',
        compute='_compute_metrics_configuration',
        help='Whether churn prediction is enabled in configuration',
    )
    
    metrics_journey_enabled = fields.Boolean(
        string='Customer Journey Enabled',
        compute='_compute_metrics_configuration',
        help='Whether customer journey tracking is enabled in configuration',
    )
    
    metrics_values_enabled = fields.Boolean(
        string='Values Analytics Enabled',
        compute='_compute_metrics_configuration',
        help='Whether values-driven analytics is enabled in configuration',
    )
    
    metrics_social_enabled = fields.Boolean(
        string='Social Commerce Enabled',
        compute='_compute_metrics_configuration',
        help='Whether social commerce analytics is enabled in configuration',
    )
    
    metrics_bnpl_enabled = fields.Boolean(
        string='BNPL Analytics Enabled',
        compute='_compute_metrics_configuration',
        help='Whether BNPL analytics is enabled in configuration',
    )
    
    metrics_mobile_enabled = fields.Boolean(
        string='Mobile Commerce Enabled',
        compute='_compute_metrics_configuration',
        help='Whether mobile commerce analytics is enabled in configuration',
    )
    
    metrics_multichannel_enabled = fields.Boolean(
        string='Multi-Channel Enabled',
        compute='_compute_metrics_configuration',
        help='Whether multi-channel behavior analytics is enabled in configuration',
    )

    def _compute_metrics_configuration(self):
        """Compute metrics configuration visibility flags"""
        config = self.env['res.config.settings'].get_analytics_config()
        
        for partner in self:
            partner.metrics_engagement_enabled = config.get('enable_engagement_scoring', True)
            partner.metrics_churn_enabled = config.get('enable_churn_prediction', True)
            partner.metrics_journey_enabled = config.get('enable_customer_journey', True)
            partner.metrics_values_enabled = config.get('enable_values_analytics', False)
            partner.metrics_social_enabled = config.get('enable_social_commerce', False)
            partner.metrics_bnpl_enabled = config.get('enable_bnpl_analytics', False)
            partner.metrics_mobile_enabled = config.get('enable_mobile_commerce', False)
            partner.metrics_multichannel_enabled = config.get('enable_multichannel_behavior', True)

    def _get_adaptive_churn_weights(self, config):
        """Get adaptive churn prediction weights based on enabled features"""
        base_factors = {
            'rfm_analysis': config.get('churn_rfm_weight', 40),
            'engagement_scoring': config.get('churn_engagement_weight', 30),
            'customer_journey': config.get('churn_journey_weight', 20),
            'multichannel_behavior': config.get('churn_multichannel_weight', 10)
        }
        
        enabled_factors = {}
        disabled_weight = 0
        
        # Check which factors are enabled
        for factor, weight in base_factors.items():
            if factor == 'rfm_analysis':
                enabled_factors[factor] = weight  # Always enabled
            elif factor == 'engagement_scoring' and config.get('enable_engagement_scoring', True):
                enabled_factors[factor] = weight
            elif factor == 'customer_journey' and config.get('enable_customer_journey', True):
                enabled_factors[factor] = weight
            elif factor == 'multichannel_behavior' and config.get('enable_multichannel_behavior', True):
                enabled_factors[factor] = weight
            else:
                disabled_weight += weight
        
        # Redistribute disabled weight proportionally to enabled factors
        if enabled_factors and disabled_weight > 0:
            total_enabled_weight = sum(enabled_factors.values())
            for factor in enabled_factors:
                proportion = enabled_factors[factor] / total_enabled_weight
                enabled_factors[factor] += disabled_weight * proportion
        
        return enabled_factors

    def _get_adaptive_engagement_weights(self, config):
        """Get adaptive engagement weights based on enabled features"""
        base_factors = {
            'email_engagement': config.get('engagement_email_weight', 40),
            'website_engagement': config.get('engagement_website_weight', 35),
            'whatsapp_engagement': config.get('engagement_whatsapp_weight', 25)
        }
        
        enabled_factors = {}
        disabled_weight = 0
        
        # Check which factors are enabled
        for factor, weight in base_factors.items():
            if factor == 'email_engagement' and config.get('enable_email_engagement', True):
                enabled_factors[factor] = weight
            elif factor == 'website_engagement' and config.get('enable_website_engagement', True):
                enabled_factors[factor] = weight
            elif factor == 'whatsapp_engagement' and config.get('enable_whatsapp_engagement', True):
                enabled_factors[factor] = weight
            else:
                disabled_weight += weight
        
        # Ensure at least one factor is enabled
        if not enabled_factors:
            enabled_factors['email_engagement'] = 100  # Fallback
        elif disabled_weight > 0:
            # Redistribute disabled weight proportionally to enabled factors
            total_enabled_weight = sum(enabled_factors.values())
            for factor in enabled_factors:
                proportion = enabled_factors[factor] / total_enabled_weight
                enabled_factors[factor] += disabled_weight * proportion
        
        return enabled_factors

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
        """Compute engagement scores across all channels (adaptive based on configuration)"""
        # Get metrics configuration
        config = self.env['res.config.settings'].get_analytics_config()
        
        for partner in self:
            # Skip if engagement scoring is disabled
            if not config.get('enable_engagement_scoring', True):
                partner.email_engagement_score = 0.0
                partner.website_engagement_score = 0.0
                partner.whatsapp_engagement_score = 0.0
                partner.overall_engagement_score = 0.0
                partner.engagement_level = 'unknown'
                continue
            
            # Get data for scoring
            messages = partner.message_ids
            campaigns = self.env['wa_marketing_automation.campaign'].search([
                ('customer_segmentation_id.selected_customers', 'in', partner.ids)
            ])
            
            # Calculate individual channel scores
            scores = {}
            
            # Email engagement (if enabled)
            if config.get('enable_email_engagement', True) and partner.email:
                engagement_period = config.get('engagement_analysis_period', 90)
                engagement_days_ago = date.today() - timedelta(days=engagement_period)
                email_messages = messages.filtered(
                    lambda m: m.date and m.date.date() >= engagement_days_ago and 
                    m.message_type == 'email'
                )
                email_multiplier = config.get('engagement_email_multiplier', 5)
                scores['email_engagement'] = min(len(email_messages) * email_multiplier, 100)
            else:
                scores['email_engagement'] = 0.0
            
            # Website engagement (if enabled)
            if config.get('enable_website_engagement', True) and partner.customer_rank > 0:
                engagement_period = config.get('engagement_analysis_period', 90)
                recent_orders = partner.sale_order_ids.filtered(
                    lambda o: o.date_order and 
                    o.date_order.date() >= date.today() - timedelta(days=engagement_period)
                )
                if recent_orders:
                    website_multiplier = config.get('engagement_website_multiplier', 15)
                    website_base = config.get('engagement_website_base', 20)
                    scores['website_engagement'] = min(len(recent_orders) * website_multiplier + website_base, 100)
                elif partner.sale_order_ids:
                    scores['website_engagement'] = config.get('engagement_website_historical', 30)  # Has historical orders
                else:
                    scores['website_engagement'] = 0.0
            else:
                scores['website_engagement'] = 0.0
            
            # WhatsApp engagement (if enabled)
            if config.get('enable_whatsapp_engagement', True) and partner.mobile:
                whatsapp_campaigns = campaigns.filtered(
                    lambda c: c.state in ('completed', 'running')
                )
                if whatsapp_campaigns:
                    whatsapp_multiplier = config.get('engagement_whatsapp_multiplier', 10)
                    whatsapp_base = config.get('engagement_whatsapp_base', 30)
                    scores['whatsapp_engagement'] = min(len(whatsapp_campaigns) * whatsapp_multiplier + whatsapp_base, 100)
                else:
                    scores['whatsapp_engagement'] = 0.0
            else:
                scores['whatsapp_engagement'] = 0.0
            
            # Calculate adaptive weighted overall score
            weights = self._get_adaptive_engagement_weights(config)
            total_weighted_score = 0.0
            total_weight = 0.0
            
            for metric, weight in weights.items():
                if metric in scores and scores[metric] > 0:
                    total_weighted_score += scores[metric] * (weight / 100)
                    total_weight += weight / 100
            
            overall_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
            
            # Set individual scores
            partner.email_engagement_score = scores['email_engagement']
            partner.website_engagement_score = scores['website_engagement']
            partner.whatsapp_engagement_score = scores['whatsapp_engagement']
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
        # Get metrics configuration
        config = self.env['res.config.settings'].get_analytics_config()
        
        for partner in self:
            # Check if sale module is available
            if not hasattr(partner, 'sale_order_count'):
                partner.customer_journey_stage = 'awareness'
                continue
                
            journey_active_threshold = config.get('journey_active_threshold', 90)
            journey_loyalty_threshold = config.get('journey_loyalty_threshold', 180)
            b2b_loyalty_orders = config.get('journey_b2b_loyalty_orders', 5)
            
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
                elif partner.days_since_last_purchase <= journey_active_threshold:
                    # Active customers
                    partner.customer_journey_stage = 'purchase'
                elif partner.days_since_last_purchase <= journey_loyalty_threshold:
                    # Recent customers building loyalty
                    partner.customer_journey_stage = 'loyalty'
                else:
                    # Dormant customers
                    partner.customer_journey_stage = 'dormant'
            else:
                # Company logic (B2B)
                if partner.customer_rank == 0:
                    partner.customer_journey_stage = 'awareness'
                elif partner.sale_order_count >= b2b_loyalty_orders:
                    partner.customer_journey_stage = 'loyalty'
                else:
                    partner.customer_journey_stage = 'purchase'

    @api.depends('email', 'mobile', 'phone', 'message_ids', 'sale_order_ids')
    def _compute_multichannel_behavior(self):
        """Compute multi-channel behavior metrics"""
        # Get metrics configuration
        config = self.env['res.config.settings'].get_analytics_config()
        
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
        """Compute churn risk score using multiple factors (adaptive based on configuration)"""
        # Get metrics configuration
        config = self.env['res.config.settings'].get_analytics_config()
        
        for partner in self:
            # Skip if churn prediction is disabled
            if not config.get('enable_churn_prediction', True):
                partner.churn_risk_score = 0.0
                partner.churn_risk_level = 'unknown'
                continue
                
            if not partner.is_company and partner.customer_rank > 0:
                # Get adaptive weights for churn factors
                weights = self._get_adaptive_churn_weights(config)
                churn_score = 0.0
                
                # RFM-based risk (always available)
                rfm_factor = 0.0
                if partner.rfm_segment in ('lost', 'hibernating'):
                    rfm_factor = config.get('churn_rfm_critical_risk', 100.0)
                elif partner.rfm_segment in ('cannot_lose_them', 'at_risk'):
                    rfm_factor = config.get('churn_rfm_high_risk', 75.0)
                elif partner.rfm_segment in ('about_to_sleep', 'need_attention'):
                    rfm_factor = config.get('churn_rfm_medium_risk', 50.0)
                elif partner.rfm_segment in ('promising', 'new_customers'):
                    rfm_factor = config.get('churn_rfm_low_risk', 25.0)
                
                if 'rfm_analysis' in weights:
                    churn_score += rfm_factor * (weights['rfm_analysis'] / 100)
                
                # Recency factor (always available)
                recency_factor = 0.0
                churn_long_period = config.get('churn_long_period', 365)
                churn_medium_period = config.get('churn_medium_period', 180)
                churn_short_period = config.get('churn_short_period', 90)
                if partner.days_since_last_purchase > churn_long_period:
                    recency_factor = config.get('churn_recency_high_risk', 100.0)
                elif partner.days_since_last_purchase > churn_medium_period:
                    recency_factor = config.get('churn_recency_medium_risk', 65.0)
                elif partner.days_since_last_purchase > churn_short_period:
                    recency_factor = config.get('churn_recency_low_risk', 35.0)
                
                # Use a separate recency weight if engagement is disabled
                if 'engagement_scoring' not in weights:
                    # Boost recency weight when engagement is not available
                    enhanced_weights = dict(weights)
                    if 'rfm_analysis' in enhanced_weights:
                        recency_weight = 60  # Higher weight for recency
                        enhanced_weights['rfm_analysis'] = 40
                    else:
                        recency_weight = 100
                    churn_score += recency_factor * (recency_weight / 100)
                else:
                    churn_score += recency_factor * (weights.get('engagement_scoring', 0) / 100 * 0.5)  # Split engagement weight
                
                # Engagement factor (if enabled)
                if 'engagement_scoring' in weights and config.get('enable_engagement_scoring', True):
                    engagement_factor = 0.0
                    churn_engagement_very_low = config.get('churn_engagement_very_low_threshold', 20)
                    churn_engagement_low = config.get('churn_engagement_low_threshold', 40)
                    churn_engagement_medium = config.get('churn_engagement_medium_threshold', 60)
                    if partner.overall_engagement_score < churn_engagement_very_low:
                        engagement_factor = config.get('churn_engagement_critical_risk', 100.0)
                    elif partner.overall_engagement_score < churn_engagement_low:
                        engagement_factor = config.get('churn_engagement_high_risk', 75.0)
                    elif partner.overall_engagement_score < churn_engagement_medium:
                        engagement_factor = config.get('churn_engagement_medium_risk', 50.0)
                    
                    churn_score += engagement_factor * (weights['engagement_scoring'] / 100 * 0.5)  # Split with recency
                
                # Journey stage factor (if enabled)
                if 'customer_journey' in weights and config.get('enable_customer_journey', True):
                    journey_factor = 0.0
                    if partner.customer_journey_stage == 'dormant':
                        journey_factor = 100.0
                    elif partner.customer_journey_stage == 'consideration':
                        journey_factor = 50.0
                    
                    churn_score += journey_factor * (weights['customer_journey'] / 100)
                
                # Multi-channel factor (if enabled)
                if 'multichannel_behavior' in weights and config.get('enable_multichannel_behavior', True):
                    multichannel_factor = 0.0
                    min_touchpoints = config.get('churn_multichannel_min_touchpoints', 1)
                    consistency_low = config.get('churn_multichannel_consistency_low', 30)
                    consistency_medium = config.get('churn_multichannel_consistency_medium', 60)
                    if partner.multichannel_touchpoints <= min_touchpoints:
                        multichannel_factor = config.get('churn_multichannel_high_risk', 80.0)
                    elif partner.multichannel_consistency_score < consistency_low:
                        multichannel_factor = config.get('churn_multichannel_medium_risk', 60.0)
                    elif partner.multichannel_consistency_score < consistency_medium:
                        multichannel_factor = config.get('churn_multichannel_low_risk', 30.0)
                    
                    churn_score += multichannel_factor * (weights['multichannel_behavior'] / 100)
                
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
        """Compute values-driven purchase propensity based on product preferences (adaptive)"""
        # Get metrics configuration
        config = self.env['res.config.settings'].get_analytics_config()
        
        for partner in self:
            # Skip if values analytics is disabled
            if not config.get('enable_values_analytics', False):
                partner.sustainability_preference_score = 0.0
                partner.premium_product_propensity = 0.0
                partner.social_responsibility_score = 0.0
                continue
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
                eco_keywords = config.get('eco_friendly_keywords', 'eco,organic,sustainable,green,bio,natural')
                sustainability_keywords = eco_keywords.split(',') if isinstance(eco_keywords, str) else eco_keywords
                sustainable_products = products.filtered(
                    lambda p: any(keyword.strip() in p.name.lower() for keyword in sustainability_keywords) if p.name else False
                )
                if products:
                    sustainability_score = (len(sustainable_products) / len(products)) * 100
                
                # Premium product propensity (based on price points)
                premium_score = 0.0
                if order_lines:
                    avg_price = sum(order_lines.mapped('price_unit')) / len(order_lines)
                    # Score based on average price point (configurable thresholds)
                    luxury_threshold = config.get('premium_luxury_threshold', 500.0)
                    premium_threshold = config.get('premium_premium_threshold', 200.0)
                    midrange_threshold = config.get('premium_midrange_threshold', 100.0)
                    budget_plus_threshold = config.get('premium_budget_plus_threshold', 50.0)
                    
                    if avg_price > luxury_threshold:
                        premium_score = config.get('premium_luxury_score', 90.0)
                    elif avg_price > premium_threshold:
                        premium_score = config.get('premium_premium_score', 70.0)
                    elif avg_price > midrange_threshold:
                        premium_score = config.get('premium_midrange_score', 50.0)
                    elif avg_price > budget_plus_threshold:
                        premium_score = config.get('premium_budget_plus_score', 30.0)
                    else:
                        premium_score = config.get('premium_budget_score', 10.0)
                
                # Social responsibility score (based on brand preferences)
                social_score = 0.0
                social_resp_keywords = config.get('social_responsibility_keywords', 'fair,ethical,charity,community,social')
                social_keywords = social_resp_keywords.split(',') if isinstance(social_resp_keywords, str) else social_resp_keywords
                social_products = products.filtered(
                    lambda p: any(keyword.strip() in p.name.lower() for keyword in social_keywords) if p.name else False
                )
                if products:
                    social_score = (len(social_products) / len(products)) * 100
                
                # Boost scores for loyal customers
                if partner.rfm_segment in ('champions', 'loyal_customers'):
                    eco_boost = config.get('eco_friendly_loyalty_boost', 1.2)
                    premium_boost = config.get('premium_loyalty_boost', 1.1)
                    social_boost = config.get('social_responsibility_loyalty_boost', 1.2)
                    sustainability_score = min(sustainability_score * eco_boost, 100)
                    premium_score = min(premium_score * premium_boost, 100)
                    social_score = min(social_score * social_boost, 100)
                
                partner.sustainability_preference_score = sustainability_score
                partner.premium_product_propensity = premium_score
                partner.social_responsibility_score = social_score
            else:
                # Default scores for customers without purchase history
                partner.sustainability_preference_score = config.get('eco_friendly_default_score', 25.0)
                partner.premium_product_propensity = config.get('premium_default_score', 25.0)
                partner.social_responsibility_score = config.get('social_responsibility_default_score', 25.0)

    @api.depends('sale_order_ids.source_id', 'sale_order_ids.campaign_id', 'sale_order_ids.medium_id')
    def _compute_social_commerce_metrics(self):
        """Compute social commerce integration metrics based on UTM sources (adaptive)"""
        # Get metrics configuration
        config = self.env['res.config.settings'].get_analytics_config()
        
        for partner in self:
            # Skip if social commerce analytics is disabled
            if not config.get('enable_social_commerce', False):
                partner.social_media_source = 'none'
                partner.social_referral_count = 0
                partner.social_engagement_score = 0.0
                partner.social_conversion_rate = 0.0
                continue
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
                fb_kw = config.get('social_facebook_keywords', 'facebook,fb')
                facebook_keywords = fb_kw.split(',') if isinstance(fb_kw, str) else fb_kw
                ig_kw = config.get('social_instagram_keywords', 'instagram,ig')
                instagram_keywords = ig_kw.split(',') if isinstance(ig_kw, str) else ig_kw
                tw_kw = config.get('social_twitter_keywords', 'twitter')
                twitter_keywords = tw_kw.split(',') if isinstance(tw_kw, str) else tw_kw
                li_kw = config.get('social_linkedin_keywords', 'linkedin')
                linkedin_keywords = li_kw.split(',') if isinstance(li_kw, str) else li_kw
                tt_kw = config.get('social_tiktok_keywords', 'tiktok')
                tiktok_keywords = tt_kw.split(',') if isinstance(tt_kw, str) else tt_kw
                yt_kw = config.get('social_youtube_keywords', 'youtube')
                youtube_keywords = yt_kw.split(',') if isinstance(yt_kw, str) else yt_kw
                ot_kw = config.get('social_other_keywords', 'social,share,referral')
                other_keywords = ot_kw.split(',') if isinstance(ot_kw, str) else ot_kw
                
                for order in orders:
                    if order.source_id:
                        source_name = order.source_id.name.lower()
                        if any(keyword.strip() in source_name for keyword in facebook_keywords):
                            social_sources.append('facebook')
                            social_order_count += 1
                        elif any(keyword.strip() in source_name for keyword in instagram_keywords):
                            social_sources.append('instagram')
                            social_order_count += 1
                        elif any(keyword.strip() in source_name for keyword in twitter_keywords):
                            social_sources.append('twitter')
                            social_order_count += 1
                        elif any(keyword.strip() in source_name for keyword in linkedin_keywords):
                            social_sources.append('linkedin')
                            social_order_count += 1
                        elif any(keyword.strip() in source_name for keyword in tiktok_keywords):
                            social_sources.append('tiktok')
                            social_order_count += 1
                        elif any(keyword.strip() in source_name for keyword in youtube_keywords):
                            social_sources.append('youtube')
                            social_order_count += 1
                        elif any(keyword.strip() in source_name for keyword in other_keywords):
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
                    social_conversion_multiplier = config.get('social_conversion_multiplier', 0.8)
                    partner.social_conversion_rate = min(social_engagement * social_conversion_multiplier, 100)
                else:
                    partner.social_conversion_rate = 0
                    
            else:
                partner.social_media_source = 'none'
                partner.social_referral_count = 0
                partner.social_engagement_score = 0
                partner.social_conversion_rate = 0

    @api.depends('sale_order_ids.payment_term_id', 'sale_order_ids.amount_total')
    def _compute_bnpl_mobile_behavior(self):
        """Compute BNPL and mobile commerce behavior metrics (adaptive)"""
        # Get metrics configuration
        config = self.env['res.config.settings'].get_analytics_config()
        
        for partner in self:
            # Skip if both BNPL and mobile analytics are disabled
            if not config.get('enable_bnpl_analytics', False) and not config.get('enable_mobile_commerce', False):
                partner.bnpl_usage_frequency = 'never'
                partner.bnpl_preference_score = 0.0
                partner.mobile_device_preference = 'mixed'
                partner.mobile_commerce_score = 0.0
                partner.average_order_value_mobile = 0.0
                partner.average_order_value_desktop = 0.0
                partner.mobile_conversion_rate = 0.0
                continue
            # Check if sale module is available
            if not hasattr(partner, 'sale_order_ids'):
                partner.bnpl_usage_frequency = 'never'
                partner.bnpl_preference_score = 0.0
                partner.mobile_device_preference = 'mixed'
                partner.mobile_commerce_score = 0.0
                partner.average_order_value_mobile = 0.0
                partner.average_order_value_desktop = 0.0
                partner.mobile_conversion_rate = 0.0
                continue
                
            if partner.sale_order_ids:
                orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
                
                # BNPL Analysis (based on payment terms)
                bnpl_orders = 0
                bnpl_kw = config.get('bnpl_keywords', 'installment,split,bnpl,klarna,afterpay,sezzle,affirm')
                bnpl_keywords = bnpl_kw.split(',') if isinstance(bnpl_kw, str) else bnpl_kw
                
                for order in orders:
                    if order.payment_term_id:
                        payment_term_name = order.payment_term_id.name.lower()
                        if any(keyword.strip() in payment_term_name for keyword in bnpl_keywords):
                            bnpl_orders += 1
                
                # Determine BNPL usage frequency
                bnpl_rarely_threshold = config.get('bnpl_rarely_threshold', 2)
                bnpl_sometimes_threshold = config.get('bnpl_sometimes_threshold', 5)
                bnpl_frequently_threshold = config.get('bnpl_frequently_threshold', 10)
                
                if bnpl_orders == 0:
                    partner.bnpl_usage_frequency = 'never'
                elif bnpl_orders <= bnpl_rarely_threshold:
                    partner.bnpl_usage_frequency = 'rarely'
                elif bnpl_orders <= bnpl_sometimes_threshold:
                    partner.bnpl_usage_frequency = 'sometimes'
                elif bnpl_orders <= bnpl_frequently_threshold:
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
                    mobile_start_hour = config.get('mobile_start_hour', 9)
                    mobile_end_hour = config.get('mobile_end_hour', 18)
                    mobile_amount_threshold = config.get('mobile_amount_threshold', 200.0)
                    
                    if (order_hour < mobile_start_hour or order_hour > mobile_end_hour) and order.amount_total < mobile_amount_threshold:
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
                    partner.mobile_commerce_score = config.get('mobile_commerce_default_score', 50.0)  # Default neutral score
                
                # Determine device preference
                mobile_preference_ratio = config.get('mobile_preference_ratio', 1.5)
                desktop_preference_ratio = config.get('desktop_preference_ratio', 1.5)
                
                if mobile_orders > desktop_orders * mobile_preference_ratio:
                    partner.mobile_device_preference = 'smartphone'
                elif desktop_orders > mobile_orders * desktop_preference_ratio:
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
                    mobile_conversion_multiplier = config.get('mobile_conversion_multiplier', 0.9)
                    partner.mobile_conversion_rate = min(partner.mobile_commerce_score * mobile_conversion_multiplier, 100)
                else:
                    partner.mobile_conversion_rate = 0
                    
            else:
                partner.bnpl_usage_frequency = 'never'
                partner.bnpl_preference_score = 0
                partner.mobile_commerce_score = config.get('mobile_commerce_default_score', 50.0)
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