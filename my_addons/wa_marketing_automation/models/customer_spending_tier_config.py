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

    @api.model
    def create_default_indonesian_spending_tiers(self):
        """
        Create default Indonesian beauty clinic customer spending tiers
        Based on client's requirements from MARKETING REPORT MEI 2025 KUDUS 2
        """
        default_spending_tiers = [
            {
                'tier_code': 'vip',
                'display_name': 'VIP',
                'min_spending_amount': 2500000.0,  # > 2.5M IDR
                'max_spending_amount': False,      # No upper limit
                'sequence': 1,
                'tier_color': '#9c27b0',  # Purple for VIP
                'tier_description': 'VIP customers with highest spending (> Rp 2.5M)'
            },
            {
                'tier_code': 'premium',
                'display_name': 'Premium',
                'min_spending_amount': 2000000.0,  # 2M IDR
                'max_spending_amount': 2499999.0,  # 2.5M IDR
                'sequence': 2,
                'tier_color': '#2196f3',  # Blue for premium
                'tier_description': 'Premium customers (Rp 2M - 2.5M)'
            },
            {
                'tier_code': 'gold',
                'display_name': 'Gold',
                'min_spending_amount': 1500000.0,  # 1.5M IDR
                'max_spending_amount': 1999999.0,  # 2M IDR
                'sequence': 3,
                'tier_color': '#ffc107',  # Gold color
                'tier_description': 'Gold tier customers (Rp 1.5M - 2M)'
            },
            {
                'tier_code': 'silver',
                'display_name': 'Silver',
                'min_spending_amount': 1000000.0,  # 1M IDR
                'max_spending_amount': 1499999.0,  # 1.5M IDR
                'sequence': 4,
                'tier_color': '#607d8b',  # Silver/grey color
                'tier_description': 'Silver tier customers (Rp 1M - 1.5M)'
            },
            {
                'tier_code': 'bronze',
                'display_name': 'Bronze',
                'min_spending_amount': 500000.0,   # 500K IDR
                'max_spending_amount': 999999.0,   # 1M IDR
                'sequence': 5,
                'tier_color': '#ff6f00',  # Bronze/orange color
                'tier_description': 'Bronze tier customers (Rp 500K - 1M)'
            },
            {
                'tier_code': 'standard',
                'display_name': 'Standard',
                'min_spending_amount': 250000.0,   # 250K IDR
                'max_spending_amount': 499999.0,   # 500K IDR
                'sequence': 6,
                'tier_color': '#4caf50',  # Green for standard
                'tier_description': 'Standard customers (Rp 250K - 500K)'
            },
            {
                'tier_code': 'basic',
                'display_name': 'Basic',
                'min_spending_amount': 100000.0,   # 100K IDR
                'max_spending_amount': 249999.0,   # 250K IDR
                'sequence': 7,
                'tier_color': '#00bcd4',  # Cyan for basic
                'tier_description': 'Basic customers (Rp 100K - 250K)'
            },
            {
                'tier_code': 'entry',
                'display_name': 'Entry',
                'min_spending_amount': 0.0,        # 0 IDR
                'max_spending_amount': 99999.0,    # 100K IDR
                'sequence': 8,
                'tier_color': '#9e9e9e',  # Grey for entry level
                'tier_description': 'Entry level customers (< Rp 100K)'
            },
        ]
        
        created_count = 0
        for tier_data in default_spending_tiers:
            # Check if tier already exists
            existing_tier = self.search([('tier_code', '=', tier_data['tier_code'])])
            if not existing_tier:
                self.create(tier_data)
                created_count += 1
                _logger.info(f"Created default spending tier: {tier_data['tier_code']} - {tier_data['display_name']}")
        
        _logger.info(f"Created {created_count} default Indonesian customer spending tiers")
        
        # Force recomputation of customer spending tiers after creating defaults
        if created_count > 0:
            partners = self.env['res.partner'].search([('is_company', '=', False), ('customer_rank', '>', 0)])
            if partners:
                partners._compute_customer_spending_tier()
                _logger.info(f"Recomputed spending tiers for {len(partners)} customers")
        
        return created_count

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

    def name_get(self):
        """Custom name display for better UX"""
        result = []
        for tier in self:
            name = f"{tier.tier_code}: {tier.display_name}"
            if tier.max_spending_amount:
                name += f" (Rp {tier.min_spending_amount:,.0f} - {tier.max_spending_amount:,.0f})"
            else:
                name += f" (> Rp {tier.min_spending_amount:,.0f})"
            result.append((tier.id, name))
        return result