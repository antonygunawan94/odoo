# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class PerformanceAnalyticsReport(models.Model):
    _name = 'wa_marketing_automation.performance_analytics_report'
    _description = 'Performance Analytics Report'
    _auto = False
    _order = 'order_date desc'

    # === PRIMARY KEYS & IDENTIFIERS ===
    order_id = fields.Many2one('sale.order', 'Order', readonly=True)
    line_id = fields.Many2one('sale.order.line', 'Order Line', readonly=True)
    
    # === SPENDING ANALYSIS ===
    spending_tier_id = fields.Many2one(
        'wa_marketing_automation.customer_spending_tier_config',
        'Spending Tier Config',
        readonly=True
    )
    spending_tier_code = fields.Char('Spending Tier Code', readonly=True)
    spending_tier_name = fields.Char('Spending Tier Name', readonly=True, aggregator='max')
    spending_tier_display = fields.Char('Spending Tier', readonly=True, help='Tier name with spending range', aggregator='max') 
    
    # === PRODUCT DIMENSIONS ===
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_name = fields.Char('Product Name', readonly=True, aggregator='max')
    product_category_id = fields.Many2one('product.category', 'Product Category', readonly=True) 
    parent_category_id = fields.Many2one('product.category', 'Parent Category', readonly=True)
    category_name = fields.Char('Category Name', readonly=True, aggregator='max')
    product_type = fields.Selection([
        ('consu', 'Product'), 
        ('service', 'Service')
    ], 'Product Type', readonly=True)
    
    # === CUSTOMER DIMENSIONS ===  
    partner_id = fields.Many2one('res.partner', 'Customer', readonly=True)
    customer_name = fields.Char('Customer Name', readonly=True, aggregator='max')
    customer_age_group = fields.Char('Customer Age Group', readonly=True, aggregator='max')
    customer_country_id = fields.Many2one('res.country', 'Customer Country', readonly=True)
    customer_state_id = fields.Many2one('res.country.state', 'Customer State', readonly=True)
    
    # === CUSTOMER ACQUISITION SOURCE (Marketing Attribution) ===
    customer_acquisition_source_id = fields.Many2one(
        'wa_marketing_automation.customer_acquisition_source_config',
        'Customer Acquisition Source',
        readonly=True
    )
    customer_acquisition_source_name = fields.Char(
        'Acquisition Source Name',
        readonly=True,
        aggregator='max',
        help="IG, TIKTOK, LEWAT DEPAN ELLA, TEMAN/KELUARGA"
    )
    
    # === CUSTOMER SEGMENTATION ===
    is_new_customer = fields.Boolean('Is New Customer', readonly=True)
    customer_type = fields.Selection([
        ('new', 'New Customer'),
        ('existing', 'Existing Customer')
    ], 'Customer Type', readonly=True)
    
    # === SALES DIMENSIONS ===
    salesperson_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    sales_team_id = fields.Many2one('crm.team', 'Sales Team', readonly=True)
    order_date = fields.Date('Order Date', readonly=True)
    order_month = fields.Char('Order Month', readonly=True, aggregator='max')
    order_quarter = fields.Char('Order Quarter', readonly=True, aggregator='max') 
    order_year = fields.Integer('Order Year', readonly=True)
    
    # === SALES SOURCE (Business Classification) ===
    sales_source_id = fields.Many2one('utm.source', 'Sales Source', readonly=True)
    sales_source_name = fields.Char(
        'Sales Source Name', 
        readonly=True,
        aggregator='max',
        help="PRODUK, TREATMENT CLINIC, REDEEM"
    )
    
    # === MEASURES ===
    quantity_ordered = fields.Integer('Qty Ordered', readonly=True)
    revenue = fields.Float('Revenue', readonly=True)
    avg_order_value = fields.Float('Avg Order Value', readonly=True, aggregator='avg')
    order_count = fields.Integer('# Orders', readonly=True)
    customer_count = fields.Integer('# Customers', readonly=True)

    @api.model
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        
        # Create the SQL view with CTE-based spending tier matching
        # This approach uses proper relational design instead of CASE statements
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                WITH parent_categories AS (
                    -- Get business-level parent category for each category  
                    -- Treats PRODUK/JASA as meaningful parents instead of "All"
                    SELECT 
                        pc.id as category_id,
                        CASE 
                            -- Direct children of "All" are treated as business-level parents  
                            WHEN pc.parent_id = 1 THEN pc.id
                            -- Categories without parent (like "All") map to themselves
                            WHEN pc.parent_id IS NULL THEN pc.id
                            -- Deep nested categories map to their business-level parent
                            ELSE CAST(SPLIT_PART(pc.parent_path, '/', 2) AS INTEGER)
                        END as parent_category_id
                    FROM product_category pc
                ),
                spending_tier_lookup AS (
                    -- Create lookup for order amounts to spending tier configs
                    -- Uses window functions with improved NULL handling for robust tier matching
                    SELECT DISTINCT
                        so.id as order_id,
                        so.amount_total,
                        FIRST_VALUE(st.id) OVER (
                            PARTITION BY so.id 
                            ORDER BY 
                                CASE 
                                    WHEN so.amount_total >= st.min_spending_amount 
                                         AND (st.max_spending_amount IS NULL OR so.amount_total <= st.max_spending_amount)
                                    THEN st.min_spending_amount 
                                    ELSE NULL 
                                END DESC NULLS LAST,
                                st.min_spending_amount DESC
                        ) as tier_id,
                        FIRST_VALUE(st.tier_code) OVER (
                            PARTITION BY so.id 
                            ORDER BY 
                                CASE 
                                    WHEN so.amount_total >= st.min_spending_amount 
                                         AND (st.max_spending_amount IS NULL OR so.amount_total <= st.max_spending_amount)
                                    THEN st.min_spending_amount 
                                    ELSE NULL 
                                END DESC NULLS LAST,
                                st.min_spending_amount DESC
                        ) as tier_code,
                        FIRST_VALUE(st.display_name) OVER (
                            PARTITION BY so.id 
                            ORDER BY 
                                CASE 
                                    WHEN so.amount_total >= st.min_spending_amount 
                                         AND (st.max_spending_amount IS NULL OR so.amount_total <= st.max_spending_amount)
                                    THEN st.min_spending_amount 
                                    ELSE NULL 
                                END DESC NULLS LAST,
                                st.min_spending_amount DESC
                        ) as tier_name,
                        FIRST_VALUE(
                            CASE 
                                WHEN st.max_spending_amount IS NULL THEN 
                                    st.display_name || ' (> Rp ' || TO_CHAR(st.min_spending_amount, 'FM999,999,999') || ')'
                                ELSE 
                                    st.display_name || ' (Rp ' || TO_CHAR(st.min_spending_amount, 'FM999,999,999') || ' - ' || TO_CHAR(st.max_spending_amount, 'FM999,999,999') || ')'
                            END
                        ) OVER (
                            PARTITION BY so.id 
                            ORDER BY 
                                CASE 
                                    WHEN so.amount_total >= st.min_spending_amount 
                                         AND (st.max_spending_amount IS NULL OR so.amount_total <= st.max_spending_amount)
                                    THEN st.min_spending_amount 
                                    ELSE NULL 
                                END DESC NULLS LAST,
                                st.min_spending_amount DESC
                        ) as tier_display
                    FROM sale_order so
                    CROSS JOIN wa_marketing_automation_customer_spending_tier_config st
                    WHERE st.active = true
                )
                SELECT
                    -- IDs
                    row_number() OVER () AS id,
                    so.id as order_id,
                    sol.id as line_id,
                    
                    -- Spending Analysis  
                    tier_match.tier_id as spending_tier_id,
                    COALESCE(tier_match.tier_code, 'UNCLASSIFIED') as spending_tier_code,
                    COALESCE(tier_match.tier_name, 'Unclassified') as spending_tier_name,
                    COALESCE(tier_match.tier_display, 'Unclassified') as spending_tier_display,
                    
                    -- Product Dimensions
                    pp.id as product_id,
                    CASE 
                        WHEN pp.default_code IS NOT NULL THEN
                            CONCAT('(', pp.default_code, ') ', 
                                CASE 
                                    WHEN pt.name::text LIKE '{{%' 
                                    THEN pt.name->>'en_US'  -- Extract English value from JSON
                                    ELSE pt.name::text      -- Handle non-JSON legacy data
                                END
                            )
                        ELSE
                            CASE 
                                WHEN pt.name::text LIKE '{{%' 
                                THEN pt.name->>'en_US'  -- Extract English value from JSON
                                ELSE pt.name::text      -- Handle non-JSON legacy data
                            END
                    END as product_name,
                    pc.id as product_category_id,
                    pn.parent_category_id,
                    COALESCE(parent_pc.name, 'UNCATEGORIZED') as category_name,
                    pt.type as product_type,
                    
                    -- Customer Dimensions
                    rp.id as partner_id, 
                    rp.name as customer_name,
                    COALESCE(rp.customer_age_group, 'Unknown') as customer_age_group,
                    rp.country_id as customer_country_id,
                    rp.state_id as customer_state_id,
                    
                    -- Customer Acquisition Source (Marketing Attribution)
                    rp.acquisition_source_id as customer_acquisition_source_id,
                    COALESCE(acq_src.display_name, 'Unknown') as customer_acquisition_source_name,
                    
                    -- Customer Segmentation
                    rp.is_new_customer,
                    CASE 
                        WHEN rp.is_new_customer = true THEN 'new'
                        ELSE 'existing'
                    END as customer_type,
                    
                    -- Sales Dimensions
                    so.user_id as salesperson_id,
                    so.team_id as sales_team_id,
                    so.date_order::date as order_date,
                    TO_CHAR(so.date_order, 'YYYY-MM') as order_month,
                    CONCAT('Q', EXTRACT(QUARTER FROM so.date_order), '-', 
                           EXTRACT(YEAR FROM so.date_order)) as order_quarter,
                    EXTRACT(YEAR FROM so.date_order) as order_year,
                    
                    -- Sales Source (Business Classification)
                    so.source_id as sales_source_id,
                    COALESCE(sales_src.name, 'Unclassified') as sales_source_name,
                    
                    -- Measures
                    CAST(sol.product_uom_qty AS INTEGER) as quantity_ordered,
                    sol.price_subtotal as revenue,
                    -- Simple AOV: order total for each line (will average correctly when aggregated)
                    so.amount_total as avg_order_value,
                    -- Count each order once per category
                    CASE 
                        WHEN ROW_NUMBER() OVER (PARTITION BY so.id, COALESCE(parent_pc.name, 'UNCATEGORIZED') ORDER BY sol.id) = 1 
                        THEN 1 
                        ELSE 0 
                    END as order_count,
                    1 as customer_count
                    
                FROM sale_order so
                JOIN sale_order_line sol ON so.id = sol.order_id
                JOIN product_product pp ON sol.product_id = pp.id
                JOIN product_template pt ON pp.product_tmpl_id = pt.id
                JOIN res_partner rp ON so.partner_id = rp.id
                LEFT JOIN product_category pc ON pt.categ_id = pc.id
                LEFT JOIN parent_categories pn ON pc.id = pn.category_id
                LEFT JOIN product_category parent_pc ON pn.parent_category_id = parent_pc.id
                
                -- Spending Tier Matching
                LEFT JOIN spending_tier_lookup tier_match ON so.id = tier_match.order_id
                
                -- Customer Acquisition Source (Marketing Attribution)
                LEFT JOIN wa_marketing_automation_customer_acquisition_source_config acq_src 
                    ON rp.acquisition_source_id = acq_src.id
                    
                -- Sales Source (Business Classification)  
                LEFT JOIN utm_source sales_src ON so.source_id = sales_src.id
                
                WHERE so.state IN ('sale', 'done')
            )
        """)