import requests
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from ..utils import show_notification


class ResConfigSettings(models.TransientModel):
    """
    WhatsApp Marketing Automation Configuration Settings
    
    This model inherits from res.config.settings following Odoo's standard
    configuration pattern to integrate with the unified settings interface.
    """
    _inherit = 'res.config.settings'

    # =====================================
    # WhatsApp API Configuration
    # =====================================
    
    whatsapp_base_url = fields.Char(
        string='WhatsApp Base API URL',
        help='Base URL for WhatsApp API server (e.g., https://api.whatsapp.com)',
        config_parameter='wa_marketing_automation.whatsapp_base_url',
        default='http://localhost:8000',
    )
    
    whatsapp_access_token = fields.Char(
        string='Access Token',
        help='API access token for WhatsApp service authentication',
        config_parameter='wa_marketing_automation.whatsapp_access_token',
    )
    
    whatsapp_send_path_url = fields.Char(
        string='Send Message URL Path',
        help='API endpoint path for sending messages',
        config_parameter='wa_marketing_automation.whatsapp_send_path_url',
        default='/send-message',
    )
    
    whatsapp_health_check_path_url = fields.Char(
        string='Health Check URL Path',
        help='API endpoint path for health checks',
        config_parameter='wa_marketing_automation.whatsapp_health_check_path_url',
        default='/health',
    )
    
    whatsapp_test_customer_id = fields.Many2one(
        'res.partner',
        string='Test Customer',
        help='Customer record used for testing message templates',
        config_parameter='wa_marketing_automation.whatsapp_test_customer_id',
    )

    # =====================================
    # Analytics Configuration
    # =====================================
    
    # Package Status
    analytics_core_enabled = fields.Boolean(
        string='Core Analytics',
        help='Essential customer metrics including RFM segmentation, engagement tracking, journey mapping, and churn prediction',
        config_parameter='wa_marketing_automation.analytics_core_enabled',
        default=True,
    )
    
    analytics_behavioral_enabled = fields.Boolean(
        string='Behavioral Analytics',
        help='Customer preference insights including values-driven analysis, eco-friendly scoring, and premium propensity',
        config_parameter='wa_marketing_automation.analytics_behavioral_enabled',
        default=False,
    )
    
    analytics_commerce_enabled = fields.Boolean(
        string='Digital Marketing Analytics',
        help='Digital marketing insights including social media tracking, campaign attribution, mobile commerce, and payment preferences',
        config_parameter='wa_marketing_automation.analytics_commerce_enabled',
        default=False,
    )

    # Core Analytics
    enable_rfm_analysis = fields.Boolean(
        string='RFM Analysis',
        help='Segment customers by purchase Recency (days since last order), Frequency (order count), and Monetary value (total spent) to identify your best customers',
        config_parameter='wa_marketing_automation.enable_rfm_analysis',
        default=True,
        readonly=True,  # Always enabled as foundation
    )
    
    enable_engagement_scoring = fields.Boolean(
        string='Engagement Scoring',
        help='Calculate customer engagement levels based on email opens/clicks, WhatsApp message interactions, and website visits to identify highly engaged customers',
        config_parameter='wa_marketing_automation.enable_engagement_scoring',
        default=True,
    )
    
    enable_email_engagement = fields.Boolean(
        string='Email Engagement',
        help='Track email open rates, click-through rates, unsubscribe rates, and campaign performance metrics',
        config_parameter='wa_marketing_automation.enable_email_engagement',
        default=True,
    )
    
    enable_whatsapp_engagement = fields.Boolean(
        string='WhatsApp Engagement',
        help='Monitor WhatsApp message delivery, read receipts, response rates, and conversation quality metrics',
        config_parameter='wa_marketing_automation.enable_whatsapp_engagement',
        default=True,
    )
    
    enable_website_engagement = fields.Boolean(
        string='Website Engagement',
        help='Analyze page views, session duration, bounce rates, product views, and cart abandonment patterns',
        config_parameter='wa_marketing_automation.enable_website_engagement',
        default=True,
    )
    
    enable_customer_journey = fields.Boolean(
        string='Customer Journey Tracking',
        help='Track customer progression through stages: New → Active → Loyal → Champion, or identify At Risk → Dormant → Lost customers',
        config_parameter='wa_marketing_automation.enable_customer_journey',
        default=True,
    )
    
    enable_churn_prediction = fields.Boolean(
        string='Churn Prediction',
        help='Predict likelihood of customer loss based on declining purchase frequency, reduced engagement, and time since last interaction',
        config_parameter='wa_marketing_automation.enable_churn_prediction',
        default=True,
    )
    
    enable_multichannel_behavior = fields.Boolean(
        string='Multi-Channel Behavior',
        help='Analyze how customers interact across email, WhatsApp, website, and in-store channels to optimize marketing mix',
        config_parameter='wa_marketing_automation.enable_multichannel_behavior',
        default=True,
    )
    
    enable_cohort_analysis = fields.Boolean(
        string='Cohort Analysis',
        help='Group customers by signup date and track retention rates over time to measure marketing effectiveness and LTV',
        config_parameter='wa_marketing_automation.enable_cohort_analysis',
        default=True,
    )
    
    # Demographics & Source Analytics (Core Package)
    enable_demographics_analytics = fields.Boolean(
        string='Demographics Analytics',
        help='Analyze customer age groups, spending tiers, and demographic patterns to optimize marketing strategies and customer segmentation',
        config_parameter='wa_marketing_automation.enable_demographics_analytics',
        default=True,
    )
    
    enable_source_analytics = fields.Boolean(
        string='Source Analytics',
        help='Track customer acquisition sources and channels to measure marketing ROI and optimize acquisition spend across different touchpoints',
        config_parameter='wa_marketing_automation.enable_source_analytics',
        default=True,
    )

    # Behavioral Analytics (Behavioral Package)
    enable_values_analytics = fields.Boolean(
        string='Values-Driven Analytics',
        help='Identify customers who prioritize personal values (quality, ethics, social impact) over price when making purchase decisions',
        config_parameter='wa_marketing_automation.enable_values_analytics',
        default=False,
    )
    
    enable_eco_friendly_score = fields.Boolean(
        string='Eco-Friendly Score',
        help='Calculate a 0-100 score based on green product purchases, sustainable shipping choices, and environmental campaign engagement',
        config_parameter='wa_marketing_automation.enable_eco_friendly_score',
        default=False,
    )
    
    enable_premium_propensity = fields.Boolean(
        string='Premium Propensity',
        help='Calculate likelihood of premium/luxury product purchases based on average order value, brand preferences, and purchase category distribution',
        config_parameter='wa_marketing_automation.enable_premium_propensity',
        default=False,
    )
    
    enable_social_responsibility = fields.Boolean(
        string='Social Responsibility',
        help='Track customer preference for socially responsible brands, fair-trade products, and charitable cause alignments through purchase patterns',
        config_parameter='wa_marketing_automation.enable_social_responsibility',
        default=False,
    )
    
    enable_product_category_analytics = fields.Boolean(
        string='Product Category Analytics',
        help='Analyze customer purchase patterns across product categories to identify preferences, diversity, and changes in buying behavior over time',
        config_parameter='wa_marketing_automation.enable_product_category_analytics',
        default=False,
    )

    # Digital Marketing Analytics (Digital Marketing Package)
    enable_social_commerce = fields.Boolean(
        string='Social Media Analytics',
        help='Track sales from Instagram, Facebook, TikTok, and other social platforms using UTM parameters and referral data',
        config_parameter='wa_marketing_automation.enable_social_commerce',
        default=False,
    )
    
    enable_utm_tracking = fields.Boolean(
        string='UTM Tracking',
        help='Capture and analyze UTM source, medium, campaign, term, and content parameters to measure marketing campaign ROI',
        config_parameter='wa_marketing_automation.enable_utm_tracking',
        default=False,
    )
    
    enable_social_engagement = fields.Boolean(
        string='Social Engagement',
        help='Monitor social media interaction rates, share counts, referral traffic, and conversion rates from social channels',
        config_parameter='wa_marketing_automation.enable_social_engagement',
        default=False,
    )
    
    enable_bnpl_analytics = fields.Boolean(
        string='BNPL Analytics',
        help='Analyze Buy Now Pay Later adoption rates, payment completion rates, and average order values for installment purchases',
        config_parameter='wa_marketing_automation.enable_bnpl_analytics',
        default=False,
    )
    
    enable_mobile_commerce = fields.Boolean(
        string='Mobile Commerce',
        help='Compare mobile app vs mobile web vs desktop conversion rates, cart sizes, and shopping session behaviors',
        config_parameter='wa_marketing_automation.enable_mobile_commerce',
        default=False,
    )
    
    enable_device_preference = fields.Boolean(
        string='Device Preference',
        help='Identify primary device usage (iOS/Android/Desktop) and optimize marketing content for preferred platforms',
        config_parameter='wa_marketing_automation.enable_device_preference',
        default=False,
    )

    # =====================================
    # WhatsApp API Methods
    # =====================================
    
    def action_test_whatsapp_connection(self):
        """Test the WhatsApp API connection"""
        self.ensure_one()
        
        if not self.whatsapp_base_url:
            return show_notification(
                self.env,
                title="Configuration Error",
                message="Please configure the WhatsApp Base API URL first.",
                type="warning",
                direct_return=True,
            )

        try:
            response = requests.get(
                f"{self.whatsapp_base_url}{self.whatsapp_health_check_path_url}", 
                timeout=10
            )
            response.raise_for_status()
            return show_notification(
                self.env,
                title="Connection Success",
                message="WhatsApp API connection test successful! ✅",
                type="success",
                direct_return=True,
            )
        except requests.exceptions.SSLError:
            return show_notification(
                self.env,
                title="SSL Certificate Error",
                message=(
                    "SSL certificate issue detected:\n"
                    "• Invalid or expired certificate\n"
                    "• Try using http:// for local testing\n"
                    "• Check certificate configuration"
                ),
                type="danger",
                direct_return=True,
            )
        except requests.exceptions.Timeout:
            return show_notification(
                self.env,
                title="Connection Timeout",
                message=(
                    "API server response timeout:\n"
                    "• Server may be overloaded\n"
                    "• Check network connectivity\n"
                    "• Try again in a few moments"
                ),
                type="warning",
                direct_return=True,
            )
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_messages = {
                404: "Endpoint not found - check health check path",
                401: "Authentication failed - verify access token",
                403: "Access forbidden - check token permissions",
                500: "Server error - contact API provider",
            }
            
            message = error_messages.get(
                status_code, 
                f"HTTP {status_code} error - check configuration"
            )
            
            return show_notification(
                self.env,
                title="API Error",
                message=message,
                type="danger",
                direct_return=True,
            )
        except requests.exceptions.ConnectionError:
            return show_notification(
                self.env,
                title="Connection Failed",
                message=(
                    "Cannot connect to WhatsApp API:\n"
                    "• Check internet connection\n"
                    "• Verify API URL is correct\n"
                    "• Ensure API server is running"
                ),
                type="danger",
                direct_return=True,
            )
        except Exception as e:
            return show_notification(
                self.env,
                title="Unexpected Error",
                message="Error details: %s" % str(e),
                type="danger",
                direct_return=True,
            )

    # =====================================
    # Advanced Analytics Configuration
    # =====================================
    
    # Eco-Friendly Keywords Configuration
    eco_keywords = fields.Char(
        string='Eco Keywords',
        help='Basic eco-friendly keywords',
        config_parameter='wa_marketing_automation.eco_keywords',
        default='eco,green',
    )
    
    organic_keywords = fields.Char(
        string='Organic Keywords',
        help='Organic product keywords',
        config_parameter='wa_marketing_automation.organic_keywords',
        default='organic,bio',
    )
    
    sustainable_keywords = fields.Char(
        string='Sustainable Keywords',
        help='Sustainability keywords',
        config_parameter='wa_marketing_automation.sustainable_keywords',
        default='sustainable,natural',
    )
    
    # Social Responsibility Keywords Configuration
    fair_trade_keywords = fields.Char(
        string='Fair Trade Keywords',
        help='Fair trade and ethical keywords',
        config_parameter='wa_marketing_automation.fair_trade_keywords',
        default='fair,ethical',
    )
    
    charity_keywords = fields.Char(
        string='Charity Keywords',
        help='Charity and community keywords',
        config_parameter='wa_marketing_automation.charity_keywords',
        default='charity,community',
    )
    
    social_cause_keywords = fields.Char(
        string='Social Cause Keywords',
        help='Social cause keywords',
        config_parameter='wa_marketing_automation.social_cause_keywords',
        default='social',
    )
    
    # BNPL Keywords Configuration
    installment_keywords = fields.Char(
        string='Installment Keywords',
        help='Installment payment keywords',
        config_parameter='wa_marketing_automation.installment_keywords',
        default='installment,split',
    )
    
    bnpl_service_keywords = fields.Char(
        string='BNPL Service Keywords',
        help='BNPL service provider keywords',
        config_parameter='wa_marketing_automation.bnpl_service_keywords',
        default='bnpl,klarna,afterpay',
    )
    
    payment_plan_keywords = fields.Char(
        string='Payment Plan Keywords',
        help='Payment plan keywords',
        config_parameter='wa_marketing_automation.payment_plan_keywords',
        default='sezzle,affirm',
    )
    
    # Premium Propensity Thresholds
    premium_threshold_luxury = fields.Float(
        string='Luxury Tier Threshold',
        help='Minimum price for luxury tier (90 points)',
        config_parameter='wa_marketing_automation.premium_threshold_luxury',
        default=500.0,
    )
    
    premium_threshold_premium = fields.Float(
        string='Premium Tier Threshold',
        help='Minimum price for premium tier (70 points)',
        config_parameter='wa_marketing_automation.premium_threshold_premium',
        default=200.0,
    )
    
    premium_threshold_mid = fields.Float(
        string='Mid-Range Tier Threshold',
        help='Minimum price for mid-range tier (50 points)',
        config_parameter='wa_marketing_automation.premium_threshold_mid',
        default=100.0,
    )
    
    premium_threshold_budget_plus = fields.Float(
        string='Budget-Plus Tier Threshold',
        help='Minimum price for budget-plus tier (30 points)',
        config_parameter='wa_marketing_automation.premium_threshold_budget_plus',
        default=50.0,
    )
    
    # Loyalty Bonuses
    eco_friendly_loyalty_bonus = fields.Float(
        string='Eco-Friendly Loyalty Bonus',
        help='Multiplier for eco-friendly scores for loyal customers',
        config_parameter='wa_marketing_automation.eco_friendly_loyalty_bonus',
        default=1.2,
    )
    
    premium_loyalty_bonus = fields.Float(
        string='Premium Loyalty Bonus',
        help='Multiplier for premium scores for loyal customers',
        config_parameter='wa_marketing_automation.premium_loyalty_bonus',
        default=1.1,
    )
    
    social_loyalty_bonus = fields.Float(
        string='Social Responsibility Loyalty Bonus',
        help='Multiplier for social responsibility scores for loyal customers',
        config_parameter='wa_marketing_automation.social_loyalty_bonus',
        default=1.2,
    )
    
    # Default Values
    values_default_score = fields.Float(
        string='Default Values Score',
        help='Default score for customers without purchase history',
        config_parameter='wa_marketing_automation.values_default_score',
        default=25.0,
    )
    
    # Time Windows (removed duplicate rfm_analysis_period - using rfm_analysis_period_days instead)
    
    email_engagement_period = fields.Integer(
        string='Email Engagement Period (Days)',
        help='Number of days to consider for email engagement calculation',
        config_parameter='wa_marketing_automation.email_engagement_period',
        default=90,
    )
    
    website_engagement_period = fields.Integer(
        string='Website Engagement Period (Days)',
        help='Number of days to consider for website engagement calculation',
        config_parameter='wa_marketing_automation.website_engagement_period',
        default=90,
    )
    
    # Engagement Scoring Parameters
    email_points_per_message = fields.Integer(
        string='Email Points per Message',
        help='Points awarded per email message',
        config_parameter='wa_marketing_automation.email_points_per_message',
        default=5,
    )
    
    website_points_per_order = fields.Integer(
        string='Website Points per Order',
        help='Points awarded per recent website order',
        config_parameter='wa_marketing_automation.website_points_per_order',
        default=15,
    )
    
    website_base_points = fields.Integer(
        string='Website Base Points',
        help='Base points for website engagement',
        config_parameter='wa_marketing_automation.website_base_points',
        default=20,
    )
    
    website_historical_points = fields.Integer(
        string='Website Historical Points',
        help='Points for having historical orders',
        config_parameter='wa_marketing_automation.website_historical_points',
        default=30,
    )
    
    whatsapp_points_per_campaign = fields.Integer(
        string='WhatsApp Points per Campaign',
        help='Points awarded per WhatsApp campaign',
        config_parameter='wa_marketing_automation.whatsapp_points_per_campaign',
        default=10,
    )
    
    whatsapp_base_points = fields.Integer(
        string='WhatsApp Base Points',
        help='Base points for WhatsApp engagement',
        config_parameter='wa_marketing_automation.whatsapp_base_points',
        default=30,
    )
    
    # Engagement Channel Weights
    email_engagement_weight = fields.Float(
        string='Email Engagement Weight (%)',
        help='Weight for email engagement in overall score',
        config_parameter='wa_marketing_automation.email_engagement_weight',
        default=40.0,
    )
    
    website_engagement_weight = fields.Float(
        string='Website Engagement Weight (%)',
        help='Weight for website engagement in overall score',
        config_parameter='wa_marketing_automation.website_engagement_weight',
        default=35.0,
    )
    
    whatsapp_engagement_weight = fields.Float(
        string='WhatsApp Engagement Weight (%)',
        help='Weight for WhatsApp engagement in overall score',
        config_parameter='wa_marketing_automation.whatsapp_engagement_weight',
        default=25.0,
    )
    
    # Churn Prediction Weights
    churn_rfm_weight = fields.Float(
        string='Churn RFM Weight (%)',
        help='Weight for RFM analysis in churn prediction',
        config_parameter='wa_marketing_automation.churn_rfm_weight',
        default=40.0,
    )
    
    churn_engagement_weight = fields.Float(
        string='Churn Engagement Weight (%)',
        help='Weight for engagement scoring in churn prediction',
        config_parameter='wa_marketing_automation.churn_engagement_weight',
        default=30.0,
    )
    
    churn_journey_weight = fields.Float(
        string='Churn Journey Weight (%)',
        help='Weight for customer journey in churn prediction',
        config_parameter='wa_marketing_automation.churn_journey_weight',
        default=20.0,
    )
    
    churn_multichannel_weight = fields.Float(
        string='Churn Multichannel Weight (%)',
        help='Weight for multichannel behavior in churn prediction',
        config_parameter='wa_marketing_automation.churn_multichannel_weight',
        default=10.0,
    )
    
    # Mobile Commerce Configuration
    mobile_order_threshold = fields.Float(
        string='Mobile Order Threshold',
        help='Maximum order amount to consider as mobile commerce',
        config_parameter='wa_marketing_automation.mobile_order_threshold',
        default=200.0,
    )
    
    mobile_hour_start = fields.Integer(
        string='Mobile Hours Start',
        help='Start hour for mobile commerce detection (24-hour format)',
        config_parameter='wa_marketing_automation.mobile_hour_start',
        default=9,
    )
    
    mobile_hour_end = fields.Integer(
        string='Mobile Hours End',
        help='End hour for mobile commerce detection (24-hour format)',
        config_parameter='wa_marketing_automation.mobile_hour_end',
        default=18,
    )
    
    mobile_device_preference_threshold = fields.Float(
        string='Mobile Device Preference Threshold',
        help='Multiplier threshold for device preference detection',
        config_parameter='wa_marketing_automation.mobile_device_preference_threshold',
        default=1.5,
    )
    
    # Social Commerce Configuration
    social_conversion_rate_multiplier = fields.Float(
        string='Social Conversion Rate Multiplier',
        help='Multiplier for social conversion rate calculation',
        config_parameter='wa_marketing_automation.social_conversion_rate_multiplier',
        default=0.8,
    )
    
    mobile_conversion_rate_multiplier = fields.Float(
        string='Mobile Conversion Rate Multiplier',
        help='Multiplier for mobile conversion rate calculation',
        config_parameter='wa_marketing_automation.mobile_conversion_rate_multiplier',
        default=0.9,
    )
    
    mobile_default_score = fields.Float(
        string='Mobile Default Score',
        help='Default score for mobile commerce when no data available',
        config_parameter='wa_marketing_automation.mobile_default_score',
        default=50.0,
    )
    
    # Multichannel Consistency Scores
    multichannel_3plus_score = fields.Float(
        string='3+ Touchpoints Score',
        help='Consistency score for 3+ touchpoints',
        config_parameter='wa_marketing_automation.multichannel_3plus_score',
        default=85.0,
    )
    
    multichannel_2_score = fields.Float(
        string='2 Touchpoints Score',
        help='Consistency score for 2 touchpoints',
        config_parameter='wa_marketing_automation.multichannel_2_score',
        default=60.0,
    )
    
    multichannel_1_score = fields.Float(
        string='1 Touchpoint Score',
        help='Consistency score for 1 touchpoint',
        config_parameter='wa_marketing_automation.multichannel_1_score',
        default=30.0,
    )
    
    # Churn Risk Thresholds
    churn_risk_very_high_threshold = fields.Float(
        string='Very High Churn Risk Threshold',
        help='Minimum score for very high churn risk classification',
        config_parameter='wa_marketing_automation.churn_risk_very_high_threshold',
        default=81.0,
    )
    
    churn_risk_high_threshold = fields.Float(
        string='High Churn Risk Threshold',
        help='Minimum score for high churn risk classification',
        config_parameter='wa_marketing_automation.churn_risk_high_threshold',
        default=61.0,
    )
    
    churn_risk_medium_threshold = fields.Float(
        string='Medium Churn Risk Threshold',
        help='Minimum score for medium churn risk classification',
        config_parameter='wa_marketing_automation.churn_risk_medium_threshold',
        default=41.0,
    )
    
    churn_risk_low_threshold = fields.Float(
        string='Low Churn Risk Threshold',
        help='Minimum score for low churn risk classification',
        config_parameter='wa_marketing_automation.churn_risk_low_threshold',
        default=21.0,
    )
    
    churn_risk_min_tier_threshold = fields.Float(
        string='Minimum Valuable Customer Spending Threshold',
        help='Minimum spending tier threshold (in currency) to consider customers valuable for churn risk analysis. Customers in tiers below this amount will be excluded from win-back campaigns.',
        config_parameter='wa_marketing_automation.churn_risk_min_tier_threshold',
        default=500.0,
    )
    
    # Churn Risk Factors
    churn_recency_365_risk = fields.Float(
        string='Recency >365 Days Risk',
        help='Risk score for customers with >365 days since last purchase',
        config_parameter='wa_marketing_automation.churn_recency_365_risk',
        default=100.0,
    )
    
    churn_recency_180_risk = fields.Float(
        string='Recency >180 Days Risk',
        help='Risk score for customers with >180 days since last purchase',
        config_parameter='wa_marketing_automation.churn_recency_180_risk',
        default=65.0,
    )
    
    churn_recency_90_risk = fields.Float(
        string='Recency >90 Days Risk',
        help='Risk score for customers with >90 days since last purchase',
        config_parameter='wa_marketing_automation.churn_recency_90_risk',
        default=35.0,
    )
    
    churn_engagement_20_risk = fields.Float(
        string='Engagement <20 Risk',
        help='Risk score for customers with <20 engagement score',
        config_parameter='wa_marketing_automation.churn_engagement_20_risk',
        default=100.0,
    )
    
    churn_engagement_40_risk = fields.Float(
        string='Engagement <40 Risk',
        help='Risk score for customers with <40 engagement score',
        config_parameter='wa_marketing_automation.churn_engagement_40_risk',
        default=75.0,
    )
    
    churn_engagement_60_risk = fields.Float(
        string='Engagement <60 Risk',
        help='Risk score for customers with <60 engagement score',
        config_parameter='wa_marketing_automation.churn_engagement_60_risk',
        default=50.0,
    )
    
    churn_multichannel_1_risk = fields.Float(
        string='Single Channel Risk',
        help='Risk score for customers with ≤1 touchpoint',
        config_parameter='wa_marketing_automation.churn_multichannel_1_risk',
        default=80.0,
    )
    
    churn_multichannel_30_risk = fields.Float(
        string='Low Consistency Risk',
        help='Risk score for customers with <30 consistency score',
        config_parameter='wa_marketing_automation.churn_multichannel_30_risk',
        default=60.0,
    )
    
    churn_multichannel_60_risk = fields.Float(
        string='Medium Consistency Risk',
        help='Risk score for customers with <60 consistency score',
        config_parameter='wa_marketing_automation.churn_multichannel_60_risk',
        default=30.0,
    )
    
    # RFM Risk Scores
    churn_rfm_lost_hibernating_risk = fields.Float(
        string='Lost/Hibernating RFM Risk',
        help='Risk score for lost/hibernating RFM segments',
        config_parameter='wa_marketing_automation.churn_rfm_lost_hibernating_risk',
        default=100.0,
    )
    
    churn_rfm_at_risk_risk = fields.Float(
        string='At Risk RFM Risk',
        help='Risk score for cannot_lose_them/at_risk RFM segments',
        config_parameter='wa_marketing_automation.churn_rfm_at_risk_risk',
        default=75.0,
    )
    
    churn_rfm_need_attention_risk = fields.Float(
        string='Need Attention RFM Risk',
        help='Risk score for about_to_sleep/need_attention RFM segments',
        config_parameter='wa_marketing_automation.churn_rfm_need_attention_risk',
        default=50.0,
    )
    
    churn_rfm_new_customers_risk = fields.Float(
        string='New Customers RFM Risk',
        help='Risk score for promising/new_customers RFM segments',
        config_parameter='wa_marketing_automation.churn_rfm_new_customers_risk',
        default=25.0,
    )
    
    # Journey Stage Risk Scores
    churn_journey_dormant_risk = fields.Float(
        string='Dormant Journey Risk',
        help='Risk score for dormant journey stage',
        config_parameter='wa_marketing_automation.churn_journey_dormant_risk',
        default=100.0,
    )
    
    churn_journey_consideration_risk = fields.Float(
        string='Consideration Journey Risk',
        help='Risk score for consideration journey stage',
        config_parameter='wa_marketing_automation.churn_journey_consideration_risk',
        default=50.0,
    )
    
    # Social Commerce Platform Keywords
    facebook_keywords = fields.Char(
        string='Facebook Keywords',
        help='Keywords to identify Facebook traffic (comma-separated)',
        config_parameter='wa_marketing_automation.facebook_keywords',
        default='facebook,fb',
    )
    
    instagram_keywords = fields.Char(
        string='Instagram Keywords',
        help='Keywords to identify Instagram traffic (comma-separated)',
        config_parameter='wa_marketing_automation.instagram_keywords',
        default='instagram,ig',
    )
    
    twitter_keywords = fields.Char(
        string='Twitter Keywords',
        help='Keywords to identify Twitter traffic (comma-separated)',
        config_parameter='wa_marketing_automation.twitter_keywords',
        default='twitter',
    )
    
    linkedin_keywords = fields.Char(
        string='LinkedIn Keywords',
        help='Keywords to identify LinkedIn traffic (comma-separated)',
        config_parameter='wa_marketing_automation.linkedin_keywords',
        default='linkedin',
    )
    
    tiktok_keywords = fields.Char(
        string='TikTok Keywords',
        help='Keywords to identify TikTok traffic (comma-separated)',
        config_parameter='wa_marketing_automation.tiktok_keywords',
        default='tiktok',
    )
    
    youtube_keywords = fields.Char(
        string='YouTube Keywords',
        help='Keywords to identify YouTube traffic (comma-separated)',
        config_parameter='wa_marketing_automation.youtube_keywords',
        default='youtube',
    )
    
    other_social_keywords = fields.Char(
        string='Other Social Keywords',
        help='Keywords to identify other social media traffic (comma-separated)',
        config_parameter='wa_marketing_automation.other_social_keywords',
        default='social,share,referral',
    )
    
    # BNPL Usage Frequency Thresholds
    bnpl_rarely_threshold = fields.Integer(
        string='BNPL Rarely Threshold',
        help='Maximum orders for rarely usage classification',
        config_parameter='wa_marketing_automation.bnpl_rarely_threshold',
        default=2,
    )
    
    bnpl_sometimes_threshold = fields.Integer(
        string='BNPL Sometimes Threshold',
        help='Maximum orders for sometimes usage classification',
        config_parameter='wa_marketing_automation.bnpl_sometimes_threshold',
        default=5,
    )
    
    bnpl_frequently_threshold = fields.Integer(
        string='BNPL Frequently Threshold',
        help='Maximum orders for frequently usage classification',
        config_parameter='wa_marketing_automation.bnpl_frequently_threshold',
        default=10,
    )
    
    # Engagement Level Thresholds
    engagement_very_high_threshold = fields.Float(
        string='Very High Engagement Threshold',
        help='Minimum score for very high engagement classification',
        config_parameter='wa_marketing_automation.engagement_very_high_threshold',
        default=81.0,
    )
    
    engagement_high_threshold = fields.Float(
        string='High Engagement Threshold',
        help='Minimum score for high engagement classification',
        config_parameter='wa_marketing_automation.engagement_high_threshold',
        default=61.0,
    )
    
    engagement_medium_threshold = fields.Float(
        string='Medium Engagement Threshold',
        help='Minimum score for medium engagement classification',
        config_parameter='wa_marketing_automation.engagement_medium_threshold',
        default=41.0,
    )
    
    engagement_low_threshold = fields.Float(
        string='Low Engagement Threshold',
        help='Minimum score for low engagement classification',
        config_parameter='wa_marketing_automation.engagement_low_threshold',
        default=21.0,
    )
    
    # Premium Propensity Scores
    premium_score_luxury = fields.Float(
        string='Luxury Tier Score',
        help='Points awarded for luxury tier purchases',
        config_parameter='wa_marketing_automation.premium_score_luxury',
        default=90.0,
    )
    
    premium_score_premium = fields.Float(
        string='Premium Tier Score',
        help='Points awarded for premium tier purchases',
        config_parameter='wa_marketing_automation.premium_score_premium',
        default=70.0,
    )
    
    premium_score_mid = fields.Float(
        string='Mid-Range Tier Score',
        help='Points awarded for mid-range tier purchases',
        config_parameter='wa_marketing_automation.premium_score_mid',
        default=50.0,
    )
    
    premium_score_budget_plus = fields.Float(
        string='Budget-Plus Tier Score',
        help='Points awarded for budget-plus tier purchases',
        config_parameter='wa_marketing_automation.premium_score_budget_plus',
        default=30.0,
    )
    
    premium_score_budget = fields.Float(
        string='Budget Tier Score',
        help='Points awarded for budget tier purchases',
        config_parameter='wa_marketing_automation.premium_score_budget',
        default=10.0,
    )
    
    # RFM Quintile Percentiles
    rfm_quintile_1 = fields.Float(
        string='RFM Quintile 1',
        help='First quintile percentile for RFM scoring',
        config_parameter='wa_marketing_automation.rfm_quintile_1',
        default=0.2,
    )
    
    rfm_quintile_2 = fields.Float(
        string='RFM Quintile 2',
        help='Second quintile percentile for RFM scoring',
        config_parameter='wa_marketing_automation.rfm_quintile_2',
        default=0.4,
    )
    
    rfm_quintile_3 = fields.Float(
        string='RFM Quintile 3',
        help='Third quintile percentile for RFM scoring',
        config_parameter='wa_marketing_automation.rfm_quintile_3',
        default=0.6,
    )
    
    rfm_quintile_4 = fields.Float(
        string='RFM Quintile 4',
        help='Fourth quintile percentile for RFM scoring',
        config_parameter='wa_marketing_automation.rfm_quintile_4',
        default=0.8,
    )
    
    # =====================================
    # Demographics & Product Category Advanced Configuration
    # =====================================
    
    # Age and Customer Validation
    age_validation_limit = fields.Integer(
        string='Age Validation Limit (Years)',
        help='Maximum reasonable age for customer demographics validation',
        config_parameter='wa_marketing_automation.age_validation_limit',
        default=150,
    )
    
    new_customer_threshold = fields.Integer(
        string='New Customer Order Threshold',
        help='Maximum number of orders to consider a customer as "new"',
        config_parameter='wa_marketing_automation.new_customer_threshold',
        default=1,
    )
    
    # Analysis Time Periods  
    rfm_analysis_period_days = fields.Integer(
        string='RFM Analysis Period (Days)',
        help='Number of days to look back for RFM (Recency, Frequency, Monetary) analysis',
        config_parameter='wa_marketing_automation.rfm_analysis_period_days',
        default=365,
    )
    
    category_analysis_period_days = fields.Integer(
        string='Category Analysis Period (Days)',
        help='Number of days to look back for product category analysis and diversity scoring',
        config_parameter='wa_marketing_automation.category_analysis_period_days',
        default=180,
    )
    
    # Product Category Analytics Configuration
    max_reasonable_categories = fields.Integer(
        string='Maximum Reasonable Categories',
        help='Maximum number of product categories considered reasonable for diversity scoring',
        config_parameter='wa_marketing_automation.max_reasonable_categories',
        default=20,
    )
    
    category_change_positive_threshold = fields.Float(
        string='Category Change Positive Threshold (%)',
        help='Percentage increase required to detect significant positive change in category spending',
        config_parameter='wa_marketing_automation.category_change_positive_threshold',
        default=20.0,
    )
    
    category_change_negative_threshold = fields.Float(
        string='Category Change Negative Threshold (%)',
        help='Percentage decrease required to detect significant negative change in category spending (positive value)',
        config_parameter='wa_marketing_automation.category_change_negative_threshold',
        default=20.0,
    )
    
    # Diversity Score Thresholds
    diversity_score_high_threshold = fields.Float(
        string='High Diversity Score Threshold',
        help='Minimum score to classify customer as having high product diversity',
        config_parameter='wa_marketing_automation.diversity_score_high_threshold',
        default=70.0,
    )
    
    diversity_score_medium_threshold = fields.Float(
        string='Medium Diversity Score Threshold',
        help='Minimum score to classify customer as having medium product diversity',
        config_parameter='wa_marketing_automation.diversity_score_medium_threshold',
        default=40.0,
    )
    
    # Category Ranking Weights
    category_spending_weight = fields.Float(
        string='Category Spending Weight',
        help='Weight factor for spending amount in category ranking calculation (0.0-1.0)',
        config_parameter='wa_marketing_automation.category_spending_weight',
        default=0.7,
    )
    
    category_frequency_weight = fields.Float(
        string='Category Frequency Weight',
        help='Weight factor for purchase frequency in category ranking calculation (0.0-1.0)',
        config_parameter='wa_marketing_automation.category_frequency_weight',
        default=0.3,
    )
    
    # Values Preference Detection Thresholds
    values_strong_preference_threshold = fields.Float(
        string='Strong Preference Threshold (%)',
        help='Minimum score to be considered as having a strong preference for a value category',
        config_parameter='wa_marketing_automation.values_strong_preference_threshold',
        default=50.0,
    )
    
    values_targeting_threshold = fields.Float(
        string='Targeting Preference Threshold (%)',
        help='Minimum score for a value category to be used as primary targeting angle',
        config_parameter='wa_marketing_automation.values_targeting_threshold',
        default=30.0,
    )

    # =====================================
    # Package Selection Onchange Methods
    # =====================================
    
    @api.onchange('analytics_core_enabled')
    def _onchange_analytics_core_enabled(self):
        """When Core Analytics is enabled/disabled, update related metrics"""
        if self.analytics_core_enabled:
            self.enable_engagement_scoring = True
            self.enable_email_engagement = True
            self.enable_whatsapp_engagement = True
            self.enable_website_engagement = True
            self.enable_customer_journey = True
            self.enable_churn_prediction = True
            self.enable_multichannel_behavior = True
            self.enable_cohort_analysis = True
            # Demographics & Source Analytics (Core Package)
            self.enable_demographics_analytics = True
            self.enable_source_analytics = True
        else:
            # If core is disabled, disable all packages
            self.analytics_behavioral_enabled = False
            self.analytics_commerce_enabled = False
            self.enable_engagement_scoring = False
            self.enable_email_engagement = False
            self.enable_whatsapp_engagement = False
            self.enable_website_engagement = False
            self.enable_customer_journey = False
            self.enable_churn_prediction = False
            self.enable_multichannel_behavior = False
            self.enable_cohort_analysis = False
            # Demographics & Source Analytics (Core Package)
            self.enable_demographics_analytics = False
            self.enable_source_analytics = False
            # Behavioral Analytics
            self.enable_values_analytics = False
            self.enable_eco_friendly_score = False
            self.enable_premium_propensity = False
            self.enable_social_responsibility = False
            self.enable_product_category_analytics = False
            # Digital Marketing Analytics
            self.enable_social_commerce = False
            self.enable_utm_tracking = False
            self.enable_social_engagement = False
            self.enable_bnpl_analytics = False
            self.enable_mobile_commerce = False
            self.enable_device_preference = False
    
    @api.onchange('analytics_behavioral_enabled')
    def _onchange_analytics_behavioral_enabled(self):
        """When Behavioral Analytics is enabled/disabled, update related metrics"""
        if self.analytics_behavioral_enabled:
            # Enable core first
            self.analytics_core_enabled = True
            self._onchange_analytics_core_enabled()
            # Enable behavioral metrics
            self.enable_values_analytics = True
            self.enable_eco_friendly_score = True
            self.enable_premium_propensity = True
            self.enable_social_responsibility = True
            self.enable_product_category_analytics = True
        else:
            # If behavioral is disabled, disable commerce too
            self.analytics_commerce_enabled = False
            self.enable_values_analytics = False
            self.enable_eco_friendly_score = False
            self.enable_premium_propensity = False
            self.enable_social_responsibility = False
            self.enable_product_category_analytics = False
            self.enable_social_commerce = False
            self.enable_utm_tracking = False
            self.enable_social_engagement = False
            self.enable_bnpl_analytics = False
            self.enable_mobile_commerce = False
            self.enable_device_preference = False
    
    @api.onchange('analytics_commerce_enabled')
    def _onchange_analytics_commerce_enabled(self):
        """When Digital Marketing Analytics is enabled/disabled, update related metrics"""
        if self.analytics_commerce_enabled:
            # Enable behavioral first (which enables core)
            self.analytics_behavioral_enabled = True
            self._onchange_analytics_behavioral_enabled()
            # Enable commerce metrics
            self.enable_social_commerce = True
            self.enable_utm_tracking = True
            self.enable_social_engagement = True
            self.enable_bnpl_analytics = True
            self.enable_mobile_commerce = True
            self.enable_device_preference = True
        else:
            # Disable commerce metrics only
            self.enable_social_commerce = False
            self.enable_utm_tracking = False
            self.enable_social_engagement = False
            self.enable_bnpl_analytics = False
            self.enable_mobile_commerce = False
            self.enable_device_preference = False
    
    # =====================================
    # Analytics Package Methods
    # =====================================
    
    def action_enable_core_package(self):
        """Enable Core Analytics Package"""
        self.write({
            'analytics_core_enabled': True,
            'enable_engagement_scoring': True,
            'enable_email_engagement': True,
            'enable_whatsapp_engagement': True,
            'enable_website_engagement': True,
            'enable_customer_journey': True,
            'enable_churn_prediction': True,
            'enable_multichannel_behavior': True,
            'enable_cohort_analysis': True,
        })
        # Execute to save the configuration
        self.execute()
        # Show notification via bus
        show_notification(
            self.env,
            title="Core Analytics Enabled",
            message="Core Analytics Package has been activated with essential customer insights.",
            type="success",
        )
        # Return reload action to refresh the form
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.config.settings',
            'view_mode': 'form',
            'target': 'inline',
        }

    def action_enable_behavioral_package(self):
        """Enable Behavioral Analytics Package (includes Core)"""
        # Enable all core + behavioral settings
        self.write({
            'analytics_core_enabled': True,
            'enable_engagement_scoring': True,
            'enable_email_engagement': True,
            'enable_whatsapp_engagement': True,
            'enable_website_engagement': True,
            'enable_customer_journey': True,
            'enable_churn_prediction': True,
            'enable_multichannel_behavior': True,
            'enable_cohort_analysis': True,
            'analytics_behavioral_enabled': True,
            'enable_values_analytics': True,
            'enable_eco_friendly_score': True,
            'enable_premium_propensity': True,
            'enable_social_responsibility': True,
        })
        # Execute to save the configuration
        self.execute()
        # Show notification via bus
        show_notification(
            self.env,
            title="Behavioral Analytics Enabled",
            message="Behavioral Analytics Package activated with customer preference insights.",
            type="success",
        )
        # Return reload action to refresh the form
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.config.settings',
            'view_mode': 'form',
            'target': 'inline',
        }

    def action_enable_commerce_package(self):
        """Enable Digital Marketing Analytics Package (includes Core + Behavioral)"""
        # Enable all core + behavioral + commerce settings
        self.write({
            'analytics_core_enabled': True,
            'enable_engagement_scoring': True,
            'enable_email_engagement': True,
            'enable_whatsapp_engagement': True,
            'enable_website_engagement': True,
            'enable_customer_journey': True,
            'enable_churn_prediction': True,
            'enable_multichannel_behavior': True,
            'enable_cohort_analysis': True,
            'analytics_behavioral_enabled': True,
            'enable_values_analytics': True,
            'enable_eco_friendly_score': True,
            'enable_premium_propensity': True,
            'enable_social_responsibility': True,
            'analytics_commerce_enabled': True,
            'enable_social_commerce': True,
            'enable_utm_tracking': True,
            'enable_social_engagement': True,
            'enable_bnpl_analytics': True,
            'enable_mobile_commerce': True,
            'enable_device_preference': True,
        })
        # Execute to save the configuration
        self.execute()
        # Show notification via bus
        show_notification(
            self.env,
            title="Digital Marketing Analytics Enabled",
            message="Digital Marketing Analytics Package activated with social media tracking, campaign attribution, and mobile commerce insights.",
            type="success",
        )
        # Return reload action to refresh the form
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.config.settings',
            'view_mode': 'form',
            'target': 'inline',
        }

    def action_disable_all_optional(self):
        """Disable all optional analytics features"""
        self.write({
            'analytics_core_enabled': True,  # Keep core enabled
            'analytics_behavioral_enabled': False,
            'analytics_commerce_enabled': False,
            # Keep core analytics enabled
            'enable_engagement_scoring': True,
            'enable_email_engagement': True,
            'enable_whatsapp_engagement': True,
            'enable_website_engagement': True,
            'enable_customer_journey': True,
            'enable_churn_prediction': True,
            'enable_multichannel_behavior': True,
            'enable_cohort_analysis': True,
            # Keep core demographics & source analytics enabled
            'enable_demographics_analytics': True,
            'enable_source_analytics': True,
            # Disable behavioral analytics
            'enable_values_analytics': False,
            'enable_eco_friendly_score': False,
            'enable_premium_propensity': False,
            'enable_social_responsibility': False,
            'enable_product_category_analytics': False,
            # Disable commerce analytics
            'enable_social_commerce': False,
            'enable_utm_tracking': False,
            'enable_social_engagement': False,
            'enable_bnpl_analytics': False,
            'enable_mobile_commerce': False,
            'enable_device_preference': False,
        })
        # Execute to save the configuration
        self.execute()
        # Show notification via bus
        show_notification(
            self.env,
            title="Optional Features Disabled",
            message="Behavioral and Digital Marketing analytics disabled. Core analytics (RFM, Engagement, Journey, Churn) remain active.",
            type="info",
        )
        # Return reload action to refresh the form
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.config.settings',
            'view_mode': 'form',
            'target': 'inline',
        }

    # =====================================
    # Configuration Helpers
    # =====================================
    
    @api.model
    def get_whatsapp_config(self):
        """Get WhatsApp configuration values"""
        return {
            'base_url': self.env['ir.config_parameter'].sudo().get_param('wa_marketing_automation.whatsapp_base_url', 'http://localhost:8000'),
            'access_token': self.env['ir.config_parameter'].sudo().get_param('wa_marketing_automation.whatsapp_access_token', ''),
            'send_path_url': self.env['ir.config_parameter'].sudo().get_param('wa_marketing_automation.whatsapp_send_path_url', '/send-message'),
            'health_check_path_url': self.env['ir.config_parameter'].sudo().get_param('wa_marketing_automation.whatsapp_health_check_path_url', '/health'),
            'test_customer_id': int(self.env['ir.config_parameter'].sudo().get_param('wa_marketing_automation.whatsapp_test_customer_id', 0)) or False,
        }

    @api.model
    def _get_combined_keywords(self, keyword_strings):
        """Combine keywords from multiple field strings into a single list
        
        Args:
            keyword_strings: List of comma-separated keyword strings
        Returns: List of cleaned keywords
        """
        combined = []
        for keyword_string in keyword_strings:
            if keyword_string:
                keywords = [k.strip() for k in keyword_string.split(',') if k.strip()]
                combined.extend(keywords)
        return combined
    
    @api.model
    def _get_social_platform_keywords(self):
        """Get social platform keywords from individual fields
        
        Returns: {"platform": ["keyword1", "keyword2"]}
        """
        import json
        params = self.env['ir.config_parameter'].sudo()
        
        result = {
            'facebook': [k.strip() for k in params.get_param('wa_marketing_automation.facebook_keywords', 'facebook,fb').split(',') if k.strip()],
            'instagram': [k.strip() for k in params.get_param('wa_marketing_automation.instagram_keywords', 'instagram,ig').split(',') if k.strip()],
            'twitter': [k.strip() for k in params.get_param('wa_marketing_automation.twitter_keywords', 'twitter').split(',') if k.strip()],
            'linkedin': [k.strip() for k in params.get_param('wa_marketing_automation.linkedin_keywords', 'linkedin').split(',') if k.strip()],
            'tiktok': [k.strip() for k in params.get_param('wa_marketing_automation.tiktok_keywords', 'tiktok').split(',') if k.strip()],
            'youtube': [k.strip() for k in params.get_param('wa_marketing_automation.youtube_keywords', 'youtube').split(',') if k.strip()],
            'other': [k.strip() for k in params.get_param('wa_marketing_automation.other_social_keywords', 'social,share,referral').split(',') if k.strip()],
        }
        
        return json.dumps(result)
    
    @api.model
    def get_analytics_config(self):
        """Get analytics configuration values"""
        params = self.env['ir.config_parameter'].sudo()
        config = {
            # Feature toggles
            'enable_rfm_analysis': True,  # Always enabled
            'enable_engagement_scoring': params.get_param('wa_marketing_automation.enable_engagement_scoring', 'True') == 'True',
            'enable_customer_journey': params.get_param('wa_marketing_automation.enable_customer_journey', 'True') == 'True',
            'enable_churn_prediction': params.get_param('wa_marketing_automation.enable_churn_prediction', 'True') == 'True',
            'enable_multichannel_behavior': params.get_param('wa_marketing_automation.enable_multichannel_behavior', 'True') == 'True',
            'enable_values_analytics': params.get_param('wa_marketing_automation.enable_values_analytics', 'False') == 'True',
            'enable_social_commerce': params.get_param('wa_marketing_automation.enable_social_commerce', 'False') == 'True',
            'enable_bnpl_analytics': params.get_param('wa_marketing_automation.enable_bnpl_analytics', 'False') == 'True',
            'enable_mobile_commerce': params.get_param('wa_marketing_automation.enable_mobile_commerce', 'False') == 'True',
            'enable_email_engagement': params.get_param('wa_marketing_automation.enable_email_engagement', 'True') == 'True',
            'enable_website_engagement': params.get_param('wa_marketing_automation.enable_website_engagement', 'True') == 'True',
            'enable_whatsapp_engagement': params.get_param('wa_marketing_automation.enable_whatsapp_engagement', 'True') == 'True',
            # Demographics & Product Category Analytics
            'enable_demographics_analytics': params.get_param('wa_marketing_automation.enable_demographics_analytics', 'True') == 'True',
            'enable_source_analytics': params.get_param('wa_marketing_automation.enable_source_analytics', 'True') == 'True',
            'enable_product_category_analytics': params.get_param('wa_marketing_automation.enable_product_category_analytics', 'False') == 'True',
            
            # Keywords (combined from separate fields)
            'eco_friendly_keywords': self._get_combined_keywords([
                params.get_param('wa_marketing_automation.eco_keywords', 'eco,green'),
                params.get_param('wa_marketing_automation.organic_keywords', 'organic,bio'),
                params.get_param('wa_marketing_automation.sustainable_keywords', 'sustainable,natural'),
            ]),
            'social_responsibility_keywords': self._get_combined_keywords([
                params.get_param('wa_marketing_automation.fair_trade_keywords', 'fair,ethical'),
                params.get_param('wa_marketing_automation.charity_keywords', 'charity,community'),
                params.get_param('wa_marketing_automation.social_cause_keywords', 'social'),
            ]),
            'bnpl_keywords': self._get_combined_keywords([
                params.get_param('wa_marketing_automation.installment_keywords', 'installment,split'),
                params.get_param('wa_marketing_automation.bnpl_service_keywords', 'bnpl,klarna,afterpay'),
                params.get_param('wa_marketing_automation.payment_plan_keywords', 'sezzle,affirm'),
            ]),
            
            # Premium thresholds
            'premium_threshold_luxury': float(params.get_param('wa_marketing_automation.premium_threshold_luxury', '500.0')),
            'premium_threshold_premium': float(params.get_param('wa_marketing_automation.premium_threshold_premium', '200.0')),
            'premium_threshold_mid': float(params.get_param('wa_marketing_automation.premium_threshold_mid', '100.0')),
            'premium_threshold_budget_plus': float(params.get_param('wa_marketing_automation.premium_threshold_budget_plus', '50.0')),
            
            # Premium scores
            'premium_score_luxury': float(params.get_param('wa_marketing_automation.premium_score_luxury', '90.0')),
            'premium_score_premium': float(params.get_param('wa_marketing_automation.premium_score_premium', '70.0')),
            'premium_score_mid': float(params.get_param('wa_marketing_automation.premium_score_mid', '50.0')),
            'premium_score_budget_plus': float(params.get_param('wa_marketing_automation.premium_score_budget_plus', '30.0')),
            'premium_score_budget': float(params.get_param('wa_marketing_automation.premium_score_budget', '10.0')),
            
            # Loyalty bonuses
            'eco_friendly_loyalty_bonus': float(params.get_param('wa_marketing_automation.eco_friendly_loyalty_bonus', '1.2')),
            'premium_loyalty_bonus': float(params.get_param('wa_marketing_automation.premium_loyalty_bonus', '1.1')),
            'social_loyalty_bonus': float(params.get_param('wa_marketing_automation.social_loyalty_bonus', '1.2')),
            
            # Default values
            'values_default_score': float(params.get_param('wa_marketing_automation.values_default_score', '25.0')),
            
            # Time periods
            # 'rfm_analysis_period' removed - using 'rfm_analysis_period_days' instead
            'email_engagement_period': int(params.get_param('wa_marketing_automation.email_engagement_period', '90')),
            'website_engagement_period': int(params.get_param('wa_marketing_automation.website_engagement_period', '90')),
            
            # Engagement scoring
            'email_points_per_message': int(params.get_param('wa_marketing_automation.email_points_per_message', '5')),
            'website_points_per_order': int(params.get_param('wa_marketing_automation.website_points_per_order', '15')),
            'website_base_points': int(params.get_param('wa_marketing_automation.website_base_points', '20')),
            'website_historical_points': int(params.get_param('wa_marketing_automation.website_historical_points', '30')),
            'whatsapp_points_per_campaign': int(params.get_param('wa_marketing_automation.whatsapp_points_per_campaign', '10')),
            'whatsapp_base_points': int(params.get_param('wa_marketing_automation.whatsapp_base_points', '30')),
            
            # Engagement weights
            'email_engagement_weight': float(params.get_param('wa_marketing_automation.email_engagement_weight', '40.0')),
            'website_engagement_weight': float(params.get_param('wa_marketing_automation.website_engagement_weight', '35.0')),
            'whatsapp_engagement_weight': float(params.get_param('wa_marketing_automation.whatsapp_engagement_weight', '25.0')),
            
            # Churn prediction weights
            'churn_rfm_weight': float(params.get_param('wa_marketing_automation.churn_rfm_weight', '40.0')),
            'churn_engagement_weight': float(params.get_param('wa_marketing_automation.churn_engagement_weight', '30.0')),
            'churn_journey_weight': float(params.get_param('wa_marketing_automation.churn_journey_weight', '20.0')),
            'churn_multichannel_weight': float(params.get_param('wa_marketing_automation.churn_multichannel_weight', '10.0')),
            
            # Churn risk thresholds
            'churn_risk_very_high_threshold': float(params.get_param('wa_marketing_automation.churn_risk_very_high_threshold', '81.0')),
            'churn_risk_high_threshold': float(params.get_param('wa_marketing_automation.churn_risk_high_threshold', '61.0')),
            'churn_risk_medium_threshold': float(params.get_param('wa_marketing_automation.churn_risk_medium_threshold', '41.0')),
            'churn_risk_low_threshold': float(params.get_param('wa_marketing_automation.churn_risk_low_threshold', '21.0')),
            
            # Churn risk factors
            'churn_recency_365_risk': float(params.get_param('wa_marketing_automation.churn_recency_365_risk', '100.0')),
            'churn_recency_180_risk': float(params.get_param('wa_marketing_automation.churn_recency_180_risk', '65.0')),
            'churn_recency_90_risk': float(params.get_param('wa_marketing_automation.churn_recency_90_risk', '35.0')),
            'churn_engagement_20_risk': float(params.get_param('wa_marketing_automation.churn_engagement_20_risk', '100.0')),
            'churn_engagement_40_risk': float(params.get_param('wa_marketing_automation.churn_engagement_40_risk', '75.0')),
            'churn_engagement_60_risk': float(params.get_param('wa_marketing_automation.churn_engagement_60_risk', '50.0')),
            'churn_multichannel_1_risk': float(params.get_param('wa_marketing_automation.churn_multichannel_1_risk', '80.0')),
            'churn_multichannel_30_risk': float(params.get_param('wa_marketing_automation.churn_multichannel_30_risk', '60.0')),
            'churn_multichannel_60_risk': float(params.get_param('wa_marketing_automation.churn_multichannel_60_risk', '30.0')),
            
            # RFM risk scores
            'churn_rfm_lost_hibernating_risk': float(params.get_param('wa_marketing_automation.churn_rfm_lost_hibernating_risk', '100.0')),
            'churn_rfm_at_risk_risk': float(params.get_param('wa_marketing_automation.churn_rfm_at_risk_risk', '75.0')),
            'churn_rfm_need_attention_risk': float(params.get_param('wa_marketing_automation.churn_rfm_need_attention_risk', '50.0')),
            'churn_rfm_new_customers_risk': float(params.get_param('wa_marketing_automation.churn_rfm_new_customers_risk', '25.0')),
            
            # Journey stage risk scores
            'churn_journey_dormant_risk': float(params.get_param('wa_marketing_automation.churn_journey_dormant_risk', '100.0')),
            'churn_journey_consideration_risk': float(params.get_param('wa_marketing_automation.churn_journey_consideration_risk', '50.0')),
            
            # Mobile commerce
            'mobile_order_threshold': float(params.get_param('wa_marketing_automation.mobile_order_threshold', '200.0')),
            'mobile_hour_start': int(params.get_param('wa_marketing_automation.mobile_hour_start', '9')),
            'mobile_hour_end': int(params.get_param('wa_marketing_automation.mobile_hour_end', '18')),
            'mobile_device_preference_threshold': float(params.get_param('wa_marketing_automation.mobile_device_preference_threshold', '1.5')),
            'mobile_conversion_rate_multiplier': float(params.get_param('wa_marketing_automation.mobile_conversion_rate_multiplier', '0.9')),
            'mobile_default_score': float(params.get_param('wa_marketing_automation.mobile_default_score', '50.0')),
            
            # Social commerce
            'social_conversion_rate_multiplier': float(params.get_param('wa_marketing_automation.social_conversion_rate_multiplier', '0.8')),
            'social_platform_keywords': self._get_social_platform_keywords(),
            
            # BNPL thresholds
            'bnpl_rarely_threshold': int(params.get_param('wa_marketing_automation.bnpl_rarely_threshold', '2')),
            'bnpl_sometimes_threshold': int(params.get_param('wa_marketing_automation.bnpl_sometimes_threshold', '5')),
            'bnpl_frequently_threshold': int(params.get_param('wa_marketing_automation.bnpl_frequently_threshold', '10')),
            
            # Multichannel scores
            'multichannel_3plus_score': float(params.get_param('wa_marketing_automation.multichannel_3plus_score', '85.0')),
            'multichannel_2_score': float(params.get_param('wa_marketing_automation.multichannel_2_score', '60.0')),
            'multichannel_1_score': float(params.get_param('wa_marketing_automation.multichannel_1_score', '30.0')),
            
            # Engagement thresholds
            'engagement_very_high_threshold': float(params.get_param('wa_marketing_automation.engagement_very_high_threshold', '81.0')),
            'engagement_high_threshold': float(params.get_param('wa_marketing_automation.engagement_high_threshold', '61.0')),
            'engagement_medium_threshold': float(params.get_param('wa_marketing_automation.engagement_medium_threshold', '41.0')),
            'engagement_low_threshold': float(params.get_param('wa_marketing_automation.engagement_low_threshold', '21.0')),
            
            # RFM quintiles
            'rfm_quintile_1': float(params.get_param('wa_marketing_automation.rfm_quintile_1', '0.2')),
            'rfm_quintile_2': float(params.get_param('wa_marketing_automation.rfm_quintile_2', '0.4')),
            'rfm_quintile_3': float(params.get_param('wa_marketing_automation.rfm_quintile_3', '0.6')),
            'rfm_quintile_4': float(params.get_param('wa_marketing_automation.rfm_quintile_4', '0.8')),
            
            # =========================================================
            # Demographics & Product Category Advanced Configuration
            # =========================================================
            
            # Age and Customer Validation
            'age_validation_limit': int(params.get_param('wa_marketing_automation.age_validation_limit', '150')),
            'new_customer_threshold': int(params.get_param('wa_marketing_automation.new_customer_threshold', '1')),
            
            # Analysis Time Periods
            'rfm_analysis_period_days': int(params.get_param('wa_marketing_automation.rfm_analysis_period_days', '365')),
            'category_analysis_period_days': int(params.get_param('wa_marketing_automation.category_analysis_period_days', '180')),
            
            # Product Category Analytics Configuration
            'max_reasonable_categories': int(params.get_param('wa_marketing_automation.max_reasonable_categories', '20')),
            'category_change_positive_threshold': float(params.get_param('wa_marketing_automation.category_change_positive_threshold', '20.0')),
            'category_change_negative_threshold': float(params.get_param('wa_marketing_automation.category_change_negative_threshold', '20.0')),
            
            # Diversity Score Thresholds
            'diversity_score_high_threshold': float(params.get_param('wa_marketing_automation.diversity_score_high_threshold', '70.0')),
            'diversity_score_medium_threshold': float(params.get_param('wa_marketing_automation.diversity_score_medium_threshold', '40.0')),
            
            # Category Ranking Weights
            'category_spending_weight': float(params.get_param('wa_marketing_automation.category_spending_weight', '0.7')),
            'category_frequency_weight': float(params.get_param('wa_marketing_automation.category_frequency_weight', '0.3')),
            
            # Values Preference Detection Thresholds
            'values_strong_preference_threshold': float(params.get_param('wa_marketing_automation.values_strong_preference_threshold', '50.0')),
            'values_targeting_threshold': float(params.get_param('wa_marketing_automation.values_targeting_threshold', '30.0')),
        }
        
        return config

    # =====================================
    # Validation
    # =====================================
    
    @api.constrains('whatsapp_base_url')
    def _check_whatsapp_base_url(self):
        """Validate WhatsApp API base URL format"""
        for record in self:
            if record.whatsapp_base_url and not record.whatsapp_base_url.startswith(('http://', 'https://')):
                raise ValidationError(_("WhatsApp Base API URL must start with http:// or https://"))
                
    @api.constrains('age_validation_limit', 'new_customer_threshold', 'rfm_analysis_period_days', 'category_analysis_period_days', 'max_reasonable_categories', 'values_strong_preference_threshold', 'values_targeting_threshold')
    def _check_positive_values(self):
        """Validate that numeric parameters are positive and reasonable"""
        for record in self:
            if record.age_validation_limit and (record.age_validation_limit < 50 or record.age_validation_limit > 200):
                raise ValidationError(_("Age validation limit must be between 50 and 200 years"))
                
            if record.new_customer_threshold and record.new_customer_threshold < 1:
                raise ValidationError(_("New customer threshold must be at least 1 order"))
                
            if record.rfm_analysis_period_days and (record.rfm_analysis_period_days < 30 or record.rfm_analysis_period_days > 1095):
                raise ValidationError(_("RFM analysis period must be between 30 and 1095 days (3 years)"))
                
            if record.category_analysis_period_days and (record.category_analysis_period_days < 30 or record.category_analysis_period_days > 730):
                raise ValidationError(_("Category analysis period must be between 30 and 730 days (2 years)"))
                
            if record.max_reasonable_categories and (record.max_reasonable_categories < 5 or record.max_reasonable_categories > 100):
                raise ValidationError(_("Maximum reasonable categories must be between 5 and 100"))
                
            if record.values_strong_preference_threshold and (record.values_strong_preference_threshold < 10.0 or record.values_strong_preference_threshold > 90.0):
                raise ValidationError(_("Strong preference threshold must be between 10% and 90%"))
                
            if record.values_targeting_threshold and (record.values_targeting_threshold < 5.0 or record.values_targeting_threshold > 80.0):
                raise ValidationError(_("Targeting threshold must be between 5% and 80%"))
                
    @api.constrains('category_change_positive_threshold', 'category_change_negative_threshold')
    def _check_change_thresholds(self):
        """Validate change detection thresholds are reasonable percentages"""
        for record in self:
            if record.category_change_positive_threshold and (record.category_change_positive_threshold < 5.0 or record.category_change_positive_threshold > 100.0):
                raise ValidationError(_("Category change positive threshold must be between 5% and 100%"))
                
            if record.category_change_negative_threshold and (record.category_change_negative_threshold < 5.0 or record.category_change_negative_threshold > 100.0):
                raise ValidationError(_("Category change negative threshold must be between 5% and 100%"))
                
    @api.constrains('diversity_score_high_threshold', 'diversity_score_medium_threshold')
    def _check_diversity_thresholds(self):
        """Validate diversity score thresholds are logical and within range"""
        for record in self:
            if record.diversity_score_high_threshold and (record.diversity_score_high_threshold < 0.0 or record.diversity_score_high_threshold > 100.0):
                raise ValidationError(_("High diversity score threshold must be between 0 and 100"))
                
            if record.diversity_score_medium_threshold and (record.diversity_score_medium_threshold < 0.0 or record.diversity_score_medium_threshold > 100.0):
                raise ValidationError(_("Medium diversity score threshold must be between 0 and 100"))
                
            if (record.diversity_score_high_threshold and record.diversity_score_medium_threshold and 
                record.diversity_score_high_threshold <= record.diversity_score_medium_threshold):
                raise ValidationError(_("High diversity threshold must be greater than medium diversity threshold"))
                
    @api.constrains('category_spending_weight', 'category_frequency_weight')
    def _check_category_weights(self):
        """Validate category ranking weights sum to 1.0"""
        for record in self:
            if record.category_spending_weight is not False and record.category_frequency_weight is not False:
                total_weight = record.category_spending_weight + record.category_frequency_weight
                if abs(total_weight - 1.0) > 0.001:  # Allow small floating point precision errors
                    raise ValidationError(_("Category spending weight and frequency weight must sum to 1.0 (currently: %.3f)") % total_weight)
                    
            if record.category_spending_weight and (record.category_spending_weight < 0.0 or record.category_spending_weight > 1.0):
                raise ValidationError(_("Category spending weight must be between 0.0 and 1.0"))
                
            if record.category_frequency_weight and (record.category_frequency_weight < 0.0 or record.category_frequency_weight > 1.0):
                raise ValidationError(_("Category frequency weight must be between 0.0 and 1.0"))