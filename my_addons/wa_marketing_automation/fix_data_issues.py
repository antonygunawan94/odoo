#!/usr/bin/env python3
"""
Simple data fix script to ensure basic data exists for dashboards to work.
"""

def fix_basic_data_issues(env):
    """Fix basic data issues that prevent dashboards from working"""
    
    print("FIXING BASIC DATA ISSUES...")
    print("=" * 50)
    
    # 1. Ensure sales source categories exist
    print("1. Checking sales source categories...")
    categories = env['wa_marketing.sales_source_category'].search([])
    
    if not categories:
        print("   Creating default sales source categories...")
        env['wa_marketing.sales_source_category'].create_default_categories()
        env.cr.commit()
        categories = env['wa_marketing.sales_source_category'].search([])
        print(f"   Created {len(categories)} categories")
    else:
        print(f"   Found {len(categories)} existing categories")
    
    # 2. Auto-assign products to categories
    print("2. Auto-assigning products to categories...")
    for category in categories:
        if category.auto_categorize:
            try:
                category.action_auto_categorize_products()
                print(f"   Processed category: {category.name}")
            except Exception as e:
                print(f"   Error with {category.name}: {str(e)}")
    
    env.cr.commit()
    
    # 3. Check if sale order lines have categories
    print("3. Checking sale order line categories...")
    
    # Count lines with and without categories
    total_lines = env['sale.order.line'].search_count([('state', '=', 'sale')])
    categorized_lines = env['sale.order.line'].search_count([
        ('state', '=', 'sale'),
        ('sales_source_category_id', '!=', False)
    ])
    
    print(f"   Total confirmed sale lines: {total_lines}")
    print(f"   Categorized lines: {categorized_lines}")
    print(f"   Uncategorized lines: {total_lines - categorized_lines}")
    
    # 4. Force recreation of top products view
    print("4. Recreating top products by category view...")
    try:
        report_model = env['wa_marketing_automation.top_products_by_category_report']
        report_model.init()
        env.cr.commit()
        print("   Top products view recreated successfully")
        
        # Test if view has data
        env.cr.execute("SELECT COUNT(*) FROM wa_marketing_automation_top_products_by_category_report")
        count = env.cr.fetchone()[0]
        print(f"   View contains {count} records")
        
    except Exception as e:
        print(f"   Error recreating view: {str(e)}")
    
    # 5. Test pivot data query
    print("5. Testing pivot data query...")
    try:
        env.cr.execute("""
            SELECT 
                COALESCE(sc.name, 'Uncategorized') as category_name,
                COUNT(sol.id) as line_count,
                COALESCE(SUM(sol.price_subtotal), 0) as total_revenue
            FROM sale_order_line sol
            LEFT JOIN wa_marketing_sales_source_category sc ON sol.sales_source_category_id = sc.id
            JOIN sale_order so ON sol.order_id = so.id
            WHERE so.state IN ('sale', 'done')
            GROUP BY sc.name
            ORDER BY total_revenue DESC
            LIMIT 10
        """)
        
        results = env.cr.fetchall()
        print("   Pivot test results:")
        for result in results:
            print(f"     - {result[0]}: {result[1]} lines, ${result[2]:.2f}")
            
    except Exception as e:
        print(f"   Error in pivot test: {str(e)}")
    
    print("\nDATA FIX COMPLETE!")
    print("Try accessing the dashboards now.")

# Instructions for running this
print("""
To run this fix script:

1. In terminal, run: python odoo-bin shell --config=.odoorc
2. In the shell, run:
   exec(open('/mnt/c/Users/anton/labs/odoo/odoo/my_addons/wa_marketing_automation/fix_data_issues.py').read())
   fix_basic_data_issues(env)
""")