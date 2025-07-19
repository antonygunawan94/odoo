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
        
        if reverse:
            # For recency: lower values (fewer days) get higher scores
            # thresholds are in descending order from _calculate_quintiles
            for i in range(len(thresholds) - 1, -1, -1):
                if value <= thresholds[i]:
                    return i + 1
            return 1  # If value > all thresholds, worst score
        else:
            # For frequency/monetary: higher values get higher scores
            for i, threshold in enumerate(thresholds):
                if value <= threshold:
                    return i + 1
            return 5  # If value > all thresholds, best score

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

    def get_rfm_thresholds_display(self):
        """Get current RFM thresholds formatted for user display"""
        # Get all active customers for threshold calculation
        all_customers = self.env['res.partner'].search([
            ('is_company', '=', False),
            ('customer_rank', '>', 0),
            ('active', '=', True)
        ])
        
        if not all_customers:
            return "No customer data available for threshold calculation"
        
        # Calculate the same thresholds used in scoring
        recency_values = [p.days_since_last_purchase for p in all_customers if p.days_since_last_purchase < 9999]
        frequency_values = [p.purchase_count for p in all_customers if p.purchase_count > 0]
        monetary_values = [p.total_spent for p in all_customers if p.total_spent > 0]
        
        recency_thresholds = self._calculate_quintiles(recency_values, reverse=True)
        frequency_thresholds = self._calculate_quintiles(frequency_values)
        monetary_thresholds = self._calculate_quintiles(monetary_values)
        
        # Format thresholds for display
        def format_currency(amount):
            return f"${amount:,.0f}" if amount > 0 else "$0"
        
        def format_days(days):
            if days == 0:
                return "0 days"
            elif days <= 30:
                return f"{days} days"
            elif days <= 365:
                return f"{days} days ({days//30}+ months)"
            else:
                return f"{days} days ({days//365}+ years)"
        
        display_text = f"""
<strong>📊 Current RFM Scoring Thresholds</strong><br/>
<em>Based on {len(all_customers)} active customers</em><br/><br/>

<strong>🕒 Recency (Days Since Last Purchase):</strong><br/>
• Score 5 (Best): ≤ {format_days(recency_thresholds[4])}<br/>
• Score 4: {format_days(recency_thresholds[4]+1)} - {format_days(recency_thresholds[3])}<br/>
• Score 3: {format_days(recency_thresholds[3]+1)} - {format_days(recency_thresholds[2])}<br/>
• Score 2: {format_days(recency_thresholds[2]+1)} - {format_days(recency_thresholds[1])}<br/>
• Score 1 (Worst): > {format_days(recency_thresholds[1])}<br/><br/>

<strong>🛒 Frequency (Purchases in Last 12 Months):</strong><br/>
• Score 5 (Best): > {frequency_thresholds[3]} purchases<br/>
• Score 4: {frequency_thresholds[2]+1} - {frequency_thresholds[3]} purchases<br/>
• Score 3: {frequency_thresholds[1]+1} - {frequency_thresholds[2]} purchases<br/>
• Score 2: {frequency_thresholds[0]+1} - {frequency_thresholds[1]} purchases<br/>
• Score 1 (Worst): ≤ {frequency_thresholds[0]} purchases<br/><br/>

<strong>💰 Monetary (Total Spent in Last 12 Months):</strong><br/>
• Score 5 (Best): > {format_currency(monetary_thresholds[3])}<br/>
• Score 4: {format_currency(monetary_thresholds[2]+1)} - {format_currency(monetary_thresholds[3])}<br/>
• Score 3: {format_currency(monetary_thresholds[1]+1)} - {format_currency(monetary_thresholds[2])}<br/>
• Score 2: {format_currency(monetary_thresholds[0]+1)} - {format_currency(monetary_thresholds[1])}<br/>
• Score 1 (Worst): ≤ {format_currency(monetary_thresholds[0])}<br/><br/>

<em>📈 Thresholds update automatically as your customer base grows</em>
"""
        return display_text

    rfm_thresholds_display = fields.Html(
        string='RFM Thresholds',
        compute='_compute_rfm_thresholds_display',
        help='Current RFM scoring thresholds for transparency'
    )

    @api.depends_context('uid')
    def _compute_rfm_thresholds_display(self):
        """Compute RFM thresholds display for the current customer base"""
        for partner in self:
            partner.rfm_thresholds_display = self.get_rfm_thresholds_display()

    def get_engagement_calculation_display(self):
        """Get engagement calculation details formatted for user display"""
        config = self.env['res.config.settings'].get_analytics_config()
        
        # Get configuration values
        engagement_period = config.get('engagement_analysis_period', 90)
        email_multiplier = config.get('engagement_email_multiplier', 5)
        website_multiplier = config.get('engagement_website_multiplier', 15)
        website_base = config.get('engagement_website_base', 20)
        website_historical = config.get('engagement_website_historical', 30)
        whatsapp_deal_multiplier = config.get('engagement_whatsapp_deal_multiplier', 25)
        whatsapp_revenue_bonus = config.get('engagement_whatsapp_revenue_bonus', 0.001)
        whatsapp_base_score = config.get('engagement_whatsapp_base_score', 30)
        whatsapp_fallback = config.get('engagement_whatsapp_fallback', 10)
        
        # Get weights
        weights = self._get_adaptive_engagement_weights(config)
        
        display_text = f"""
<strong>📊 Engagement Score Calculation Details</strong><br/>
<em>Analysis period: Last {engagement_period} days</em><br/><br/>

<strong>📧 Email Engagement:</strong><br/>
• <strong>Data source:</strong> Email messages in last {engagement_period} days<br/>
• <strong>Formula:</strong> Email messages × {email_multiplier} (max 100)<br/>
• <strong>Example:</strong> 10 email interactions = {10 * email_multiplier} points<br/><br/>

<strong>🌐 Website Engagement:</strong><br/>
• <strong>Status:</strong> <span style="color: #d73502;"><strong>Currently Disabled</strong></span><br/>
• <strong>Reason:</strong> Sale orders ≠ website engagement (customers can buy offline, by phone, in-store, etc.)<br/>
• <strong>Current score:</strong> Always 0 until real website analytics are implemented<br/>
• <strong>Future implementation:</strong> Will track actual website visits, page views, session time, and content engagement<br/><br/>

<strong>📱 WhatsApp Engagement:</strong><br/>
• <strong>Data source:</strong> Won CRM opportunities with "WhatsApp Campaign" source in last {engagement_period} days<br/>
• <strong>Formula:</strong> Base score ({whatsapp_base_score}) + (Won deals × {whatsapp_deal_multiplier}) + (Revenue × {whatsapp_revenue_bonus}) (max 100)<br/>
• <strong>Fallback:</strong> If in campaigns but no won deals = {whatsapp_fallback} points<br/>
• <strong>Example:</strong> 2 won deals worth $1000 = {whatsapp_base_score} + {2 * whatsapp_deal_multiplier} + {1000 * whatsapp_revenue_bonus} = {whatsapp_base_score + 2 * whatsapp_deal_multiplier + 1000 * whatsapp_revenue_bonus} points<br/><br/>

<strong>🎯 Overall Engagement (Weighted Average):</strong><br/>
"""
        
        for metric, weight in weights.items():
            channel_name = metric.replace('_engagement', '').replace('_', ' ').title()
            display_text += f"• <strong>{channel_name}:</strong> {weight:.1f}% weight<br/>"
        
        display_text += f"""<br/>
<strong>💡 Understanding Your Scores:</strong><br/>
• <strong>Website engagement is currently disabled</strong> because sale orders don't represent true website activity<br/>
• <strong>Email engagement of 0</strong> means no email interactions in last {engagement_period} days<br/>
• <strong>WhatsApp engagement</strong> now tracks actual business results (won deals) rather than just message activity<br/>
• <strong>Overall score</strong> = weighted average of enabled channels (currently Email + WhatsApp only)<br/>
• <strong>When website tracking is implemented</strong>, overall scores will include all three channels<br/><br/>

<em>📈 Scores update automatically based on recent customer activity</em>
"""
        return display_text

    engagement_calculation_display = fields.Html(
        string='Engagement Calculation Details',
        compute='_compute_engagement_calculation_display',
        help='Current engagement scoring logic for transparency'
    )

    @api.depends_context('uid')
    def _compute_engagement_calculation_display(self):
        """Compute engagement calculation display"""
        for partner in self:
            partner.engagement_calculation_display = self.get_engagement_calculation_display()

    def get_journey_multichannel_calculation_display(self):
        """Get journey and multichannel calculation details formatted for user display"""
        config = self.env['res.config.settings'].get_analytics_config()
        
        # Get configuration values
        journey_active_threshold = config.get('journey_active_threshold', 90)
        journey_loyalty_threshold = config.get('journey_loyalty_threshold', 180)
        b2b_loyalty_orders = config.get('journey_b2b_loyalty_orders', 5)
        engagement_period = config.get('engagement_analysis_period', 90)
        
        display_text = f"""
<strong>🗺️ Customer Journey Stage Calculation</strong><br/>
<em>Determines where customers are in their relationship with your business</em><br/><br/>

<strong>📋 Journey Stage Rules:</strong><br/>
<strong>For Individual Customers:</strong><br/>
• <strong>Awareness:</strong> Never made a purchase (customer_rank = 0)<br/>
• <strong>Consideration:</strong> First-time customer (exactly 1 order)<br/>
• <strong>Active Customer:</strong> Recent purchase (last purchase ≤ {journey_active_threshold} days ago)<br/>
• <strong>Loyal Customer:</strong> Moderate recency (last purchase {journey_active_threshold+1}-{journey_loyalty_threshold} days ago)<br/>
• <strong>Brand Advocate:</strong> RFM segment = Champions or Loyal Customers<br/>
• <strong>Dormant:</strong> Long time since purchase (last purchase > {journey_loyalty_threshold} days ago)<br/><br/>

<strong>For Business Customers (B2B):</strong><br/>
• <strong>Awareness:</strong> Never made a purchase<br/>
• <strong>Loyal Customer:</strong> {b2b_loyalty_orders}+ orders (established relationship)<br/>
• <strong>Active Customer:</strong> 1-{b2b_loyalty_orders-1} orders (growing relationship)<br/><br/>

<strong>🌐 Multi-Channel Behavior Calculation</strong><br/>
<em>Analyzes how customers interact across different channels</em><br/><br/>

<strong>📊 Channel Detection:</strong><br/>
• <strong>Email Channel:</strong> Has email address<br/>
• <strong>WhatsApp Channel:</strong> Has mobile number<br/>
• <strong>Phone Channel:</strong> Has phone number<br/>
• <strong>Website Channel:</strong> <span style="color: #d73502;"><strong>Currently Disabled</strong></span> (sale orders ≠ website usage)<br/><br/>

<strong>🎯 Preferred Channel Logic:</strong><br/>
• <strong>WhatsApp:</strong> Won CRM opportunities with "WhatsApp Campaign" source + mobile number (business results)<br/>
• <strong>Email:</strong> Recent email activity in last {engagement_period} days + email address (engagement-based)<br/>
• <strong>Email (Fallback):</strong> Has email address but no recent activity<br/>
• <strong>WhatsApp (Fallback):</strong> Has mobile number but no won deals<br/>
• <strong>Phone (Fallback):</strong> Has phone number only<br/>
• <strong>Mixed:</strong> No contact methods available<br/><br/>

<strong>📈 Consistency Score Rules:</strong><br/>
• <strong>85 points:</strong> 3+ channels available (highly connected)<br/>
• <strong>60 points:</strong> 2 channels available (moderately connected)<br/>
• <strong>30 points:</strong> 1 channel available (limited connectivity)<br/>
• <strong>0 points:</strong> No channels available<br/><br/>

<strong>💡 Understanding Your Results:</strong><br/>
• <strong>Journey stage</strong> shows customer lifecycle position based on purchase behavior<br/>
• <strong>Channel touchpoints</strong> count available communication methods (email, mobile, phone only - website disabled)<br/>
• <strong>Preferred channel</strong> indicates best way to reach this customer based on actual engagement and business results<br/>
• <strong>Consistency score</strong> measures connectivity across available channels (max 3 channels currently)<br/>
• <strong>WhatsApp preference</strong> now based on won deals rather than message activity for better business alignment<br/><br/>

<em>📈 Metrics update automatically based on contact info and purchase activity</em>
"""
        return display_text

    journey_multichannel_calculation_display = fields.Html(
        string='Journey & Multi-Channel Calculation Details',
        compute='_compute_journey_multichannel_calculation_display',
        help='Current journey and multichannel logic for transparency'
    )

    @api.depends_context('uid')
    def _compute_journey_multichannel_calculation_display(self):
        """Compute journey and multichannel calculation display"""
        for partner in self:
            partner.journey_multichannel_calculation_display = self.get_journey_multichannel_calculation_display()

    def get_churn_calculation_display(self):
        """Get churn risk calculation details formatted for user display"""
        config = self.env['res.config.settings'].get_analytics_config()
        
        # Get configuration values
        churn_long_period = config.get('churn_long_period', 365)
        churn_medium_period = config.get('churn_medium_period', 180)
        churn_short_period = config.get('churn_short_period', 90)
        
        churn_engagement_very_low = config.get('churn_engagement_very_low_threshold', 20)
        churn_engagement_low = config.get('churn_engagement_low_threshold', 40)
        churn_engagement_medium = config.get('churn_engagement_medium_threshold', 60)
        
        consistency_very_low = config.get('churn_consistency_very_low_threshold', 20)
        consistency_low = config.get('churn_consistency_low_threshold', 40)
        consistency_medium = config.get('churn_consistency_medium_threshold', 60)
        
        display_text = f"""
<strong>🚨 Churn Risk Calculation</strong><br/>
<em>Predicts the likelihood of customer leaving in the next 90 days</em><br/><br/>

<strong>📊 Risk Factors & Scoring:</strong><br/><br/>

<strong>1️⃣ RFM Segment Analysis (40% weight):</strong><br/>
• <strong>Lost/Hibernating:</strong> 100 points (critical risk)<br/>
• <strong>Cannot Lose Them/At Risk:</strong> 75 points (high risk)<br/>
• <strong>About to Sleep/Need Attention:</strong> 50 points (medium risk)<br/>
• <strong>Promising/New Customers:</strong> 25 points (low risk)<br/>
• <strong>Other segments:</strong> 0 points (minimal risk)<br/><br/>

<strong>2️⃣ Purchase Recency (30% weight):</strong><br/>
• <strong>No purchase > {churn_long_period} days:</strong> 100 points (critical)<br/>
• <strong>No purchase > {churn_medium_period} days:</strong> 65 points (high)<br/>
• <strong>No purchase > {churn_short_period} days:</strong> 35 points (medium)<br/>
• <strong>Recent purchase ≤ {churn_short_period} days:</strong> 0 points (low)<br/><br/>

<strong>3️⃣ Engagement Level (20% weight):</strong><br/>
• <strong>Overall score < {churn_engagement_very_low}:</strong> 100 points (critical)<br/>
• <strong>Overall score < {churn_engagement_low}:</strong> 75 points (high)<br/>
• <strong>Overall score < {churn_engagement_medium}:</strong> 50 points (medium)<br/>
• <strong>Overall score ≥ {churn_engagement_medium}:</strong> 0 points (low)<br/><br/>

<strong>4️⃣ Journey Stage (5% weight):</strong><br/>
• <strong>Dormant stage:</strong> 100 points<br/>
• <strong>Consideration stage:</strong> 50 points<br/>
• <strong>Other stages:</strong> 0 points<br/><br/>

<strong>5️⃣ Multi-Channel Activity (5% weight):</strong><br/>
• <strong>Consistency score < {consistency_very_low}:</strong> 100 points<br/>
• <strong>Consistency score < {consistency_low}:</strong> 65 points<br/>
• <strong>Consistency score < {consistency_medium}:</strong> 35 points<br/>
• <strong>Consistency score ≥ {consistency_medium}:</strong> 0 points<br/><br/>

<strong>🎯 Final Score Calculation:</strong><br/>
• Each factor's points are multiplied by its weight percentage<br/>
• All weighted scores are summed for final risk score (0-100)<br/>
• <strong>Note:</strong> Weights automatically adjust if some metrics are disabled<br/><br/>

<strong>⚡ Risk Level Classification:</strong><br/>
• <strong>Very Low Risk (0-20):</strong> Customer is stable and engaged<br/>
• <strong>Low Risk (21-40):</strong> Minor attention may be beneficial<br/>
• <strong>Medium Risk (41-60):</strong> Proactive engagement recommended<br/>
• <strong>High Risk (61-80):</strong> Immediate action required<br/>
• <strong>Very High Risk (81-100):</strong> Critical - deploy retention strategies<br/><br/>

<strong>💡 Business Actions by Risk Level:</strong><br/>
• <strong>Very Low/Low:</strong> Continue normal engagement, reward loyalty<br/>
• <strong>Medium:</strong> Send personalized offers, increase touchpoints<br/>
• <strong>High:</strong> Direct outreach, special discounts, win-back campaigns<br/>
• <strong>Very High:</strong> Executive attention, maximum retention efforts<br/><br/>

<em>📈 Scores update automatically based on customer behavior changes</em>
"""
        return display_text

    churn_calculation_display = fields.Html(
        string='Churn Risk Calculation Details',
        compute='_compute_churn_calculation_display',
        help='Current churn risk prediction logic for transparency'
    )

    @api.depends_context('uid')
    def _compute_churn_calculation_display(self):
        """Compute churn calculation display"""
        for partner in self:
            partner.churn_calculation_display = self.get_churn_calculation_display()

    def get_values_propensity_calculation_display(self):
        """Get values-driven propensity calculation details formatted for user display"""
        config = self.env['res.config.settings'].get_analytics_config()
        
        # Get configuration values
        eco_keywords = config.get('eco_friendly_keywords', 'eco,organic,sustainable,green,bio,natural')
        social_keywords = config.get('social_responsibility_keywords', 'fair,ethical,charity,community,social')
        
        luxury_threshold = config.get('premium_luxury_threshold', 500.0)
        premium_threshold = config.get('premium_premium_threshold', 200.0)
        midrange_threshold = config.get('premium_midrange_threshold', 100.0)
        budget_plus_threshold = config.get('premium_budget_plus_threshold', 50.0)
        
        eco_boost = config.get('eco_friendly_loyalty_boost', 1.2)
        premium_boost = config.get('premium_loyalty_boost', 1.1)
        social_boost = config.get('social_responsibility_loyalty_boost', 1.2)
        
        display_text = f"""
<strong>🌱 Values & Preferences Calculation</strong><br/>
<em>Analyzes what this customer cares about when making purchases</em><br/><br/>

<strong>🍃 Sustainability Preference Score:</strong><br/>
<strong>How it works:</strong><br/>
• Examines all products purchased by customer<br/>
• Searches for eco-friendly keywords in product names<br/>
• <strong>Keywords:</strong> {eco_keywords}<br/>
• <strong>Formula:</strong> (Eco products ÷ Total products) × 100<br/>
• <strong>Example:</strong> 3 eco products out of 10 = 30% score<br/><br/>

<strong>💎 Premium Product Propensity:</strong><br/>
<strong>Price-based classification:</strong><br/>
• <strong>Luxury (${luxury_threshold}+):</strong> 90 points<br/>
• <strong>Premium (${premium_threshold}-${luxury_threshold}):</strong> 70 points<br/>
• <strong>Mid-range (${midrange_threshold}-${premium_threshold}):</strong> 50 points<br/>
• <strong>Budget Plus (${budget_plus_threshold}-${midrange_threshold}):</strong> 30 points<br/>
• <strong>Budget (< ${budget_plus_threshold}):</strong> 10 points<br/>
<strong>Calculation:</strong> Based on average price of all items purchased<br/><br/>

<strong>🤝 Social Responsibility Score:</strong><br/>
<strong>How it works:</strong><br/>
• Examines all products purchased by customer<br/>
• Searches for social impact keywords in product names<br/>
• <strong>Keywords:</strong> {social_keywords}<br/>
• <strong>Formula:</strong> (Social products ÷ Total products) × 100<br/>
• <strong>Example:</strong> 2 fair-trade products out of 8 = 25% score<br/><br/>

<strong>🎯 Loyalty Boost Factor:</strong><br/>
• Champions & Loyal Customers get score boosts:<br/>
• <strong>Sustainability:</strong> {(eco_boost - 1) * 100:.0f}% boost (max 100)<br/>
• <strong>Premium:</strong> {(premium_boost - 1) * 100:.0f}% boost (max 100)<br/>
• <strong>Social:</strong> {(social_boost - 1) * 100:.0f}% boost (max 100)<br/>
• <strong>Why?</strong> Loyal customers' preferences are more established<br/><br/>

<strong>💡 Understanding the Scores:</strong><br/>
• <strong>0-20:</strong> Little to no interest in this value<br/>
• <strong>21-40:</strong> Some interest, worth testing<br/>
• <strong>41-60:</strong> Moderate preference, good targeting opportunity<br/>
• <strong>61-80:</strong> Strong preference, prioritize these products<br/>
• <strong>81-100:</strong> Core value, central to purchase decisions<br/><br/>

<strong>📊 Data Quality Notes:</strong><br/>
• Scores based on actual purchase history, not surveys<br/>
• Keyword matching depends on product naming accuracy<br/>
• New customers may have low scores due to limited data<br/>
• Scores improve in accuracy with more purchases<br/><br/>

<em>📈 Scores update automatically as customers make new purchases</em>
"""
        return display_text

    values_propensity_calculation_display = fields.Html(
        string='Values & Preferences Calculation Details',
        compute='_compute_values_propensity_calculation_display',
        help='Current values-driven propensity logic for transparency'
    )

    @api.depends_context('uid')
    def _compute_values_propensity_calculation_display(self):
        """Compute values propensity calculation display"""
        for partner in self:
            partner.values_propensity_calculation_display = self.get_values_propensity_calculation_display()

    def get_social_commerce_calculation_display(self):
        """Get social commerce calculation details formatted for user display"""
        config = self.env['res.config.settings'].get_analytics_config()
        
        # Get configuration values
        fb_kw = config.get('social_facebook_keywords', 'facebook,fb')
        ig_kw = config.get('social_instagram_keywords', 'instagram,ig')
        tw_kw = config.get('social_twitter_keywords', 'twitter')
        li_kw = config.get('social_linkedin_keywords', 'linkedin')
        tt_kw = config.get('social_tiktok_keywords', 'tiktok')
        yt_kw = config.get('social_youtube_keywords', 'youtube')
        ot_kw = config.get('social_other_keywords', 'social,share,referral')
        
        display_text = f"""
<strong>📱 Social Commerce Calculation</strong><br/>
<em>Tracks how customers discover and buy from you through social media</em><br/><br/>

<strong>🔍 Social Media Source Detection:</strong><br/>
<strong>How it works:</strong><br/>
• Examines UTM source data from all confirmed orders<br/>
• Searches for platform keywords in order source names<br/>
• Counts most frequent platform as primary source<br/><br/>

<strong>Platform Keywords:</strong><br/>
• <strong>Facebook:</strong> {fb_kw}<br/>
• <strong>Instagram:</strong> {ig_kw}<br/>
• <strong>Twitter:</strong> {tw_kw}<br/>
• <strong>LinkedIn:</strong> {li_kw}<br/>
• <strong>TikTok:</strong> {tt_kw}<br/>
• <strong>YouTube:</strong> {yt_kw}<br/>
• <strong>Other Social:</strong> {ot_kw}<br/><br/>

<strong>📊 Metric Calculations:</strong><br/><br/>

<strong>1️⃣ Social Media Source:</strong><br/>
• Platform with most orders wins (majority rule)<br/>
• If tied, first detected platform is selected<br/>
• "None" if no social media sources found<br/><br/>

<strong>2️⃣ Social Referral Count:</strong><br/>
• Total number of orders from any social media source<br/>
• Includes all platforms, not just primary<br/><br/>

<strong>3️⃣ Social Engagement Score:</strong><br/>
• <strong>Formula:</strong> (Social orders ÷ Total orders) × 100<br/>
• <strong>Example:</strong> 3 social orders out of 10 total = 30% score<br/>
• Shows percentage of business from social media<br/><br/>

<strong>4️⃣ Social Conversion Rate:</strong><br/>
• Measures effectiveness of social traffic<br/>
• <strong>Formula:</strong> Social engagement score × conversion factor<br/>
• Higher scores = better social media ROI<br/><br/>

<strong>💡 Data Requirements:</strong><br/>
• Orders must have UTM source tracking configured<br/>
• Source names must contain platform keywords<br/>
• No source data = "none" classification<br/>
• Works with any UTM tracking tool<br/><br/>

<strong>📈 Business Insights:</strong><br/>
• <strong>Primary source</strong> shows where to focus social efforts<br/>
• <strong>Referral count</strong> shows social media impact on sales<br/>
• <strong>Engagement score</strong> reveals social dependency level<br/>
• <strong>Conversion rate</strong> indicates social traffic quality<br/><br/>

<em>📊 Metrics update automatically as new orders are tracked</em>
"""
        return display_text

    social_commerce_calculation_display = fields.Html(
        string='Social Commerce Calculation Details',
        compute='_compute_social_commerce_calculation_display',
        help='Current social commerce tracking logic for transparency'
    )

    @api.depends_context('uid')
    def _compute_social_commerce_calculation_display(self):
        """Compute social commerce calculation display"""
        for partner in self:
            partner.social_commerce_calculation_display = self.get_social_commerce_calculation_display()

    def get_bnpl_calculation_display(self):
        """Get BNPL calculation details formatted for user display"""
        config = self.env['res.config.settings'].get_analytics_config()
        
        # Get configuration values
        bnpl_keywords = config.get('bnpl_keywords', 'installment,split,bnpl,klarna,afterpay,sezzle,affirm')
        bnpl_rarely_threshold = config.get('bnpl_rarely_threshold', 2)
        bnpl_sometimes_threshold = config.get('bnpl_sometimes_threshold', 5)
        bnpl_frequently_threshold = config.get('bnpl_frequently_threshold', 10)
        
        display_text = f"""
<strong>💳 BNPL (Buy Now Pay Later) Calculation</strong><br/>
<em>Analyzes customer payment preferences for installment and deferred payment options</em><br/><br/>

<strong>🔍 BNPL Detection Method:</strong><br/>
• Examines payment terms on all confirmed orders<br/>
• Searches for BNPL keywords in payment term names<br/>
• <strong>Keywords:</strong> {bnpl_keywords}<br/>
• Counts orders with matching payment terms<br/><br/>

<strong>📊 Usage Frequency Classification:</strong><br/>
• <strong>Never:</strong> 0 BNPL orders<br/>
• <strong>Rarely:</strong> 1-{bnpl_rarely_threshold} BNPL orders<br/>
• <strong>Sometimes:</strong> {bnpl_rarely_threshold + 1}-{bnpl_sometimes_threshold} BNPL orders<br/>
• <strong>Frequently:</strong> {bnpl_sometimes_threshold + 1}-{bnpl_frequently_threshold} BNPL orders<br/>
• <strong>Always:</strong> > {bnpl_frequently_threshold} BNPL orders<br/><br/>

<strong>💯 Preference Score Calculation:</strong><br/>
• <strong>Formula:</strong> (BNPL orders ÷ Total orders) × 100<br/>
• <strong>Example:</strong> 3 BNPL orders out of 12 total = 25% preference<br/>
• Shows percentage of orders using BNPL options<br/>
• Score range: 0-100%<br/><br/>

<strong>🔧 Common BNPL Payment Terms:</strong><br/>
• <strong>Klarna:</strong> Split payments, pay in 30 days<br/>
• <strong>Afterpay:</strong> 4 interest-free installments<br/>
• <strong>Sezzle:</strong> Split into 4 payments<br/>
• <strong>Affirm:</strong> Monthly installments<br/>
• <strong>Generic:</strong> Any "installment" or "split" payment<br/><br/>

<strong>📈 Business Insights:</strong><br/>
• <strong>High preference (60%+):</strong> Always offer BNPL options<br/>
• <strong>Medium preference (30-60%):</strong> Highlight BNPL availability<br/>
• <strong>Low preference (< 30%):</strong> BNPL optional but available<br/>
• <strong>Zero preference:</strong> Focus on standard payment methods<br/><br/>

<strong>⚠️ Mobile Commerce Note:</strong><br/>
• Mobile metrics are <strong>currently disabled</strong> due to unreliable data<br/>
• Cannot accurately determine device type from order data<br/>
• Will be implemented when real device tracking is available<br/><br/>

<em>💳 Scores update automatically as customers choose different payment methods</em>
"""
        return display_text

    bnpl_calculation_display = fields.Html(
        string='BNPL Calculation Details',
        compute='_compute_bnpl_calculation_display',
        help='Current BNPL tracking logic for transparency'
    )

    @api.depends_context('uid')
    def _compute_bnpl_calculation_display(self):
        """Compute BNPL calculation display"""
        for partner in self:
            partner.bnpl_calculation_display = self.get_bnpl_calculation_display()

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
                # TODO: Implement real website engagement tracking
                # Currently disabled because sale orders ≠ website engagement
                # Customers can buy offline, by phone, in-store, etc.
                # Real website engagement should measure:
                # - Page views, session time, content consumption
                # - Website visits without purchases
                # - Click-through rates, form submissions
                # 
                # For now, set to 0 until proper website analytics are available
                scores['website_engagement'] = 0.0
            else:
                scores['website_engagement'] = 0.0
            
            # WhatsApp engagement (if enabled)
            if config.get('enable_whatsapp_engagement', True) and partner.mobile:
                # WhatsApp engagement based on won CRM opportunities from WhatsApp campaigns
                engagement_period = config.get('engagement_analysis_period', 90)
                engagement_days_ago = date.today() - timedelta(days=engagement_period)
                
                # Find won opportunities with WhatsApp Campaign source
                won_opportunities = self.env['crm.lead'].search([
                    ('partner_id', '=', partner.id),
                    ('probability', '=', 100),  # Won deals
                    ('stage_id.is_won', '=', True),  # Ensure stage is marked as won
                    ('source_id.name', 'ilike', 'WhatsApp Campaign%'),  # Source starts with "WhatsApp Campaign"
                    ('create_date', '>=', engagement_days_ago),  # Within engagement period
                    ('active', '=', True)
                ])
                
                # Calculate engagement score based on won deals
                if won_opportunities:
                    # Score based on number of won deals and their value
                    deal_count = len(won_opportunities)
                    total_revenue = sum(won_opportunities.mapped('expected_revenue'))
                    
                    # Base score calculation
                    deal_multiplier = config.get('engagement_whatsapp_deal_multiplier', 25)
                    revenue_bonus = config.get('engagement_whatsapp_revenue_bonus', 0.001)  # Small bonus per currency unit
                    base_score = config.get('engagement_whatsapp_base_score', 30)
                    
                    # Calculate score: base + (deals * multiplier) + (revenue * bonus)
                    calculated_score = base_score + (deal_count * deal_multiplier) + (total_revenue * revenue_bonus)
                    scores['whatsapp_engagement'] = min(calculated_score, 100)
                elif campaigns.filtered(lambda c: c.state in ('completed', 'running')):
                    # Fallback: if in campaigns but no won deals, give modest score
                    scores['whatsapp_engagement'] = config.get('engagement_whatsapp_fallback', 10)
                else:
                    scores['whatsapp_engagement'] = 0.0
            else:
                scores['whatsapp_engagement'] = 0.0
            
            # Calculate adaptive weighted overall score
            weights = self._get_adaptive_engagement_weights(config)
            total_weighted_score = 0.0
            total_weight = 0.0
            
            for metric, weight in weights.items():
                if metric in scores:
                    # Include ALL enabled channels in weighted average, even if score is 0
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

    @api.depends('email', 'mobile', 'phone', 'message_ids', 'opportunity_ids')
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
                
            # Count available channels (excluding website since we can't track real website activity)
            channels = []
            if partner.email:
                channels.append('email')
            if partner.mobile:
                channels.append('whatsapp')
            if partner.phone:
                channels.append('phone')
            # Note: Website channel removed - sale orders don't indicate website usage
            # Customers can buy offline, by phone, in-store, etc.
            
            # Count touchpoints
            partner.multichannel_touchpoints = len(channels)
            
            # Determine preferred channel based on actual business results and engagement
            engagement_period = config.get('engagement_analysis_period', 90)
            engagement_days_ago = date.today() - timedelta(days=engagement_period)
            
            # Check for WhatsApp preference based on won CRM opportunities (consistent with engagement logic)
            won_whatsapp_opportunities = self.env['crm.lead'].search([
                ('partner_id', '=', partner.id),
                ('probability', '=', 100),  # Won deals
                ('stage_id.is_won', '=', True),  # Ensure stage is marked as won
                ('source_id.name', 'ilike', 'WhatsApp Campaign%'),  # Source starts with "WhatsApp Campaign"
                ('create_date', '>=', engagement_days_ago),  # Within engagement period
                ('active', '=', True)
            ])
            
            # Check for email activity (consistent with engagement logic)  
            recent_email_messages = partner.message_ids.filtered(
                lambda m: m.date and m.date.date() >= engagement_days_ago and 
                m.message_type == 'email'
            )
            
            # Determine preference based on actual business activity
            if won_whatsapp_opportunities and partner.mobile:
                partner.preferred_channel = 'whatsapp'  # Has won deals from WhatsApp campaigns
            elif recent_email_messages and partner.email:
                partner.preferred_channel = 'email'  # Active email engagement
            elif partner.email:
                partner.preferred_channel = 'email'  # Has email (fallback)
            elif partner.mobile:
                partner.preferred_channel = 'whatsapp'  # Has mobile (fallback)
            elif partner.phone:
                partner.preferred_channel = 'phone'  # Has phone (fallback)
            else:
                partner.preferred_channel = 'mixed'  # No clear preference
            
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
                
                # Mobile Commerce Analysis - DISABLED DUE TO FUNDAMENTAL FLAWS
                # TODO: Implement real mobile analytics when device tracking is available
                # Current issues (same as website engagement issue):
                # - Order timing ≠ mobile usage (customers can order offline, by phone, in-store, etc.)
                # - Order amount ≠ device type (small orders don't necessarily mean mobile)
                # - Heuristic assumptions are unreliable and create misleading metrics
                # 
                # Real mobile commerce tracking should measure:
                # - Actual device detection from web sessions
                # - Mobile app usage analytics  
                # - User agent strings from real web traffic
                # - Mobile-specific conversion funnels
                #
                # For now, set neutral/disabled values until proper mobile analytics are implemented
                
                partner.mobile_commerce_score = 0.0  # Disabled - no reliable way to track mobile vs desktop orders
                partner.mobile_device_preference = 'mixed'  # Cannot determine without real device tracking
                partner.average_order_value_mobile = 0.0  # Cannot separate mobile vs desktop order values
                partner.average_order_value_desktop = 0.0  # Cannot separate mobile vs desktop order values
                partner.mobile_conversion_rate = 0.0  # Cannot calculate without real mobile analytics
                    
            else:
                # No orders - set defaults
                partner.bnpl_usage_frequency = 'never'
                partner.bnpl_preference_score = 0
                # Mobile commerce - disabled (same as above, no orders doesn't change the fundamental issues)
                partner.mobile_commerce_score = 0.0
                partner.mobile_device_preference = 'mixed'
                partner.average_order_value_mobile = 0.0
                partner.average_order_value_desktop = 0.0
                partner.mobile_conversion_rate = 0.0
    
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