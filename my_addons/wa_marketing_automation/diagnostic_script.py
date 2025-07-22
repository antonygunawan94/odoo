#!/usr/bin/env python3
"""
Diagnostic script to identify root causes of dashboard issues.
Run this in Odoo shell to diagnose the problems.
"""

import logging
_logger = logging.getLogger(__name__)

def diagnose_dashboard_issues(env):
    """Comprehensive diagnosis of dashboard issues"""
    
    print("=" * 60)
    print("DASHBOARD DIAGNOSTIC SCRIPT")
    print("=" * 60)
    
    # 1. Check if sales source categories exist and have data
    print("\n1. CHECKING SALES SOURCE CATEGORIES:")
    print("-" * 40)
    
    categories = env['wa_marketing.sales_source_category'].search([])
    print(f"Found {len(categories)} sales source categories:")
    for cat in categories:
        print(f"  - {cat.name} (code: {cat.code}, products: {cat.product_count})")
    
    if not categories:
        print("ERROR: No sales source categories found!")
        print("Creating default categories...")
        env['wa_marketing.sales_source_category'].create_default_categories()
        categories = env['wa_marketing.sales_source_category'].search([])
        print(f"Created {len(categories)} default categories")
    
    # 2. Check if products have sales source categories assigned
    print("\n2. CHECKING PRODUCT ASSIGNMENTS:")
    print("-" * 40)
    
    total_products = env['product.template'].search_count([('sale_ok', '=', True)])
    categorized_products = env['product.template'].search_count([
        ('sale_ok', '=', True),
        ('sales_source_category_id', '!=', False)
    ])
    
    print(f"Total sellable products: {total_products}")
    print(f"Categorized products: {categorized_products}")
    print(f"Uncategorized products: {total_products - categorized_products}")
    
    if categorized_products == 0:
        print("ERROR: No products are assigned to sales source categories!")
        print("Auto-assigning categories...")
        for cat in categories:
            if cat.auto_categorize:
                cat.action_auto_categorize_products()
        
        # Recheck
        categorized_products = env['product.template'].search_count([
            ('sale_ok', '=', True),
            ('sales_source_category_id', '!=', False)
        ])
        print(f"After auto-assignment: {categorized_products} products categorized")
    
    # 3. Check sale order lines data
    print("\n3. CHECKING SALE ORDER LINE DATA:")
    print("-" * 40)
    
    # Recent orders
    recent_orders = env['sale.order'].search([
        ('state', '=', 'sale'),
        ('date_order', '>=', '2024-01-01')
    ], limit=5)
    
    print(f"Found {len(recent_orders)} recent confirmed orders")
    
    for order in recent_orders:
        print(f"\nOrder {order.name} ({order.date_order}):")
        for line in order.order_line:
            category = line.sales_source_category_id
            cat_name = category.name if category else "UNCATEGORIZED"
            print(f"  - {line.product_id.name}: {cat_name} (${line.price_subtotal})")
    
    # 4. Check top products by category report model
    print("\n4. CHECKING TOP PRODUCTS REPORT:")
    print("-" * 40)
    
    try:
        # Try to access the report model
        report_model = env['wa_marketing_automation.top_products_by_category_report']
        
        # Check if the SQL view exists
        env.cr.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'wa_marketing_automation_top_products_by_category_report'
        """)
        table_exists = env.cr.fetchone()[0] > 0
        print(f"SQL view exists: {table_exists}")
        
        if table_exists:
            # Try to fetch some data
            env.cr.execute("""
                SELECT COUNT(*) FROM wa_marketing_automation_top_products_by_category_report 
                LIMIT 1
            """)
            record_count = env.cr.fetchone()[0]
            print(f"Records in view: {record_count}")
            
            if record_count > 0:
                # Get sample data
                env.cr.execute("""
                    SELECT product_name, categ_name, total_revenue, period_name
                    FROM wa_marketing_automation_top_products_by_category_report 
                    LIMIT 5
                """)
                samples = env.cr.fetchall()
                print("Sample data:")
                for sample in samples:
                    print(f"  - {sample[0]} ({sample[1]}): ${sample[2]} in {sample[3]}")
            else:
                print("ERROR: No data in top products view!")
        else:
            print("ERROR: Top products SQL view does not exist!")
            print("Recreating view...")
            report_model.init()
            
    except Exception as e:
        print(f"ERROR accessing top products report: {str(e)}")
    
    # 5. Check field types in pivot views
    print("\n5. CHECKING FIELD TYPES FOR PIVOT VIEWS:")
    print("-" * 40)
    
    # Check sale.order.line model fields
    sol_model = env['sale.order.line']
    critical_fields = [
        'sales_source_category_id',
        'product_id', 
        'order_partner_id',
        'price_subtotal',
        'product_uom_qty'
    ]
    
    for field_name in critical_fields:
        if hasattr(sol_model, field_name):
            field = sol_model._fields.get(field_name)
            if field:
                print(f"  - {field_name}: {field.__class__.__name__}")
                
                # For Many2one fields, check if they have proper string representation
                if field.__class__.__name__ == 'Many2one':
                    try:
                        # Test with a real record
                        test_line = sol_model.search([('sales_source_category_id', '!=', False)], limit=1)
                        if test_line:
                            value = getattr(test_line, field_name)
                            print(f"    Sample value: {value} (type: {type(value).__name__})")
                            if hasattr(value, 'name'):
                                print(f"    Display name: {value.name}")
                    except Exception as e:
                        print(f"    ERROR testing field: {str(e)}")
            else:
                print(f"  - {field_name}: FIELD NOT FOUND!")
        else:
            print(f"  - {field_name}: ATTRIBUTE NOT FOUND!")
    
    # 6. Test pivot view data directly
    print("\n6. TESTING PIVOT VIEW DATA:")
    print("-" * 40)
    
    try:
        # Simulate what pivot view does
        env.cr.execute("""
            SELECT 
                sc.name as category_name,
                COUNT(*) as line_count,
                SUM(sol.price_subtotal) as total_revenue
            FROM sale_order_line sol
            LEFT JOIN wa_marketing_sales_source_category sc ON sol.sales_source_category_id = sc.id
            WHERE sol.state = 'sale'
            GROUP BY sc.name
            ORDER BY total_revenue DESC
            LIMIT 5
        """)
        
        pivot_data = env.cr.fetchall()
        print("Pivot data simulation:")
        for row in pivot_data:
            category = row[0] if row[0] else "Uncategorized"
            print(f"  - {category}: {row[1]} lines, ${row[2] or 0}")
            
    except Exception as e:
        print(f"ERROR in pivot simulation: {str(e)}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

# Usage instructions
print("""
To run this diagnostic script:

1. Open Odoo shell:
   make run-shell

2. In the shell, run:
   exec(open('/mnt/c/Users/anton/labs/odoo/odoo/my_addons/wa_marketing_automation/diagnostic_script.py').read())
   diagnose_dashboard_issues(env)
""")