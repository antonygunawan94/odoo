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

    @api.model
    def smart_sync(self, payload):
        """Smart synchronization of transaction data (creates confirmed sales orders)"""
        try:
            # Validate required fields
            external_id = payload.get('external_id') or payload.get('patient_id')
            if not external_id:
                raise ValidationError("external_id or patient_id is required")
            if not payload.get('source'):
                raise ValidationError("source (agreement id) is required")
            
            # Find customer by external_id reference
            customer_ref = f"CONTACT-{external_id}"
            customer = self.env['res.partner'].search([
                ('ref', '=', customer_ref)
            ], limit=1)
            
            if not customer:
                # Try fuzzy matching by name
                if payload.get('customer_name'):
                    customer, _ = self.env['res.partner'].find_duplicate_contact_with_score({'name': payload['customer_name']})
                
                if not customer:
                    raise ValidationError(f"Customer not found with external_id: {external_id}")
            
            # Prepare order values
            order_vals = {
                'partner_id': customer.id,
                'state': 'draft',
            }
            
            # Order reference
            if payload.get('name'):
                order_vals['client_order_ref'] = payload['name']
            
            # Order date
            if payload.get('date_order'):
                try:
                    order_vals['date_order'] = fields.Datetime.from_string(payload['date_order'])
                except:
                    _logger.warning(f"Invalid date format for date_order: {payload.get('date_order')}")
            
            # Add source as note
            order_vals['note'] = f"Source Agreement ID: {payload['source']}"
            
            # Create order
            order = self.create(order_vals)
            
            # Process order lines
            if payload.get('order_line'):
                for line_data in payload['order_line']:
                    # Find product by code
                    product = self.env['product.product'].search([
                        ('default_code', '=', line_data.get('product_code'))
                    ], limit=1)
                    
                    if not product and line_data.get('product_name'):
                        # Try finding by name
                        product = self.env['product.product'].search([
                            ('name', '=ilike', line_data['product_name'])
                        ], limit=1)
                    
                    if product:
                        line_vals = {
                            'order_id': order.id,
                            'product_id': product.id,
                            'product_uom_qty': float(line_data.get('product_uom_qty', 1)),
                            'price_unit': float(line_data.get('price_unit', product.list_price)),
                        }
                        self.env['sale.order.line'].create(line_vals)
                    else:
                        _logger.warning(f"Product not found: {line_data.get('product_code')} / {line_data.get('product_name')}")
            
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