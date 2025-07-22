# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CustomerSpendingTierConfig(models.Model):
    """
    Customer Spending Tier Configuration
    
    This model manages configurable spending-based customer tiers for business analytics.
    Allows dynamic tier management without code changes for future business flexibility.
    """
    _name = 'wa_marketing_automation.customer_spending_tier_config'
    _description = 'Customer Spending Tier Configuration - Spending Amount Based Tiers'
    _order = 'min_spending_amount desc'  # Sort by spending (highest first)
    _rec_name = 'display_name'

    # Core tier identification
    tier_code = fields.Char(
        string='Tier Code', 
        required=True, 
        size=256,
        help='Short code for this spending tier (e.g., VIP, Premium, Gold, Silver)'
    )
    
    display_name = fields.Char(
        string='Tier Name', 
        required=True, 
        help='Descriptive name for this spending tier (e.g., Premium, High Value)'
    )
    
    # Spending amount thresholds (in IDR)
    min_spending_amount = fields.Float(
        string='Minimum Spending Amount (IDR)', 
        required=True,
        help='Minimum total customer spending to qualify for this tier'
    )
    
    max_spending_amount = fields.Float(
        string='Maximum Spending Amount (IDR)', 
        default=False,  # False = NULL in Odoo, prevents 0.0 default for unlimited tiers
        help='Maximum total customer spending for this tier (leave empty for highest tier)'
    )
    
    # Visual and organizational
    tier_color = fields.Char(
        string='Tier Color', 
        default='#007bff', 
        help='Hex color code for UI display (e.g., #007bff)'
    )
    
    tier_description = fields.Text(
        string='Tier Description',
        help='Detailed description of this customer spending tier'
    )
    
    # Management fields
    active = fields.Boolean(
        string='Active', 
        default=True,
        help='Whether this spending tier is currently active'
    )
    
    sequence = fields.Integer(
        string='Display Sequence', 
        default=10,
        help='Order for displaying tiers (lower numbers appear first)'
    )
    
    # Computed fields for business insights  
    customer_count = fields.Integer(
        string='Customer Count',
        compute='_compute_tier_analytics',
        store=False,
        help='Number of customers currently in this spending tier'
    )
    
    total_tier_revenue = fields.Float(
        string='Total Tier Revenue',
        compute='_compute_tier_analytics', 
        store=False,
        help='Total revenue from customers in this spending tier'
    )
    
    average_spending = fields.Float(
        string='Average Customer Spending',
        compute='_compute_tier_analytics',
        store=False,
        help='Average spending per customer in this tier'
    )

    @api.constrains('min_spending_amount', 'max_spending_amount')
    def _check_spending_tier_ranges(self):
        """Ensure customer spending tier ranges are valid and don't overlap"""
        for tier in self:
            # Validate min/max relationship
            if tier.max_spending_amount and tier.min_spending_amount >= tier.max_spending_amount:
                raise ValidationError(
                    f"Minimum spending amount ({tier.min_spending_amount:,.0f} IDR) "
                    f"must be less than maximum spending amount ({tier.max_spending_amount:,.0f} IDR) "
                    f"for spending tier '{tier.tier_code}'"
                )
            
            # Check for overlaps with other active spending tiers
            domain = [
                ('id', '!=', tier.id),
                ('active', '=', True),
            ]
            
            # Build overlap detection conditions
            if tier.max_spending_amount:
                # This tier has a max, check for overlaps
                overlap_domain = [
                    '|',
                    '&', ('min_spending_amount', '<=', tier.min_spending_amount),
                         '|', ('max_spending_amount', '>=', tier.min_spending_amount),
                              ('max_spending_amount', '=', False),
                    '&', ('min_spending_amount', '<=', tier.max_spending_amount),
                         '|', ('max_spending_amount', '>=', tier.max_spending_amount),
                              ('max_spending_amount', '=', False)
                ]
            else:
                # This tier has no max (highest tier), check for overlaps
                overlap_domain = [
                    ('min_spending_amount', '>=', tier.min_spending_amount)
                ]
            
            overlapping_tiers = self.search(domain + overlap_domain)
            if overlapping_tiers:
                raise ValidationError(
                    f"Customer spending tier '{tier.tier_code}' overlaps with "
                    f"existing tier '{overlapping_tiers[0].tier_code}'. "
                    f"Please adjust the spending amount ranges to avoid conflicts."
                )

    @api.constrains('tier_code')
    def _check_unique_tier_code(self):
        """Ensure tier codes are unique among active tiers"""
        for tier in self:
            if tier.active:
                existing_tier = self.search([
                    ('id', '!=', tier.id),
                    ('tier_code', '=', tier.tier_code),
                    ('active', '=', True)
                ])
                if existing_tier:
                    raise ValidationError(
                        f"Tier code '{tier.tier_code}' is already used by another active spending tier. "
                        f"Please use a different tier code."
                    )

    def _compute_tier_analytics(self):
        """Compute analytics for each spending tier"""
        for tier in self:
            # Get all customers and filter by spending amount ranges
            # This is more reliable than depending on computed customer_spending_tier field
            domain = [
                ('is_company', '=', False),
                ('customer_rank', '>', 0),
                ('total_spent', '>=', tier.min_spending_amount)
            ]
            
            # Add max spending condition if tier has upper limit
            if tier.max_spending_amount:
                domain.append(('total_spent', '<=', tier.max_spending_amount))
            
            customers = self.env['res.partner'].search(domain)
            
            tier.customer_count = len(customers)
            tier.total_tier_revenue = sum(customers.mapped('total_spent')) if customers else 0.0
            tier.average_spending = tier.total_tier_revenue / tier.customer_count if tier.customer_count > 0 else 0.0

    @api.onchange('min_spending_amount', 'max_spending_amount')
    def _onchange_spending_amounts(self):
        """Auto-refresh analytics when spending amounts change"""
        if self.min_spending_amount is not False or self.max_spending_amount is not False:
            self._compute_tier_analytics()

    @api.model
    def get_spending_tier_for_amount(self, spending_amount):
        """
        Get appropriate customer spending tier for a given spending amount
        
        Args:
            spending_amount (float): Total customer spending amount in IDR
            
        Returns:
            str: Tier code for the appropriate spending tier, or 'UNCLASSIFIED'
        """
        if spending_amount < 0:
            _logger.warning(f"Negative spending amount received: {spending_amount}")
            return 'UNCLASSIFIED'
        
        # Find matching active tier
        domain = [
            ('active', '=', True),
            ('min_spending_amount', '<=', spending_amount),
        ]
        
        # Add max amount condition (None means no upper limit)
        tier = self.search(domain + [
            '|', 
            ('max_spending_amount', '>=', spending_amount), 
            ('max_spending_amount', '=', False)
        ], limit=1)
        
        if tier:
            _logger.debug(f"Spending amount {spending_amount:,.0f} IDR classified as tier '{tier.tier_code}'")
            return tier.tier_code
        else:
            _logger.warning(f"No spending tier found for amount {spending_amount:,.0f} IDR")
            return 'UNCLASSIFIED'

    @api.model  
    def get_spending_tier_selection_options(self):
        """
        Generate dynamic selection options for customer spending tier field
        
        Returns:
            list: List of tuples (tier_code, display_label) for selection field
        """
        active_tiers = self.search([('active', '=', True)], order='sequence, min_spending_amount desc')
        options = [(tier.tier_code, f"{tier.tier_code}: {tier.display_name}") for tier in active_tiers]
        
        # Always include UNCLASSIFIED option
        options.append(('UNCLASSIFIED', 'Unclassified'))
        
        _logger.debug(f"Generated {len(options)} spending tier selection options")
        return options


    def action_refresh_tier_analytics(self):
        """Manually refresh tier analytics"""
        self._compute_tier_analytics()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'title': 'Analytics Refreshed',
                'message': f'Spending tier analytics have been refreshed successfully.',
            }
        }

    def _recompute_all_partner_spending_tiers(self):
        """Recompute spending tiers for all customers"""
        customers = self.env['res.partner'].search([
            ('is_company', '=', False),
            ('customer_rank', '>', 0)
        ])
        if customers:
            _logger.info(f"Recomputing spending tiers for {len(customers)} customers")
            customers._compute_customer_spending_tier()
            _logger.info("Spending tier recomputation completed")

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to trigger partner recomputation (batch-aware)"""
        records = super().create(vals_list)
        # Recompute partner spending tiers when new tier config is created
        if records:
            records[0]._recompute_all_partner_spending_tiers()  # Only call once for batch
        return records

    def write(self, vals):
        """Override write to trigger partner recomputation when tier ranges change"""
        # Check if tier-related fields are being modified
        tier_fields = {'min_spending_amount', 'max_spending_amount', 'active', 'tier_code'}
        if any(field in vals for field in tier_fields):
            result = super().write(vals)
            # Recompute partner spending tiers when tier configuration changes
            self._recompute_all_partner_spending_tiers()
            return result
        else:
            return super().write(vals)

    def unlink(self):
        """Override unlink to trigger partner recomputation when tiers are deleted"""
        result = super().unlink()
        # Recompute partner spending tiers when tier config is deleted
        if self.env['res.partner']:
            self.env['res.partner'].search([
                ('is_company', '=', False),
                ('customer_rank', '>', 0)
            ])._compute_customer_spending_tier()
        return result

    def name_get(self):
        """Custom name display for better UX"""
        context = self._context
        result = []
        for tier in self:
            # Check if we want the compact format (for pivot tables)
            if context.get('show_spending_range', False):
                if tier.max_spending_amount:
                    name = f"{tier.display_name} (Rp {tier.min_spending_amount:,.0f} - {tier.max_spending_amount:,.0f})"
                else:
                    name = f"{tier.display_name} (> Rp {tier.min_spending_amount:,.0f})"
            else:
                # Default format
                name = f"{tier.tier_code}: {tier.display_name}"
                if tier.max_spending_amount:
                    name += f" (Rp {tier.min_spending_amount:,.0f} - {tier.max_spending_amount:,.0f})"
                else:
                    name += f" (> Rp {tier.min_spending_amount:,.0f})"
            result.append((tier.id, name))
        return result