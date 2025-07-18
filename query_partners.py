#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config

# Initialize Odoo
config.parse_config(['-c', '.odoorc'])
odoo.registry(config['db_name'])

# Execute queries
with odoo.api.Environment.manage():
    registry = odoo.registry(config['db_name'])
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Run the partner queries
        print("Partner Database Analysis:")
        print("=" * 40)
        
        # Total partners
        total_partners = env['res.partner'].search_count([])
        print(f"1. Total partners: {total_partners}")
        
        # Individual contacts (is_company = False)
        individual_contacts = env['res.partner'].search_count([('is_company', '=', False)])
        print(f"2. Individual contacts (is_company = False): {individual_contacts}")
        
        # Customers (customer_rank > 0)
        customers = env['res.partner'].search_count([('customer_rank', '>', 0)])
        print(f"3. Customers (customer_rank > 0): {customers}")
        
        # Both conditions (individual customers)
        individual_customers = env['res.partner'].search_count([
            ('is_company', '=', False),
            ('customer_rank', '>', 0)
        ])
        print(f"4. Individual customers (both conditions): {individual_customers}")
        
        # Get some examples
        print("\n5. Examples of individual customers:")
        print("-" * 40)
        examples = env['res.partner'].search([
            ('is_company', '=', False),
            ('customer_rank', '>', 0)
        ], limit=5)
        
        for partner in examples:
            print(f"   ID: {partner.id}")
            print(f"   Name: {partner.name}")
            print(f"   Email: {partner.email}")
            print(f"   Phone: {partner.phone}")
            print(f"   Mobile: {partner.mobile}")
            print(f"   Customer Rank: {partner.customer_rank}")
            print(f"   Is Company: {partner.is_company}")
            print(f"   Parent ID: {partner.parent_id.id if partner.parent_id else 'None'}")
            print("   ---")
        
        # Additional analysis - check for phone/mobile fields
        print("\n6. Additional Analysis:")
        print("-" * 40)
        
        # Individual customers with phone
        with_phone = env['res.partner'].search_count([
            ('is_company', '=', False),
            ('customer_rank', '>', 0),
            ('phone', '!=', False)
        ])
        print(f"   Individual customers with phone: {with_phone}")
        
        # Individual customers with mobile
        with_mobile = env['res.partner'].search_count([
            ('is_company', '=', False),
            ('customer_rank', '>', 0),
            ('mobile', '!=', False)
        ])
        print(f"   Individual customers with mobile: {with_mobile}")
        
        # Individual customers with phone OR mobile
        with_phone_or_mobile = env['res.partner'].search_count([
            ('is_company', '=', False),
            ('customer_rank', '>', 0),
            '|',
            ('phone', '!=', False),
            ('mobile', '!=', False)
        ])
        print(f"   Individual customers with phone OR mobile: {with_phone_or_mobile}")
        
        # Check company records for comparison
        print("\n7. Company Records for Comparison:")
        print("-" * 40)
        
        companies = env['res.partner'].search_count([('is_company', '=', True)])
        print(f"   Total companies: {companies}")
        
        company_customers = env['res.partner'].search_count([
            ('is_company', '=', True),
            ('customer_rank', '>', 0)
        ])
        print(f"   Company customers: {company_customers}")