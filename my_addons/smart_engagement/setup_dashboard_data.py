#!/usr/bin/env python3
"""
Simple script to set up basic data for dashboards to work.
Run this after module update to ensure data exists.
"""

def setup_dashboard_data():
    """Set up basic data for dashboards"""
    
    import odoo
    from odoo import api, SUPERUSER_ID
    import os
    
    # Get database configuration
    config_path = '/mnt/c/Users/anton/labs/odoo/odoo/.odoorc'
    
    # Initialize Odoo
    odoo.tools.config.parse_config(['-c', config_path])
    odoo.cli.server.report_configuration()
    
    # Connect to database
    db_name = 'odoo'
    registry = odoo.registry(db_name)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("SETTING UP DASHBOARD DATA...")
        print("=" * 50)
        
        # 1. Create default sales source categories
        print("1. Setting up sales source categories...")
        try:
            SalesSourceCategory = env['wa_marketing.sales_source_category']
            
            # Check if categories exist
            existing_categories = SalesSourceCategory.search([])
            if not existing_categories:
                print("   Creating default categories...")
                SalesSourceCategory.create_default_categories()
                cr.commit()
                print("   ✓ Default categories created")
            else:
                print(f"   ✓ Found {len(existing_categories)} existing categories")
                
            # Auto-assign products to categories
            categories = SalesSourceCategory.search([('auto_categorize', '=', True)])
            for category in categories:
                try:
                    category.action_auto_categorize_products()
                    print(f"   ✓ Auto-assigned products for: {category.name}")
                except Exception as e:
                    print(f"   ⚠ Error auto-assigning {category.name}: {str(e)}")
            
            cr.commit()
            
        except Exception as e:
            print(f"   ✗ Error setting up categories: {str(e)}")
        
        # 2. Check data in views
        print("\n2. Checking dashboard data...")
        try:
            # Check sale order lines with categories
            cr.execute("""
                SELECT 
                    COALESCE(sc.name, 'Uncategorized') as category,
                    COUNT(sol.id) as lines,
                    COALESCE(SUM(sol.price_subtotal), 0) as revenue
                FROM sale_order_line sol
                LEFT JOIN wa_marketing_sales_source_category sc ON sol.sales_source_category_id = sc.id
                JOIN sale_order so ON sol.order_id = so.id
                WHERE so.state IN ('sale', 'done')
                GROUP BY sc.name
                ORDER BY revenue DESC
                LIMIT 5
            """)
            
            results = cr.fetchall()
            print("   Sales by category:")
            for result in results:
                print(f"     - {result[0]}: {result[1]} lines, ${result[2]:.2f}")
                
        except Exception as e:
            print(f"   ⚠ Error checking sales data: {str(e)}")
        
        # 3. Check top products view
        print("\n3. Checking top products view...")
        try:
            cr.execute("""
                SELECT COUNT(*) FROM smart_engagement_top_products_by_category_report
            """)
            count = cr.fetchone()[0]
            print(f"   ✓ Top products view has {count} records")
            
            if count > 0:
                cr.execute("""
                    SELECT product_name, categ_name, total_revenue, period_name
                    FROM smart_engagement_top_products_by_category_report
                    ORDER BY total_revenue DESC
                    LIMIT 3
                """)
                samples = cr.fetchall()
                print("   Sample top products:")
                for sample in samples:
                    print(f"     - {sample[0]} ({sample[1]}): ${sample[2]:.2f} in {sample[3]}")
            
        except Exception as e:
            print(f"   ⚠ Error checking top products: {str(e)}")
        
        # 4. Test pivot data for charts
        print("\n4. Testing chart data...")
        try:
            # Test basic pivot query that charts would use
            cr.execute("""
                SELECT 
                    COALESCE(sc.name, 'Uncategorized') as category_name,
                    SUM(sol.price_subtotal) as total_revenue
                FROM sale_order_line sol
                LEFT JOIN wa_marketing_sales_source_category sc ON sol.sales_source_category_id = sc.id
                JOIN sale_order so ON sol.order_id = so.id
                WHERE so.state IN ('sale', 'done')
                  AND so.date_order >= (CURRENT_DATE - INTERVAL '3 months')
                GROUP BY sc.name
                HAVING SUM(sol.price_subtotal) > 0
                ORDER BY total_revenue DESC
            """)
            
            chart_data = cr.fetchall()
            print("   Chart data preview:")
            for data in chart_data:
                print(f"     - {data[0]}: ${data[1]:.2f}")
                
        except Exception as e:
            print(f"   ⚠ Error testing chart data: {str(e)}")
        
        print("\n" + "=" * 50)
        print("DASHBOARD DATA SETUP COMPLETE!")
        print("=" * 50)
        print("\nYou can now test the dashboards:")
        print("1. Go to Smart Engagement > Dashboard")
        print("2. Check Sales Source Analysis")
        print("3. Check Top Products Analysis")
        print("4. Verify that charts show actual data instead of [object Object]")

if __name__ == "__main__":
    setup_dashboard_data()