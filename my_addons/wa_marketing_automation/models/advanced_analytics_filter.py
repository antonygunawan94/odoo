from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class AdvancedAnalyticsFilter(models.TransientModel):
    _name = 'wa_marketing_automation.advanced_filter'
    _description = 'Advanced Analytics Filter for Customer Targeting'

    name = fields.Char(
        string='Filter Name',
        help='Give your filter a descriptive name'
    )

    # RFM Filters
    rfm_segments = fields.Char(
        string='RFM Segments',
        help='Select specific RFM customer segments (comma-separated)'
    )
    rfm_score_min = fields.Integer(
        string='Min RFM Score',
        default=0,
        help='Minimum combined RFM score (3-15)'
    )
    rfm_score_max = fields.Integer(
        string='Max RFM Score',
        default=15,
        help='Maximum combined RFM score (3-15)'
    )

    # Engagement Filters
    engagement_levels = fields.Char(
        string='Engagement Levels',
        help='Select engagement level classifications (comma-separated)'
    )
    engagement_score_min = fields.Float(
        string='Min Engagement Score',
        default=0.0,
        help='Minimum overall engagement score (0-100)'
    )
    engagement_score_max = fields.Float(
        string='Max Engagement Score',
        default=100.0,
        help='Maximum overall engagement score (0-100)'
    )

    # Churn Risk Filters
    churn_risk_levels = fields.Char(
        string='Churn Risk Levels',
        help='Select churn risk classifications (comma-separated)'
    )
    churn_score_min = fields.Float(
        string='Min Churn Score',
        default=0.0,
        help='Minimum churn risk score (0-100)'
    )
    churn_score_max = fields.Float(
        string='Max Churn Score',
        default=100.0,
        help='Maximum churn risk score (0-100)'
    )

    # Customer Journey Filters
    journey_stages = fields.Char(
        string='Journey Stages',
        help='Select customer journey stages (comma-separated)'
    )

    # Age and Demographics
    age_min = fields.Integer(
        string='Min Age',
        help='Minimum customer age'
    )
    age_max = fields.Integer(
        string='Max Age',
        help='Maximum customer age'
    )

    # Purchase Behavior
    days_since_purchase_min = fields.Integer(
        string='Min Days Since Purchase',
        help='Minimum days since last purchase'
    )
    days_since_purchase_max = fields.Integer(
        string='Max Days Since Purchase',
        help='Maximum days since last purchase'
    )
    purchase_count_min = fields.Integer(
        string='Min Purchase Count',
        help='Minimum number of purchases'
    )
    total_spent_min = fields.Float(
        string='Min Total Spent',
        help='Minimum total amount spent'
    )
    total_spent_max = fields.Float(
        string='Max Total Spent',
        help='Maximum total amount spent'
    )

    # Social Commerce Filters (if enabled)
    social_media_sources = fields.Char(
        string='Social Media Sources',
        help='Select social media sources (comma-separated: facebook,instagram,twitter,linkedin,tiktok,youtube,other,none)'
    )
    social_engagement_min = fields.Float(
        string='Min Social Engagement',
        help='Minimum social engagement score (0-100)'
    )

    # Values-Driven Filters (if enabled)
    sustainability_score_min = fields.Float(
        string='Min Sustainability Score',
        help='Minimum sustainability preference score (0-100)'
    )
    premium_propensity_min = fields.Float(
        string='Min Premium Propensity',
        help='Minimum premium product propensity (0-100)'
    )
    social_responsibility_min = fields.Float(
        string='Min Social Responsibility',
        help='Minimum social responsibility score (0-100)'
    )

    # BNPL and Mobile Filters (if enabled)
    bnpl_usage_frequencies = fields.Char(
        string='BNPL Usage Frequencies',
        help='Select BNPL usage patterns (comma-separated: never,rarely,sometimes,frequently,always)'
    )
    mobile_commerce_score_min = fields.Float(
        string='Min Mobile Commerce Score',
        help='Minimum mobile commerce score (0-100)'
    )
    device_preferences = fields.Char(
        string='Device Preferences',
        help='Select preferred device types (comma-separated: smartphone,tablet,desktop,mixed,unknown)'
    )

    # Multi-Channel Behavior
    touchpoints_min = fields.Integer(
        string='Min Touchpoints',
        help='Minimum number of channel touchpoints'
    )
    consistency_score_min = fields.Float(
        string='Min Consistency Score',
        help='Minimum multi-channel consistency score (0-100)'
    )

    # Output Options
    create_segment = fields.Boolean(
        string='Create Segment',
        default=True,
        help='Create a customer segment with these filters'
    )
    segment_name = fields.Char(
        string='Segment Name',
        help='Name for the new customer segment'
    )

    # Results
    customer_count = fields.Integer(
        string='Matching Customers',
        readonly=True,
        help='Number of customers matching the criteria'
    )
    filter_domain = fields.Text(
        string='Filter Domain',
        readonly=True,
        help='Generated domain filter for technical reference'
    )

    @api.onchange('name')
    def _onchange_name(self):
        if self.name and not self.segment_name:
            self.segment_name = f"Segment: {self.name}"

    def action_preview_customers(self):
        """Preview customers matching the filter criteria"""
        domain = self._build_domain()
        
        # Get metrics configuration to show only relevant filters
        config = self.env['wa_marketing_automation.config.settings'].get_analytics_config()
        
        # Update customer count
        customers = self.env['res.partner'].search(domain)
        self.customer_count = len(customers)
        self.filter_domain = str(domain)
        
        # Show preview
        return {
            'type': 'ir.actions.act_window',
            'name': f'Preview: {self.name or "Filtered Customers"}',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'search_default_customer': 1,
                'default_is_company': False,
            },
            'target': 'current',
        }

    def action_apply_filter(self):
        """Apply filter and optionally create segment"""
        domain = self._build_domain()
        customers = self.env['res.partner'].search(domain)
        
        result_action = {
            'type': 'ir.actions.act_window',
            'name': f'Filtered Customers: {self.name or "Advanced Filter"}',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'search_default_customer': 1,
                'default_is_company': False,
            },
            'target': 'current',
        }
        
        if self.create_segment and self.segment_name:
            # Create customer segment
            segment_vals = {
                'name': self.segment_name,
                'segmentation_type': 'rule_based',
                'domain': str(domain),
                'description': f'Advanced filter: {self.name}\nMatching customers: {len(customers)}',
            }
            
            segment = self.env['wa_marketing_automation.customer_segmentation'].create(segment_vals)
            
            # Add customers to segment
            segment.write({'selected_customers': [(6, 0, customers.ids)]})
            
            # Show success message and redirect to segment
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'title': 'Segment Created Successfully',
                    'message': f'Created segment "{self.segment_name}" with {len(customers)} customers',
                    'next': {
                        'type': 'ir.actions.act_window',
                        'res_model': 'wa_marketing_automation.customer_segmentation',
                        'res_id': segment.id,
                        'view_mode': 'form',
                        'target': 'current',
                    }
                }
            }
        
        return result_action

    def _build_domain(self):
        """Build domain filter based on selected criteria"""
        domain = [('customer_rank', '>', 0), ('is_company', '=', False)]
        
        # Get metrics configuration to filter only enabled metrics
        config = self.env['wa_marketing_automation.config.settings'].get_analytics_config()
        
        # RFM Filters (always available)
        if self.rfm_segments:
            segments = [seg.strip() for seg in self.rfm_segments.split(',') if seg.strip()]
            if segments:
                domain.append(('rfm_segment', 'in', segments))
        
        if self.rfm_score_min > 0:
            domain.append(('rfm_score', '>=', self.rfm_score_min))
        if self.rfm_score_max < 15:
            domain.append(('rfm_score', '<=', self.rfm_score_max))

        # Engagement Filters (if enabled)
        if config.get('enable_engagement_scoring', True):
            if self.engagement_levels:
                levels = [level.strip() for level in self.engagement_levels.split(',') if level.strip()]
                if levels:
                    domain.append(('engagement_level', 'in', levels))
            
            if self.engagement_score_min > 0:
                domain.append(('overall_engagement_score', '>=', self.engagement_score_min))
            if self.engagement_score_max < 100:
                domain.append(('overall_engagement_score', '<=', self.engagement_score_max))

        # Churn Risk Filters (if enabled)
        if config.get('enable_churn_prediction', True):
            if self.churn_risk_levels:
                levels = [level.strip() for level in self.churn_risk_levels.split(',') if level.strip()]
                if levels:
                    domain.append(('churn_risk_level', 'in', levels))
            
            if self.churn_score_min > 0:
                domain.append(('churn_risk_score', '>=', self.churn_score_min))
            if self.churn_score_max < 100:
                domain.append(('churn_risk_score', '<=', self.churn_score_max))

        # Customer Journey Filters (if enabled)
        if config.get('enable_customer_journey', True) and self.journey_stages:
            stages = [stage.strip() for stage in self.journey_stages.split(',') if stage.strip()]
            if stages:
                domain.append(('customer_journey_stage', 'in', stages))

        # Age and Demographics
        if self.age_min:
            domain.append(('age', '>=', self.age_min))
        if self.age_max:
            domain.append(('age', '<=', self.age_max))

        # Purchase Behavior
        if self.days_since_purchase_min:
            domain.append(('days_since_last_purchase', '>=', self.days_since_purchase_min))
        if self.days_since_purchase_max:
            domain.append(('days_since_last_purchase', '<=', self.days_since_purchase_max))
        if self.purchase_count_min:
            domain.append(('purchase_count', '>=', self.purchase_count_min))
        if self.total_spent_min:
            domain.append(('total_spent', '>=', self.total_spent_min))
        if self.total_spent_max:
            domain.append(('total_spent', '<=', self.total_spent_max))

        # Social Commerce Filters (if enabled)
        if config.get('enable_social_commerce', False):
            if self.social_media_sources:
                sources = [src.strip() for src in self.social_media_sources.split(',') if src.strip()]
                if sources:
                    domain.append(('social_media_source', 'in', sources))
            if self.social_engagement_min:
                domain.append(('social_engagement_score', '>=', self.social_engagement_min))

        # Values-Driven Filters (if enabled)
        if config.get('enable_values_analytics', False):
            if self.sustainability_score_min:
                domain.append(('sustainability_preference_score', '>=', self.sustainability_score_min))
            if self.premium_propensity_min:
                domain.append(('premium_product_propensity', '>=', self.premium_propensity_min))
            if self.social_responsibility_min:
                domain.append(('social_responsibility_score', '>=', self.social_responsibility_min))

        # BNPL and Mobile Filters (if enabled)
        if config.get('enable_bnpl_analytics', False) and self.bnpl_usage_frequencies:
            frequencies = [freq.strip() for freq in self.bnpl_usage_frequencies.split(',') if freq.strip()]
            if frequencies:
                domain.append(('bnpl_usage_frequency', 'in', frequencies))
        
        if config.get('enable_mobile_commerce', False):
            if self.mobile_commerce_score_min:
                domain.append(('mobile_commerce_score', '>=', self.mobile_commerce_score_min))
            if self.device_preferences:
                prefs = [pref.strip() for pref in self.device_preferences.split(',') if pref.strip()]
                if prefs:
                    domain.append(('mobile_device_preference', 'in', prefs))

        # Multi-Channel Behavior (if enabled)
        if config.get('enable_multichannel_behavior', True):
            if self.touchpoints_min:
                domain.append(('multichannel_touchpoints', '>=', self.touchpoints_min))
            if self.consistency_score_min:
                domain.append(('multichannel_consistency_score', '>=', self.consistency_score_min))

        return domain

    def action_save_template(self):
        """Save filter as a reusable template"""
        template_vals = {
            'name': f"Template: {self.name}",
            'template_data': self._get_template_data(),
            'description': f'Advanced filter template created from: {self.name}',
        }
        
        template = self.env['wa_marketing_automation.filter_template'].create(template_vals)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'title': 'Template Saved',
                'message': f'Filter template "{template.name}" has been saved for reuse',
            }
        }

    def _get_template_data(self):
        """Get filter data for template saving"""
        return {
            'rfm_segments': self.rfm_segments.ids,
            'rfm_score_min': self.rfm_score_min,
            'rfm_score_max': self.rfm_score_max,
            'engagement_levels': self.engagement_levels.ids,
            'engagement_score_min': self.engagement_score_min,
            'engagement_score_max': self.engagement_score_max,
            'churn_risk_levels': self.churn_risk_levels.ids,
            'churn_score_min': self.churn_score_min,
            'churn_score_max': self.churn_score_max,
            'age_min': self.age_min,
            'age_max': self.age_max,
            'total_spent_min': self.total_spent_min,
            'total_spent_max': self.total_spent_max,
        }


class AdvancedFilterTemplate(models.Model):
    _name = 'wa_marketing_automation.filter_template'
    _description = 'Advanced Filter Templates'
    _order = 'name'

    name = fields.Char(
        string='Template Name',
        required=True
    )
    description = fields.Text(
        string='Description'
    )
    template_data = fields.Text(
        string='Template Data',
        help='Serialized filter configuration'
    )
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help='Number of times this template has been used'
    )

    def action_use_template(self):
        """Create new filter wizard with template data"""
        template_data = safe_eval(self.template_data) if self.template_data else {}
        
        # Increment usage count
        self.usage_count += 1
        
        # Create new filter wizard with template values
        wizard = self.env['wa_marketing_automation.advanced_filter'].create({
            'name': f"From template: {self.name}",
            **template_data
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Advanced Analytics Filter',
            'res_model': 'wa_marketing_automation.advanced_filter',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }