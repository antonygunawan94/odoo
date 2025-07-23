# -*- coding: utf-8 -*-
"""
Product Category model extensions for Smart Engagement Module
Handles webhook integration for category management
"""

import logging
from odoo import api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    """Extension of product.category for webhook integration"""
    _inherit = 'product.category'

    @api.model
    def smart_sync(self, payload):
        """Smart synchronization of category data"""
        try:
            # Validate required fields
            if not payload.get('name'):
                raise ValidationError("name is required")
            
            name = payload['name'].strip()
            
            # Find existing category
            existing_category = self.search([
                ('name', '=ilike', name)
            ], limit=1)
            
            vals = {'name': name}
            
            # Handle parent category
            if payload.get('parent_name'):
                parent = self.search([
                    ('name', '=ilike', payload['parent_name'].strip())
                ], limit=1)
                
                if not parent:
                    # Create parent if doesn't exist
                    parent = self.create({
                        'name': payload['parent_name'].strip()
                    })
                vals['parent_id'] = parent.id
            
            if existing_category:
                existing_category.write(vals)
                result = {
                    'success': True,
                    'action': 'updated',
                    'category_id': existing_category.id,
                    'category_name': existing_category.complete_name
                }
                _logger.info(f"Updated category: {existing_category.complete_name}")
            else:
                new_category = self.create(vals)
                result = {
                    'success': True,
                    'action': 'created',
                    'category_id': new_category.id,
                    'category_name': new_category.complete_name
                }
                _logger.info(f"Created category: {new_category.complete_name}")
            
            return result
            
        except Exception as e:
            _logger.error(f"Category smart_sync error: {e}")
            return {'success': False, 'error': str(e)}