# -*- coding: utf-8 -*-
"""
Product model extensions for Smart Engagement Module
Handles webhook integration for product management
"""

import logging
from odoo import api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    """Extension of product.product for webhook integration"""
    _inherit = 'product.product'

    @api.model
    def smart_sync(self, payload):
        """Smart synchronization of product data (services, products, treatments)"""
        try:
            # Validate required fields
            if not payload.get('name'):
                raise ValidationError("name is required")
            
            # Find category
            category_id = False
            if payload.get('categ_name'):
                category = self.env['product.category'].search([
                    ('name', '=ilike', payload['categ_name'].strip())
                ], limit=1)
                if category:
                    category_id = category.id
                else:
                    # Create category if doesn't exist
                    category = self.env['product.category'].create({
                        'name': payload['categ_name'].strip()
                    })
                    category_id = category.id
            
            # Prepare product values
            vals = {
                'name': payload['name'].strip(),
                'type': payload.get('type', 'service'),  # Default to service
                'sale_ok': True,
                'purchase_ok': False,
            }
            
            if payload.get('default_code'):
                vals['default_code'] = payload['default_code'].strip()
            
            if payload.get('barcode'):
                vals['barcode'] = payload['barcode'].strip()
            
            if payload.get('list_price'):
                vals['list_price'] = float(payload['list_price'])
            
            if category_id:
                vals['categ_id'] = category_id
            
            # Find existing product by code or barcode
            domain = []
            if payload.get('default_code'):
                domain = [('default_code', '=', payload['default_code'].strip())]
            elif payload.get('barcode'):
                domain = [('barcode', '=', payload['barcode'].strip())]
            
            existing_product = False
            if domain:
                existing_product = self.search(domain, limit=1)
            
            if existing_product:
                existing_product.write(vals)
                result = {
                    'success': True,
                    'action': 'updated',
                    'product_id': existing_product.id,
                    'product_name': existing_product.name,
                    'product_code': existing_product.default_code
                }
                _logger.info(f"Updated product: {existing_product.name} [{existing_product.default_code}]")
            else:
                new_product = self.create(vals)
                result = {
                    'success': True,
                    'action': 'created',
                    'product_id': new_product.id,
                    'product_name': new_product.name,
                    'product_code': new_product.default_code
                }
                _logger.info(f"Created product: {new_product.name} [{new_product.default_code}]")
            
            return result
            
        except Exception as e:
            _logger.error(f"Product smart_sync error: {e}")
            return {'success': False, 'error': str(e)}