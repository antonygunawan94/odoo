#!/usr/bin/env python3
"""
Script to inspect actual product data in the database
"""

import os
import sys

# Add Odoo to Python path
sys.path.append('/mnt/c/Users/anton/labs/odoo/odoo')

import odoo
from odoo import api, SUPERUSER_ID

def inspect_products():
    """Inspect actual products and their names"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config(['-c', '/mnt/c/Users/anton/labs/odoo/odoo/.odoorc'])
    
    # Connect to database
    db_name = 'odoo'
    registry = odoo.registry(db_name)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("=" * 60)
        print("INSPECTING ACTUAL DATABASE PRODUCTS")
        print("=" * 60)
        
        # 1. Check sale order lines
        print("\n1. RECENT SALE ORDER LINES:")
        print("-" * 40)
        
        recent_lines = env['sale.order.line'].search([
            ('order_id.state', 'in', ['sale', 'done']),
            ('price_subtotal', '>', 0)
        ], limit=5)
        
        for line in recent_lines:
            print(f"Line ID: {line.id}")
            print(f"  Product ID: {line.product_id.id}")
            print(f"  Product Name: {line.product_id.name}")
            print(f"  Product Name Type: {type(line.product_id.name)}")
            print(f"  Product Template Name: {line.product_id.product_tmpl_id.name}")
            print(f"  Category: {line.product_id.categ_id.name}")
            print(f"  Price: {line.price_subtotal}")
            print(f"  Order: {line.order_id.name}")
            print()
        
        # 2. Check raw SQL fields
        print("\n2. RAW SQL PRODUCT FIELDS:")
        print("-" * 40)
        
        cr.execute("""
            SELECT 
                pp.id as product_id,
                pt.name as template_name_raw,
                pc.name as category_name_raw,
                sol.price_subtotal,
                so.name as order_name
            FROM sale_order_line sol
            JOIN sale_order so ON sol.order_id = so.id
            JOIN product_product pp ON sol.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
            JOIN product_category pc ON pt.categ_id = pc.id
            WHERE so.state IN ('sale', 'done')
            AND sol.price_subtotal > 0
            LIMIT 5
        """)
        
        raw_results = cr.fetchall()
        for result in raw_results:
            print(f"Product ID: {result[0]}")
            print(f"  Template Name Raw: {result[1]} (type: {type(result[1])})")
            print(f"  Category Name Raw: {result[2]} (type: {type(result[2])})")
            print(f"  Price: {result[3]}")
            print(f"  Order: {result[4]}")
            print()
        
        # 3. Test JSON extraction if needed
        print("\n3. TESTING JSON EXTRACTION:")
        print("-" * 40)
        
        if raw_results:
            sample_name = raw_results[0][1]
            if isinstance(sample_name, dict):
                print(f"Name is dict: {sample_name}")
                if 'en_US' in sample_name:
                    print(f"English name: {sample_name['en_US']}")
            elif isinstance(sample_name, str):
                print(f"Name is string: {sample_name}")
                if sample_name.startswith('{'):
                    import json
                    try:
                        parsed = json.loads(sample_name)
                        print(f"Parsed JSON: {parsed}")
                        if 'en_US' in parsed:
                            print(f"English name from JSON: {parsed['en_US']}")
                    except Exception as e:
                        print(f"JSON parse error: {e}")
        
        # 4. Check what fields are available
        print("\n4. AVAILABLE PRODUCT FIELDS:")
        print("-" * 40)
        
        if recent_lines:
            sample_product = recent_lines[0].product_id
            print("Product model fields:")
            for field_name in ['name', 'display_name', 'default_code']:
                if hasattr(sample_product, field_name):
                    value = getattr(sample_product, field_name)
                    print(f"  {field_name}: {value} (type: {type(value)})")
        
        print("\n" + "=" * 60)
        print("INSPECTION COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    inspect_products()