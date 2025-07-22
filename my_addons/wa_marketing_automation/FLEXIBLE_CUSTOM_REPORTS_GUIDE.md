# Building Flexible Custom Reports in Odoo - Complete Guide

**Based on Performance Analytics Report V2 Implementation**

## Table of Contents
1. [Report Architecture Overview](#report-architecture-overview)
2. [Creating the Base Report Model](#creating-the-base-report-model)
3. [Adding Data Dimensions](#adding-data-dimensions)
4. [Data Population Strategies](#data-population-strategies)
5. [Grouping and Filtering](#grouping-and-filtering)
6. [Date Range Filtering](#date-range-filtering)
7. [Aggregations and Calculations](#aggregations-and-calculations)
8. [Advanced UI Features](#advanced-ui-features)
9. [Performance Optimization](#performance-optimization)
10. [Best Practices and Pitfalls](#best-practices-and-pitfalls)

---

## Report Architecture Overview

### Core Components
Every flexible custom report in Odoo consists of:

1. **Model** (`models/reports/your_report.py`) - Data structure and logic
2. **Views** (`views/reports/your_report_views.xml`) - UI definition
3. **Security** (`security/ir.model.access.csv`) - Access permissions
4. **Menu** (`views/menu.xml`) - Navigation integration

### Design Philosophy
```python
# reports/performance_analytics_report_v2.py
class PerformanceAnalyticsReportV2(models.Model):
    _name = "wa_marketing_automation.performance_analytics_report_v2"
    _description = "Performance Analytics Report V2"
    _auto = False  # No table creation - we'll use SQL view
    _order = "date_order desc, partner_id, order_id"
```

**Key Decisions:**
- `_auto = False` - Uses SQL views for better performance
- `_order` - Default sorting for consistent results
- Descriptive `_name` and `_description` for clarity

---

## Creating the Base Report Model

### 1. Model Declaration
```python
class YourCustomReport(models.Model):
    _name = "your_module.your_report"
    _description = "Your Custom Report Description"
    _auto = False  # SQL view approach
    _order = "date_field desc, primary_dimension"
    
    # Make it a report model
    _table = "your_report_view_name"
```

### 2. Essential Fields
Every report needs these foundation fields:

```python
# Primary Keys and References
id = fields.Id()
partner_id = fields.Many2one('res.partner', string="Customer", readonly=True)
order_id = fields.Many2one('sale.order', string="Order", readonly=True)

# Date Dimensions
date_order = fields.Date(string="Order Date", readonly=True)
year = fields.Char(string="Year", readonly=True)
month = fields.Char(string="Month", readonly=True)
quarter = fields.Char(string="Quarter", readonly=True)

# Categorical Dimensions  
customer_type = fields.Selection([
    ('new', 'New Customer'),
    ('existing', 'Existing Customer'),
], string="Customer Type", readonly=True)

# Numerical Measures
revenue = fields.Float(string="Revenue", readonly=True)
quantity = fields.Float(string="Quantity", readonly=True)
order_count = fields.Float(string="Order Count", readonly=True)
```

---

## Adding Data Dimensions

### 1. Customer Dimensions
```python
# Basic Demographics
customer_age_group = fields.Selection([
    ('gen_z', 'Gen Z (18-26)'),
    ('millennial', 'Millennial (27-42)'),
    ('gen_x', 'Gen X (43-58)'),
    ('boomer', 'Baby Boomer (59-77)'),
    ('silent', 'Silent Generation (78+)'),
], string="Age Group", readonly=True)

# Behavioral Segments
customer_spending_tier = fields.Selection([
    ('l', 'Low Spender'),
    ('m', 'Medium Spender'), 
    ('h', 'High Spender'),
], string="Spending Tier", readonly=True)

# Geographic
partner_country_id = fields.Many2one('res.country', string="Country", readonly=True)
partner_state_id = fields.Many2one('res.country.state', string="State", readonly=True)
```

### 2. Product Dimensions
```python
# Product Information
product_id = fields.Many2one('product.product', string="Product", readonly=True)
product_category_id = fields.Many2one('product.category', string="Category", readonly=True)
product_name = fields.Char(string="Product Name", readonly=True)

# Custom Product Classifications
product_price_range = fields.Selection([
    ('budget', 'Budget ($0-$50)'),
    ('mid', 'Mid-range ($51-$200)'),
    ('premium', 'Premium ($201+)'),
], string="Price Range", readonly=True)
```

### 3. Time Dimensions
```python
# Standard Time Periods
date_order = fields.Date(string="Order Date", readonly=True)
datetime_order = fields.Datetime(string="Order DateTime", readonly=True)

# Computed Time Dimensions
@api.depends('date_order')
def _compute_time_dimensions(self):
    for record in self:
        if record.date_order:
            record.year = str(record.date_order.year)
            record.month = record.date_order.strftime('%Y-%m')
            record.quarter = f"Q{((record.date_order.month-1)//3)+1} {record.date_order.year}"
            record.week = record.date_order.strftime('%Y-W%W')
            record.day_of_week = record.date_order.strftime('%A')

year = fields.Char(compute='_compute_time_dimensions', store=True)
month = fields.Char(compute='_compute_time_dimensions', store=True) 
quarter = fields.Char(compute='_compute_time_dimensions', store=True)
week = fields.Char(compute='_compute_time_dimensions', store=True)
day_of_week = fields.Char(compute='_compute_time_dimensions', store=True)
```

---

## Data Population Strategies

### Strategy 1: SQL View (Recommended for Performance)
```python
@api.model
def init(self):
    """Initialize report data using SQL view"""
    tools.drop_view_if_exists(self.env.cr, self._table)
    self.env.cr.execute(f"""
        CREATE OR REPLACE VIEW {self._table} AS (
            SELECT 
                -- Primary keys
                ROW_NUMBER() OVER (ORDER BY so.date_order, so.partner_id, so.id, sol.id) AS id,
                so.partner_id,
                so.id AS order_id,
                sol.id AS order_line_id,
                
                -- Date dimensions
                so.date_order,
                EXTRACT(year FROM so.date_order)::text AS year,
                TO_CHAR(so.date_order, 'YYYY-MM') AS month,
                CONCAT('Q', EXTRACT(quarter FROM so.date_order), ' ', EXTRACT(year FROM so.date_order)) AS quarter,
                
                -- Customer dimensions
                CASE 
                    WHEN rp.is_new_customer = true THEN 'new'
                    ELSE 'existing'
                END AS customer_type,
                rp.customer_age_group,
                rp.customer_spending_tier,
                
                -- Product dimensions  
                sol.product_id,
                pt.categ_id AS product_category_id,
                pt.name AS product_name,
                
                -- Measures
                sol.price_subtotal AS revenue,
                sol.product_uom_qty AS quantity,
                -- Fractional order count to prevent double-counting
                1.0 / COUNT(sol.id) OVER (PARTITION BY so.id) AS order_count
                
            FROM sale_order so
            JOIN sale_order_line sol ON so.id = sol.order_id
            JOIN res_partner rp ON so.partner_id = rp.id
            JOIN product_product pp ON sol.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
            
            WHERE so.state IN ('sale', 'done')
                AND rp.customer_rank > 0
                AND NOT rp.is_company
                AND so.amount_total > 0  -- Only revenue-generating orders
        )
    """)
```

### Strategy 2: Python-based Data Refresh
```python
@api.model
def refresh_data(self):
    """Refresh report data using Python ORM"""
    # Clear existing data
    self.search([]).unlink()
    
    # Get base data
    orders = self.env['sale.order'].search([
        ('state', 'in', ['sale', 'done']),
        ('amount_total', '>', 0),
    ])
    
    report_data = []
    for order in orders:
        if not order.partner_id.customer_rank or order.partner_id.is_company:
            continue
            
        for line in order.order_line:
            # Calculate fractional order count
            order_count = 1.0 / len(order.order_line)
            
            report_data.append({
                'partner_id': order.partner_id.id,
                'order_id': order.id,
                'order_line_id': line.id,
                'date_order': order.date_order.date(),
                'customer_type': 'new' if order.partner_id.is_new_customer else 'existing',
                'customer_age_group': order.partner_id.customer_age_group,
                'product_id': line.product_id.id,
                'revenue': line.price_subtotal,
                'quantity': line.product_uom_qty,
                'order_count': order_count,
            })
    
    # Batch create for performance
    self.create(report_data)
```

---

## Grouping and Filtering

### 1. Search View with Filters
```xml
<!-- views/reports/your_report_views.xml -->
<record id="view_your_report_search" model="ir.ui.view">
    <field name="name">Your Report Search</field>
    <field name="model">your_module.your_report</field>
    <field name="arch" type="xml">
        <search>
            <!-- Search Fields -->
            <field name="partner_id" string="Customer"/>
            <field name="product_id" string="Product"/>
            <field name="date_order" string="Order Date"/>
            
            <!-- Predefined Filters -->
            <filter name="this_year" string="This Year" 
                domain="[('date_order', '>=', (context_today() - relativedelta(years=0)).strftime('%Y-01-01'))]"/>
            <filter name="last_month" string="Last Month" 
                domain="[('date_order', '>=', (context_today() - relativedelta(months=1)).strftime('%Y-%m-01')),
                        ('date_order', '<', context_today().strftime('%Y-%m-01'))]"/>
            <filter name="new_customers" string="New Customers Only" 
                domain="[('customer_type', '=', 'new')]"/>
            <filter name="high_value" string="High Value Orders" 
                domain="[('revenue', '>', 1000)]"/>
            
            <separator/>
            
            <!-- Group By Options -->
            <group expand="1" string="Group By">
                <filter string="Customer" name="group_customer"
                    context="{'group_by': 'partner_id'}"/>
                <filter string="Customer Type" name="group_customer_type"
                    context="{'group_by': 'customer_type'}"/>
                <filter string="Age Group" name="group_age"
                    context="{'group_by': 'customer_age_group'}"/>
                <filter string="Product Category" name="group_category"
                    context="{'group_by': 'product_category_id'}"/>
                
                <separator/>
                
                <filter string="Year" name="group_year"
                    context="{'group_by': 'year'}"/>
                <filter string="Month" name="group_month"
                    context="{'group_by': 'month'}"/>
                <filter string="Quarter" name="group_quarter"
                    context="{'group_by': 'quarter'}"/>
            </group>
        </search>
    </field>
</record>
```

### 2. Advanced Filter Examples
```xml
<!-- Complex Date Filters -->
<filter name="current_quarter" string="Current Quarter"
    domain="[('quarter', '=', (datetime.datetime.now().month-1)//3+1)]"/>

<!-- Multi-field Filters -->
<filter name="premium_new_customers" string="Premium New Customers"
    domain="[('customer_type', '=', 'new'), ('revenue', '>', 500)]"/>

<!-- Dynamic Filters Using Context -->
<filter name="my_customers" string="My Customers" 
    domain="[('partner_id.user_id', '=', uid)]"/>
```

---

## Date Range Filtering

### 1. Built-in Date Filters
```xml
<!-- Standard Date Range Filters -->
<filter name="today" string="Today"
    domain="[('date_order', '=', context_today())]"/>
<filter name="this_week" string="This Week"
    domain="[('date_order', '>=', (context_today() - relativedelta(weeks=0, weekday=0)).strftime('%Y-%m-%d')),
            ('date_order', '<=', (context_today() + relativedelta(weeks=0, weekday=6)).strftime('%Y-%m-%d'))]"/>
<filter name="this_month" string="This Month"
    domain="[('date_order', '>=', context_today().strftime('%Y-%m-01'))]"/>
<filter name="this_year" string="This Year"
    domain="[('date_order', '>=', context_today().strftime('%Y-01-01'))]"/>
```

### 2. Custom Date Fields
```python
# Add computed date range fields
date_range = fields.Selection([
    ('today', 'Today'),
    ('week', 'This Week'),
    ('month', 'This Month'),
    ('quarter', 'This Quarter'),
    ('year', 'This Year'),
    ('last_30', 'Last 30 Days'),
    ('last_90', 'Last 90 Days'),
], compute='_compute_date_range', store=True)

@api.depends('date_order')
def _compute_date_range(self):
    today = fields.Date.today()
    for record in self:
        if not record.date_order:
            record.date_range = False
            continue
            
        days_diff = (today - record.date_order).days
        
        if days_diff == 0:
            record.date_range = 'today'
        elif days_diff <= 7:
            record.date_range = 'week'  
        elif days_diff <= 30:
            record.date_range = 'month'
        elif days_diff <= 90:
            record.date_range = 'quarter'
        elif days_diff <= 365:
            record.date_range = 'year'
        else:
            record.date_range = False
```

---

## Aggregations and Calculations

### 1. SQL Aggregations
```sql
-- In your SQL view
SELECT 
    partner_id,
    customer_type,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_order_value,
    MIN(date_order) as first_order_date,
    MAX(date_order) as last_order_date,
    
    -- Advanced calculations
    SUM(revenue) / COUNT(DISTINCT order_id) as true_aov,
    COUNT(DISTINCT CASE WHEN date_order >= CURRENT_DATE - INTERVAL '30 days' THEN order_id END) as recent_orders,
    
    -- Percentage calculations
    100.0 * COUNT(DISTINCT order_id) / SUM(COUNT(DISTINCT order_id)) OVER() as order_share_pct
    
FROM your_base_query
GROUP BY partner_id, customer_type
```

### 2. Python Computed Aggregations
```python
# Computed fields for dynamic calculations
total_revenue = fields.Float(
    string="Total Revenue",
    compute="_compute_aggregations", 
    store=True
)

avg_order_value = fields.Float(
    string="Average Order Value",
    compute="_compute_aggregations",
    store=True
)

@api.depends('revenue', 'order_count')
def _compute_aggregations(self):
    for record in self:
        # Group by partner for aggregations
        partner_records = self.search([
            ('partner_id', '=', record.partner_id.id)
        ])
        
        record.total_revenue = sum(partner_records.mapped('revenue'))
        order_count = sum(partner_records.mapped('order_count'))
        record.avg_order_value = record.total_revenue / order_count if order_count else 0
```

### 3. Fractional Counting (Avoid Double-Counting)
```python
# CRITICAL: Prevent double-counting in multi-dimensional reports
@api.depends("order_id")
def _compute_order_count(self):
    """Each order line gets 1/total_lines of the order count"""
    for record in self:
        if not record.order_id:
            record.order_count = 0.0
            continue
            
        # Count ALL lines for this order (across all categories)
        total_order_lines = self.search_count([
            ('order_id', '=', record.order_id.id)
        ])
        
        record.order_count = 1.0 / total_order_lines if total_order_lines > 0 else 1.0
```

---

## Advanced UI Features

### 1. Multiple View Types
```xml
<!-- List View -->
<record id="view_your_report_tree" model="ir.ui.view">
    <field name="name">Your Report List</field>
    <field name="model">your_module.your_report</field>
    <field name="arch" type="xml">
        <list string="Your Report" create="false" delete="false">
            <field name="partner_id"/>
            <field name="customer_type"/>
            <field name="date_order"/>
            <field name="revenue" sum="Total Revenue"/>
            <field name="quantity" sum="Total Quantity"/>
            <field name="order_count" sum="Total Orders"/>
        </list>
    </field>
</record>

<!-- Pivot View -->
<record id="view_your_report_pivot" model="ir.ui.view">
    <field name="name">Your Report Pivot</field>
    <field name="model">your_module.your_report</field>
    <field name="arch" type="xml">
        <pivot string="Your Report Analysis">
            <!-- Default Row Grouping -->
            <field name="customer_type" type="row"/>
            
            <!-- Default Column Grouping -->
            <field name="month" type="col"/>
            
            <!-- Measures -->
            <field name="revenue" type="measure"/>
            <field name="order_count" type="measure"/>
            <field name="quantity" type="measure"/>
        </pivot>
    </field>
</record>

<!-- Graph View -->
<record id="view_your_report_graph" model="ir.ui.view">
    <field name="name">Your Report Graph</field>
    <field name="model">your_module.your_report</field>
    <field name="arch" type="xml">
        <graph string="Revenue Trends" type="line">
            <field name="month" type="row"/>
            <field name="revenue" type="measure"/>
        </graph>
    </field>
</record>
```

### 2. Window Action
```xml
<record id="action_your_report" model="ir.actions.act_window">
    <field name="name">Your Custom Report</field>
    <field name="res_model">your_module.your_report</field>
    <field name="view_mode">pivot,list,graph</field>
    <field name="context">{'search_default_this_year': 1}</field>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">
            Create your first report entry!
        </p>
        <p>
            This report shows comprehensive analytics across customers, products, and time.
        </p>
    </field>
</record>
```

---

## Performance Optimization

### 1. Database Indexing
```python
# Add indexes for frequent filter/group fields
@api.model
def init(self):
    # Create the view first
    super().init()
    
    # Add database indexes for performance
    self.env.cr.execute("""
        CREATE INDEX IF NOT EXISTS idx_your_report_partner_date 
        ON {table} (partner_id, date_order);
        
        CREATE INDEX IF NOT EXISTS idx_your_report_customer_type 
        ON {table} (customer_type);
        
        CREATE INDEX IF NOT EXISTS idx_your_report_date_range 
        ON {table} (date_order, customer_type);
    """.format(table=self._table))
```

### 2. Efficient Data Loading
```python
@api.model
def refresh_data(self):
    """Optimized data refresh with batch processing"""
    # Use SQL for better performance on large datasets
    self.env.cr.execute("DELETE FROM {}".format(self._table))
    
    # Batch insert using SQL
    self.env.cr.execute("""
        INSERT INTO {table} (
            partner_id, order_id, date_order, customer_type, 
            revenue, quantity, order_count
        )
        SELECT 
            so.partner_id,
            so.id,
            so.date_order,
            CASE WHEN rp.is_new_customer THEN 'new' ELSE 'existing' END,
            sol.price_subtotal,
            sol.product_uom_qty,
            1.0 / COUNT(sol.id) OVER (PARTITION BY so.id)
        FROM sale_order so
        JOIN sale_order_line sol ON so.id = sol.order_id  
        JOIN res_partner rp ON so.partner_id = rp.id
        WHERE so.state IN ('sale', 'done')
          AND rp.customer_rank > 0
          AND so.amount_total > 0
    """.format(table=self._table))
```

### 3. Smart Caching
```python
@api.model 
def _is_data_stale(self):
    """Check if report data needs refresh"""
    last_report_record = self.search([], order='write_date desc', limit=1)
    if not last_report_record:
        return True
        
    # Check if any source data changed since last update  
    last_order = self.env['sale.order'].search([
        ('state', 'in', ['sale', 'done'])
    ], order='write_date desc', limit=1)
    
    return last_order.write_date > last_report_record.write_date
```

---

## Best Practices and Pitfalls

### ✅ DO's

**1. Use SQL Views for Large Datasets**
```python
# Good - SQL view for performance
_auto = False
_table = "your_report_view"

@api.model  
def init(self):
    tools.drop_view_if_exists(self.env.cr, self._table)
    self.env.cr.execute(f"CREATE VIEW {self._table} AS ...")
```

**2. Prevent Double-Counting**
```python
# Good - Fractional counting
order_count = 1.0 / COUNT(sol.id) OVER (PARTITION BY so.id)
```

**3. Add Proper Indexes**
```python
# Good - Index on filter/group fields
CREATE INDEX idx_report_partner_date ON report_table (partner_id, date_order);
```

**4. Use Meaningful Field Names**
```python
# Good - Clear field names
customer_acquisition_date = fields.Date(string="Customer Acquisition Date")
avg_order_value = fields.Float(string="Average Order Value")
```

### ❌ DON'Ts

**1. Don't Use Heuristic Calculations**
```python
# Bad - Indirect assumptions
mobile_usage = "orders under $50 on weekends"  # Wrong!

# Good - Direct data sources  
mobile_usage = website_sessions.filter(device_type='mobile')
```

**2. Don't Ignore Performance**
```python
# Bad - Slow Python loops
for partner in self.env['res.partner'].search([]):
    for order in partner.sale_order_ids:
        # Lots of processing...

# Good - Single SQL query
self.env.cr.execute("SELECT ... FROM ... WHERE ... GROUP BY ...")
```

**3. Don't Create Rigid Reports**
```python
# Bad - Hard-coded filters
domain = [('date_order', '>=', '2024-01-01')]

# Good - Dynamic filters
domain = [('date_order', '>=', context.get('date_from', fields.Date.today()))]
```

**4. Don't Skip Data Validation**
```python
# Bad - No validation
revenue = fields.Float()

# Good - With validation
revenue = fields.Float(
    string="Revenue",
    help="Total revenue in company currency",
    digits=(16, 2)  # Precision control
)
```

### 🔧 Troubleshooting Common Issues

**1. "RecordSet is empty" Errors**
```python
# Check for empty results
records = self.search(domain)
if not records:
    return {'type': 'ir.actions.act_window_close'}
```

**2. Performance Issues**
```python
# Add logging to identify bottlenecks
import logging
_logger = logging.getLogger(__name__)

start_time = time.time()
result = self.expensive_operation()
_logger.info(f"Operation took {time.time() - start_time:.2f}s")
```

**3. Data Inconsistencies**
```python
# Add data validation
@api.constrains('revenue', 'quantity')  
def _check_data_consistency(self):
    for record in self:
        if record.revenue < 0:
            raise ValidationError("Revenue cannot be negative")
```

---

## Complete Implementation Checklist

### Model (`models/reports/your_report.py`)
- [ ] Define `_name`, `_description`, `_auto = False`
- [ ] Add all dimension fields with proper types
- [ ] Add measure fields with aggregation support
- [ ] Implement `init()` method with SQL view
- [ ] Add computed fields for complex calculations
- [ ] Include data validation and constraints

### Views (`views/reports/your_report_views.xml`)
- [ ] Create search view with filters and grouping
- [ ] Define list view with summable fields
- [ ] Add pivot view for analysis
- [ ] Include graph view for visualization
- [ ] Configure window action with proper context

### Security (`security/ir.model.access.csv`)
- [ ] Add read access for relevant user groups
- [ ] Restrict create/write/unlink as needed

### Menu (`views/menu.xml`)
- [ ] Add menu item in appropriate location
- [ ] Set proper sequence and permissions

### Performance
- [ ] Add database indexes for filter fields
- [ ] Optimize SQL queries with proper JOINs
- [ ] Implement efficient data refresh mechanism
- [ ] Test with large datasets

This guide provides a complete foundation for building flexible, performant custom reports in Odoo based on proven patterns from our Performance Analytics Report V2 implementation.