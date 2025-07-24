# -*- coding: utf-8 -*-
"""
Sale Order model extensions for Smart Engagement Module
Handles webhook integration for transaction/order management
"""

import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    """Extension of sale.order for webhook integration"""
    _inherit = 'sale.order'
    
    # Customer's external system ID for linking and duplicate detection
    customer_external_id = fields.Char(string="Customer External ID", help="Customer ID from external system used to link order to partner and prevent duplicates")

    @api.model
    def smart_sync(self, payload):
        """Smart synchronization of transaction data (creates confirmed sales orders)"""
        try:
            # Validate required fields - support both new and legacy field names
            customer_external_id = payload.get('external_partner_id') or payload.get('patient_id')
            if not customer_external_id:
                raise ValidationError("external_partner_id or patient_id is required")
            
            order_name = payload.get('name')
            if not order_name:
                raise ValidationError("name is required - order identifier must be provided")
            
            # Check if order with same customer_external_id AND order name already exists
            existing_order = self.search([
                ('customer_external_id', '=', customer_external_id),
                ('name', '=', order_name)
            ], limit=1)
            
            if existing_order:
                _logger.info(f"Found existing order for external_partner_id {customer_external_id} + order_name {order_name} -> Order: {existing_order.name}")
                return {
                    'success': True,
                    'action': 'exists',
                    'order_id': existing_order.id,
                    'order_name': existing_order.name,
                    'customer_name': existing_order.partner_id.name,
                    'amount_total': existing_order.amount_total
                }
            
            # Find customer by external_partner_id reference
            customer = self.env['res.partner'].search([
                ('ref', '=', customer_external_id)
            ], limit=1)
            
            if not customer:
                # Try fuzzy matching by name (optional fallback)
                if payload.get('customer_name'):
                    customer, _ = self.env['res.partner'].find_duplicate_contact_with_score({'name': payload['customer_name']})
                
                if not customer:
                    raise ValidationError(f"Customer not found with external_partner_id: {customer_external_id}")
            
            # Prepare order values
            order_vals = {
                'partner_id': customer.id,
                'state': 'draft',
                'customer_external_id': customer_external_id,  # Store customer_external_id for duplicate detection
                'name': order_name,  # Set the actual order name from external system
            }
            
            # Optional: Set origin to source (business document reference)
            if payload.get('source'):
                order_vals['origin'] = payload['source']
            
            # Order date - IMPORTANT: Use actual order date from external system, not current time
            if payload.get('date_order'):
                try:
                    from dateutil import parser
                    # Parse various date formats including ISO
                    parsed_date = parser.parse(payload['date_order'])
                    order_vals['date_order'] = parsed_date
                except Exception as e:
                    _logger.warning(f"Invalid date format for date_order: {payload.get('date_order')} - {e}")
            
            # Create order
            order = self.create(order_vals)
            
            # Process order lines (required)
            if not payload.get('order_line'):
                raise ValidationError("order_line is required - at least one product line must be provided")
                
            for line_data in payload['order_line']:
                # Validate required line fields
                if not line_data.get('product_code'):
                    raise ValidationError("product_code is required in order_line")
                if not line_data.get('product_uom_qty'):
                    raise ValidationError("product_uom_qty is required in order_line")
                if not line_data.get('price_unit'):
                    raise ValidationError("price_unit is required in order_line")
                
                # Find product by code (required)
                product = self.env['product.product'].search([
                    ('default_code', '=', line_data['product_code'])
                ], limit=1)
                
                if not product and line_data.get('product_name'):
                    # Try fallback: find by product name
                    product = self.env['product.product'].search([
                        ('name', '=ilike', line_data['product_name'])
                    ], limit=1)
                
                if not product:
                    product_info = f"code: {line_data['product_code']}"
                    if line_data.get('product_name'):
                        product_info += f" / name: {line_data['product_name']}"
                    raise ValidationError(f"Product not found with {product_info}")
                
                # Create order line (Odoo auto-calculates subtotals)
                line_vals = {
                    'order_id': order.id,
                    'product_id': product.id,
                    'product_uom_qty': float(line_data['product_uom_qty']),
                    'price_unit': float(line_data['price_unit']),
                }
                self.env['sale.order.line'].create(line_vals)
            
            # Confirm and mark as done
            order.action_confirm()
            
            # Create invoice and mark as paid (to show in analytics)
            if hasattr(order, '_create_invoices'):
                invoice = order._create_invoices()
                if invoice:
                    invoice.action_post()
                    # Register payment to mark as paid
                    payment_vals = {
                        'payment_type': 'inbound',
                        'partner_type': 'customer',
                        'partner_id': customer.id,
                        'amount': order.amount_total,
                        'currency_id': order.currency_id.id,
                        'journal_id': self.env['account.journal'].search([
                            ('type', 'in', ['bank', 'cash'])
                        ], limit=1).id,
                    }
                    payment = self.env['account.payment'].create(payment_vals)
                    payment.action_post()
            
            result = {
                'success': True,
                'order_id': order.id,
                'order_name': order.name,
                'customer_name': customer.name,
                'amount_total': order.amount_total
            }
            
            _logger.info(f"Created order: {order.name} for {customer.name} (Total: {order.amount_total})")
            return result
            
        except Exception as e:
            _logger.error(f"Sale order smart_sync error: {e}")
            return {'success': False, 'error': str(e)}