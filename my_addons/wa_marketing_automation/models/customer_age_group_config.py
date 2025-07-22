# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CustomerAgeGroupConfig(models.Model):
    """Configuration model for customer age group segmentation"""
    
    _name = 'wa_marketing_automation.customer_age_group_config'
    _description = 'Customer Age Group Configuration'
    _order = 'sequence, min_age asc'
    _rec_name = 'display_name'

    # Basic Configuration Fields
    group_code = fields.Char(
        string='Age Group Code',
        required=True,
        size=256,
        help='Short code for this age group (e.g., youth, adult, senior)'
    )
    
    display_name = fields.Char(
        string='Display Name',
        required=True,
        help='Human-readable name for this age group (e.g., Young Adult, Mature Professional)'
    )
    
    min_age = fields.Integer(
        string='Minimum Age',
        required=True,
        default=0,
        help='Minimum age in years for this group (inclusive)'
    )
    
    max_age = fields.Integer(
        string='Maximum Age',
        help='Maximum age in years for this group (inclusive). Leave empty for no upper limit.'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Display order for age groups'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this age group is active and used for classification'
    )
    
    group_color = fields.Char(
        string='Group Color',
        help='Color code for visual identification in charts and reports'
    )
    
    group_description = fields.Text(
        string='Group Description',
        help='Description of this age group\'s characteristics and business value'
    )

    # Analytics Fields (Computed)
    customer_count = fields.Integer(
        string='Customer Count',
        compute='_compute_age_group_analytics',
        store=True,
        help='Number of customers in this age group'
    )
    
    average_age = fields.Float(
        string='Average Age',
        compute='_compute_age_group_analytics',
        store=True,
        digits=(3, 1),
        help='Average age of customers in this group'
    )
    
    total_group_revenue = fields.Float(
        string='Total Group Revenue',
        compute='_compute_age_group_analytics',
        store=True,
        help='Total revenue from customers in this age group'
    )
    
    average_spending = fields.Float(
        string='Average Spending per Customer',
        compute='_compute_age_group_analytics',
        store=True,
        help='Average spending per customer in this age group'
    )
    
    age_distribution_percentage = fields.Float(
        string='Age Distribution %',
        compute='_compute_age_group_analytics',
        store=True,
        digits=(5, 2),
        help='Percentage of total customers this age group represents'
    )

    # Constraints and Validation
    @api.constrains('min_age', 'max_age')
    def _check_age_range_validity(self):
        """Validate age ranges are logical"""
        for group in self:
            if group.min_age < 0:
                raise ValidationError("Minimum age cannot be negative.")
            
            # Only validate max_age if it has a value (not False)
            if group.max_age and group.max_age < 0:
                raise ValidationError("Maximum age cannot be negative.")
            
            # Only compare if max_age has a value (not False/None)
            if group.max_age and group.min_age > group.max_age:
                raise ValidationError(
                    f"Minimum age ({group.min_age}) cannot be greater than maximum age ({group.max_age})."
                )
            
            # Business logic: reasonable age limits
            if group.min_age > 150:
                raise ValidationError("Minimum age cannot exceed 150 years.")
            
            if group.max_age and group.max_age > 150:
                raise ValidationError("Maximum age cannot exceed 150 years.")

    @api.constrains('min_age', 'max_age', 'active')
    def _check_no_overlapping_ranges(self):
        """Ensure no overlapping age ranges for active groups"""
        # Skip validation during data loading/update
        if self.env.context.get('skip_overlap_validation'):
            return
        for group in self:
            if not group.active:
                continue
                
            # Use manual overlap checking with proper range overlap algorithm
            all_other_groups = self.search([('id', '!=', group.id), ('active', '=', True)])
            overlapping_groups = self.browse()
            
            for other_group in all_other_groups:
                # Check if ranges overlap using standard algorithm: 
                # [A1,A2] overlaps [B1,B2] if A1 <= B2 AND B1 <= A2
                
                # Handle infinite upper bounds (max_age = False means infinity)
                group_max = group.max_age if group.max_age is not False else float('inf')
                other_max = other_group.max_age if other_group.max_age is not False else float('inf')
                
                # Check overlap condition
                if group.min_age <= other_max and other_group.min_age <= group_max:
                    overlapping_groups |= other_group
            
            if overlapping_groups:
                overlapping_names = ', '.join(overlapping_groups.mapped('display_name'))
                raise ValidationError(
                    f"Age group '{group.display_name}' (ages {group.min_age}-"
                    f"{'∞' if group.max_age is False else group.max_age}) overlaps with: {overlapping_names}. "
                    f"Please adjust the age ranges to avoid overlaps."
                )

    @api.constrains('group_code', 'active')
    def _check_unique_group_code(self):
        """Ensure group codes are unique among active groups"""
        for group in self:
            if group.active:
                duplicate_groups = self.search([
                    ('id', '!=', group.id),
                    ('active', '=', True),
                    ('group_code', '=', group.group_code)
                ])
                
                if duplicate_groups:
                    raise ValidationError(
                        f"Age group code '{group.group_code}' is already used by another active age group. "
                        f"Please use a different group code."
                    )

    @api.depends('min_age', 'max_age', 'active')
    def _compute_age_group_analytics(self):
        """Compute analytics for each age group"""
        for group in self:
            if not group.active:
                # Reset analytics for inactive groups
                group.customer_count = 0
                group.average_age = 0.0
                group.total_group_revenue = 0.0
                group.average_spending = 0.0
                group.age_distribution_percentage = 0.0
                continue
            
            # Get all customers and filter by age ranges
            domain = [
                ('is_company', '=', False),
                ('customer_rank', '>', 0),
                ('age', '>=', group.min_age)
            ]
            
            # Add max age condition if group has upper limit
            if group.max_age is not False:
                domain.append(('age', '<=', group.max_age))
            
            customers = self.env['res.partner'].search(domain)
            
            # Compute basic analytics
            group.customer_count = len(customers)
            
            if customers:
                # Calculate average age
                total_age = sum(customers.mapped('age'))
                group.average_age = total_age / len(customers)
                
                # Calculate revenue metrics
                group.total_group_revenue = sum(customers.mapped('total_spent'))
                group.average_spending = group.total_group_revenue / len(customers)
                
                # Calculate distribution percentage
                total_customers = self.env['res.partner'].search_count([
                    ('is_company', '=', False),
                    ('customer_rank', '>', 0),
                    ('age', '>', 0)  # Only count customers with valid ages
                ])
                
                if total_customers > 0:
                    group.age_distribution_percentage = (len(customers) / total_customers) * 100
                else:
                    group.age_distribution_percentage = 0.0
            else:
                group.average_age = 0.0
                group.total_group_revenue = 0.0
                group.average_spending = 0.0
                group.age_distribution_percentage = 0.0

    @api.onchange('min_age', 'max_age')
    def _onchange_age_ranges(self):
        """Auto-refresh analytics when age ranges change"""
        if self.min_age is not False or self.max_age is not False:
            self._compute_age_group_analytics()

    @api.model
    def get_age_group_for_age(self, age):
        """
        Get the appropriate age group code for a given age
        
        Args:
            age (int): Customer age in years
            
        Returns:
            str: Age group code for the appropriate group, or 'UNCLASSIFIED'
        """
        if age < 0:
            _logger.warning(f"Negative age received: {age}")
            return 'UNCLASSIFIED'
        
        # Find matching active group
        domain = [
            ('active', '=', True),
            ('min_age', '<=', age),
        ]
        
        # Add max age condition (None means no upper limit)
        group = self.search(domain + [
            '|', 
            ('max_age', '>=', age), 
            ('max_age', '=', False)
        ], limit=1)
        
        if group:
            _logger.debug(f"Age {age} years classified as group '{group.group_code}'")
            return group.group_code
        else:
            _logger.warning(f"No age group found for age {age} years")
            return 'UNCLASSIFIED'

    @api.model
    def get_age_group_selection(self):
        """Get selection list for age group field"""
        active_groups = self.search([('active', '=', True)], order='sequence, min_age asc')
        selection = [(group.group_code, group.display_name) for group in active_groups]
        
        # Add unclassified option
        selection.append(('UNCLASSIFIED', 'Unclassified'))
        
        return selection

    def action_refresh_age_group_analytics(self):
        """Manual action to refresh analytics"""
        self._compute_age_group_analytics()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Age group analytics refreshed successfully!',
                'type': 'success',
                'sticky': False,
            }
        }

    def _recompute_all_partner_age_groups(self):
        """Recompute age groups for all customers"""
        customers = self.env['res.partner'].search([
            ('is_company', '=', False),
            ('customer_rank', '>', 0)
        ])
        if customers:
            _logger.info(f"Recomputing age groups for {len(customers)} customers")
            customers._compute_customer_age_group()
            _logger.info("Age group recomputation completed")

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to trigger partner recomputation (batch-aware)"""
        records = super().create(vals_list)
        # Recompute partner age groups when new age group config is created
        if records:
            records[0]._recompute_all_partner_age_groups()  # Only call once for batch
        return records

    def write(self, vals):
        """Override write to trigger partner recomputation when age ranges change"""
        # Check if age-related fields are being modified
        age_fields = {'min_age', 'max_age', 'active', 'group_code'}
        if any(field in vals for field in age_fields):
            result = super().write(vals)
            # Recompute partner age groups when age configuration changes
            self._recompute_all_partner_age_groups()
            return result
        else:
            return super().write(vals)

    def unlink(self):
        """Override unlink to trigger partner recomputation when age groups are deleted"""
        result = super().unlink()
        # Recompute partner age groups when age group config is deleted
        if self.env['res.partner']:
            self.env['res.partner'].search([
                ('is_company', '=', False),
                ('customer_rank', '>', 0)
            ])._compute_customer_age_group()
        return result

    def name_get(self):
        """Custom name display for better UX"""
        result = []
        for record in self:
            max_age_display = '∞' if record.max_age is False else str(record.max_age)
            name = f"{record.display_name} ({record.min_age}-{max_age_display} years)"
            result.append((record.id, name))
        return result

    @api.model
    def create_default_age_groups_if_empty(self):
        """Create default age groups only if database is empty"""
        # Check if any age groups exist
        existing_count = self.search_count([])
        if existing_count > 0:
            _logger.info(f"Age groups already exist ({existing_count} records), skipping default creation")
            return True
            
        _logger.info("No age groups found, creating default age groups")
        
        default_groups = [
            {
                'group_code': 'young',
                'display_name': 'Young (Under 18)',
                'min_age': 0,
                'max_age': 17,
                'sequence': 10,
                'active': True,
                'group_color': '#E8F4FD',
                'group_description': 'Young customers under 18 years old. Requires parental consent for services.'
            },
            {
                'group_code': '18_25',
                'display_name': 'Youth (18-25)',
                'min_age': 18,
                'max_age': 25,
                'sequence': 20,
                'active': True,
                'group_color': '#FFE6CC',
                'group_description': 'Young adults starting their careers. Digital-native, budget-conscious.'
            },
            {
                'group_code': '26_35',
                'display_name': 'Young Adult (26-35)',
                'min_age': 26,
                'max_age': 35,
                'sequence': 30,
                'active': True,
                'group_color': '#FFCCDD',
                'group_description': 'Career-building professionals, often starting families.'
            },
            {
                'group_code': '36_45',
                'display_name': 'Adult (36-45)',
                'min_age': 36,
                'max_age': 45,
                'sequence': 40,
                'active': True,
                'group_color': '#E6CCFF',
                'group_description': 'Established professionals with families. Peak earning years.'
            },
            {
                'group_code': '46_55',
                'display_name': 'Mature Professional (46-55)',
                'min_age': 46,
                'max_age': 55,
                'sequence': 50,
                'active': True,
                'group_color': '#CCFFCC',
                'group_description': 'Mature professionals with higher disposable income.'
            },
            {
                'group_code': '56_65',
                'display_name': 'Senior (56-64)',
                'min_age': 56,
                'max_age': 64,
                'sequence': 60,
                'active': True,
                'group_color': '#FFFFCC',
                'group_description': 'Pre-retirement customers with time and resources for self-care.'
            },
            {
                'group_code': '65_plus',
                'display_name': 'Elder (65+)',
                'min_age': 65,
                'max_age': False,
                'sequence': 70,
                'active': True,
                'group_color': '#F0F0F0',
                'group_description': 'Retirement-age customers focused on skin health and comfort.'
            }
        ]
        
        # Create default groups with validation disabled
        for group_data in default_groups:
            self.with_context(skip_overlap_validation=True).create(group_data)
            
        _logger.info(f"Created {len(default_groups)} default age groups")
        return True

    @api.model
    def migrate_to_new_codes(self):
        """Migrate existing age group codes to new format"""
        # Check if migration already completed
        if self.env['ir.config_parameter'].sudo().get_param('wa_marketing_automation.vip_tiers_migrated'):
            return True
            
        # Temporarily disable constraints
        with self.env.cr.savepoint():
            # Update age group codes
            updates = [
                ('Minor (Under 18)', 'young', 'Young (Under 18)'),
                ('Youth (18-25)', '18_25', None),
                ('Young Adult (26-35)', '26_35', None), 
                ('Adult (36-45)', '36_45', None),
                ('Mature Professional (46-55)', '46_55', None),
                ('Senior (56-64)', '56_65', None),
                ('Elder (65+)', '65_plus', None),
            ]
            
            for old_name, new_code, new_display_name in updates:
                groups = self.search([('display_name', '=', old_name)])
                if groups:
                    values = {'group_code': new_code}
                    if new_display_name:
                        values['display_name'] = new_display_name
                    groups.with_context(skip_overlap_validation=True).write(values)
                    
        # Update spending tiers - delete ALL existing tiers first
        tier_model = self.env['wa_marketing_automation.customer_spending_tier_config']
        
        # Force delete all tiers to prevent conflicts - XML data will reload them
        self.env.cr.execute("DELETE FROM wa_marketing_automation_customer_spending_tier_config")
        
        # Recompute customer fields
        customers = self.env['res.partner'].search([('is_company', '=', False), ('customer_rank', '>', 0)])
        if customers:
            customers._compute_customer_spending_tier()
            customers._compute_customer_age_group()
        
        # Mark migration as completed
        self.env['ir.config_parameter'].sudo().set_param('wa_marketing_automation.vip_tiers_migrated', 'true')
        
        return True