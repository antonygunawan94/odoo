# 🎯 **Complete Guide to Custom Reports using SQL Views in Odoo 18.0**

## 📋 **Table of Contents**
1. [Why SQL Views?](#why-sql-views)
2. [Quick Start](#quick-start)
3. [Step-by-Step Implementation](#step-by-step-implementation)
4. [Working Example](#working-example)
5. [Advanced Patterns](#advanced-patterns)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Performance Tips](#performance-tips)

---

## 🤔 **Why SQL Views?**

### **The Reality Check**
After extensive research, **SQL Views are the ONLY well-documented, reliable approach** for custom reports in Odoo 18.0:

| **Approach** | **Documentation** | **Reliability** | **Performance** | **Control** |
|--------------|-------------------|-----------------|-----------------|-------------|
| **SQL Views** | ✅ Excellent | ✅ Production-ready | ✅ Fast | ✅ Full |
| **Spreadsheet Dashboards** | ❌ Almost none | ⚠️ Undocumented APIs | ⚠️ Unknown | ❌ Limited |
| **Dynamic Dashboards** | ⚠️ Third-party only | ⚠️ Module dependent | ⚠️ Variable | ⚠️ Limited |

### **When to Use SQL Views**
✅ **Perfect for:**
- Complex multi-table analytics
- Performance-critical reports
- Production systems requiring reliability
- Reports needing version control
- Data aggregation from multiple sources

❌ **Not ideal for:**
- Simple single-table reports (use standard views)
- Real-time data that changes frequently
- Reports requiring frequent user modifications

---

## ⚡ **Quick Start**

### **1. Create the Model File**
```bash
# In your module/models/ directory
touch simple_report.py
```

### **2. Basic SQL View Structure**
```python
from odoo import api, fields, models, tools

class SimpleReport(models.Model):
    _name = 'your_module.simple_report'
    _description = 'Simple Report'
    _auto = False  # 🔑 KEY: Don't create database table
    _rec_name = 'name'
    _order = 'date desc'

    # Define your fields
    name = fields.Char(string='Name', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    count = fields.Integer(string='Count', readonly=True)

    @api.model
    def init(self):
        """🔑 KEY: This creates the PostgreSQL view"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () AS id,  -- 🔑 Required ID field
                    your_field AS name,
                    your_date AS date,
                    COUNT(*) AS count
                FROM your_table
                GROUP BY your_field, your_date
            )
        """ % self._table)
```

### **3. Add to Module**
```python
# In models/__init__.py
from . import simple_report

# In security/ir.model.access.csv
access_simple_report,access.simple_report,model_your_module_simple_report,base.group_user,0,0,1,0
```

---

## 📝 **Step-by-Step Implementation**

### **Step 1: Plan Your Report**

**Define Requirements:**
```python
# Example: Campaign Performance Report
# Data Sources: campaigns, API logs, CRM leads
# Metrics: messages sent, failed, response rates
# Grouping: by campaign, date, status
```

### **Step 2: Create the Model**

**File: `models/campaign_report.py`**
```python
from odoo import api, fields, models, tools

class CampaignReport(models.Model):
    """Custom campaign performance report using SQL views"""
    _name = 'your_module.campaign_report'
    _description = 'Campaign Performance Report'
    _auto = False  # Don't create table automatically
    _rec_name = 'campaign_name'
    _order = 'date desc'

    # 🔑 CRITICAL: All fields must be readonly=True
    campaign_id = fields.Many2one('your_module.campaign', string='Campaign', readonly=True)
    campaign_name = fields.Char(string='Campaign Name', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('finished', 'Finished'),
    ], string='Status', readonly=True)
    
    # Metrics
    messages_sent = fields.Integer(string='Messages Sent', readonly=True)
    messages_failed = fields.Integer(string='Messages Failed', readonly=True)
    success_rate = fields.Float(string='Success Rate (%)', readonly=True)

    @api.model
    def init(self):
        """Create the PostgreSQL view"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () AS id,  -- 🔑 REQUIRED: Unique ID
                    c.id AS campaign_id,
                    c.name AS campaign_name,
                    c.create_date::date AS date,
                    c.state AS state,
                    
                    -- Calculate metrics using subqueries
                    COALESCE((
                        SELECT COUNT(*) 
                        FROM your_api_log_table l 
                        WHERE l.campaign_id = c.id AND l.status = 'success'
                    ), 0) AS messages_sent,
                    
                    COALESCE((
                        SELECT COUNT(*) 
                        FROM your_api_log_table l 
                        WHERE l.campaign_id = c.id AND l.status = 'error'
                    ), 0) AS messages_failed,
                    
                    -- Calculate percentage
                    CASE 
                        WHEN COALESCE((SELECT COUNT(*) FROM your_api_log_table WHERE campaign_id = c.id), 0) > 0
                        THEN (COALESCE((SELECT COUNT(*) FROM your_api_log_table WHERE campaign_id = c.id AND status = 'success'), 0)::float / 
                              COALESCE((SELECT COUNT(*) FROM your_api_log_table WHERE campaign_id = c.id), 1)::float) * 100
                        ELSE 0
                    END AS success_rate
                    
                FROM your_campaign_table c
                WHERE c.state != 'draft'
            )
        """ % self._table)
```

### **Step 3: Create Views**

**File: `views/campaign_report_views.xml`**
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Search View -->
        <record id="view_campaign_report_search" model="ir.ui.view">
            <field name="name">campaign.report.search</field>
            <field name="model">your_module.campaign_report</field>
            <field name="arch" type="xml">
                <search>
                    <field name="campaign_name"/>
                    <field name="state"/>
                    <field name="date"/>
                    
                    <!-- Filters -->
                    <filter name="filter_running" string="Running" domain="[('state', '=', 'running')]"/>
                    <filter name="filter_finished" string="Finished" domain="[('state', '=', 'finished')]"/>
                    <filter name="filter_with_failures" string="Has Failures" domain="[('messages_failed', '>', 0)]"/>
                    
                    <!-- Group By -->
                    <group expand="0" string="Group By">
                        <filter name="group_campaign" string="Campaign" domain="[]" context="{'group_by': 'campaign_name'}"/>
                        <filter name="group_state" string="Status" domain="[]" context="{'group_by': 'state'}"/>
                        <filter name="group_date" string="Date" domain="[]" context="{'group_by': 'date'}"/>
                    </group>
                </search>
            </field>
        </record>

        <!-- List View -->
        <record id="view_campaign_report_list" model="ir.ui.view">
            <field name="name">campaign.report.list</field>
            <field name="model">your_module.campaign_report</field>
            <field name="arch" type="xml">
                <list string="Campaign Report" create="false" edit="false" delete="false"
                      decoration-success="success_rate > 90"
                      decoration-warning="messages_failed > 0">
                    <field name="campaign_name"/>
                    <field name="date"/>
                    <field name="state" widget="badge"/>
                    <field name="messages_sent"/>
                    <field name="messages_failed"/>
                    <field name="success_rate" widget="percentage"/>
                </list>
            </field>
        </record>

        <!-- Pivot View -->
        <record id="view_campaign_report_pivot" model="ir.ui.view">
            <field name="name">campaign.report.pivot</field>
            <field name="model">your_module.campaign_report</field>
            <field name="arch" type="xml">
                <pivot string="Campaign Analysis">
                    <field name="state" type="row"/>
                    <field name="date" type="col" interval="month"/>
                    <field name="messages_sent" type="measure"/>
                    <field name="success_rate" type="measure"/>
                </pivot>
            </field>
        </record>

        <!-- Graph View -->
        <record id="view_campaign_report_graph" model="ir.ui.view">
            <field name="name">campaign.report.graph</field>
            <field name="model">your_module.campaign_report</field>
            <field name="arch" type="xml">
                <graph string="Campaign Performance" type="line">
                    <field name="date" type="row"/>
                    <field name="success_rate" type="measure"/>
                </graph>
            </field>
        </record>

        <!-- Action -->
        <record id="action_campaign_report" model="ir.actions.act_window">
            <field name="name">Campaign Report</field>
            <field name="res_model">your_module.campaign_report</field>
            <field name="view_mode">list,pivot,graph</field>
            <field name="search_view_id" ref="view_campaign_report_search"/>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    No campaign data found!
                </p>
                <p>Create some campaigns to see performance data here.</p>
            </field>
        </record>

        <!-- Menu Item -->
        <menuitem id="menu_campaign_report"
                  name="Campaign Report"
                  parent="your_base_menu"
                  action="action_campaign_report"
                  sequence="10"/>
    </data>
</odoo>
```

### **Step 4: Add Security**

**File: `security/ir.model.access.csv`**
```csv
id,name,model_id:id,group_id:id,perm_create,perm_write,perm_read,perm_unlink
access_campaign_report,access.campaign_report,model_your_module_campaign_report,base.group_user,0,0,1,0
```

### **Step 5: Update Module Files**

**Add to `models/__init__.py`:**
```python
from . import campaign_report
```

**Add to `__manifest__.py`:**
```python
"data": [
    "security/ir.model.access.csv",
    "views/campaign_report_views.xml",
    # ... other files
],
```

---

## 🔍 **Working Example**

Our module includes a complete working example: **`simple_campaign_report.py`**

### **File Structure:**
```
my_addons/wa_marketing_automation/
├── models/
│   └── simple_campaign_report.py          # ✅ Working example
├── views/
│   └── simple_campaign_report_views.xml   # ✅ Complete views
├── security/
│   └── ir.model.access.csv               # ✅ Security rules
└── SQL_VIEWS_GUIDE.md                    # ✅ This guide
```

### **Test the Example:**
1. **Start Odoo:** `make run-dev`
2. **Navigate to:** `WhatsApp Marketing Automation → Reports → Simple Campaign Report`
3. **Explore:** List, pivot, and graph views with real data

### **Key Features Demonstrated:**
- ✅ PostgreSQL view creation
- ✅ Multi-table data aggregation
- ✅ Computed fields (percentages)
- ✅ Search filters and grouping
- ✅ Multiple view types
- ✅ Proper security model

---

## 🚀 **Advanced Patterns**

### **Pattern 1: Complex Aggregations**
```sql
-- Multiple aggregation levels
SELECT
    row_number() OVER () AS id,
    partner_id,
    SUM(amount_total) as total_revenue,
    COUNT(DISTINCT id) as order_count,
    AVG(amount_total) as avg_order_value,
    -- Percentile calculations
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount_total) as median_order
FROM sale_order
WHERE state = 'sale'
GROUP BY partner_id
```

### **Pattern 2: Date-Based Analysis**
```sql
-- Time-based grouping with date functions
SELECT
    row_number() OVER () AS id,
    DATE_TRUNC('month', create_date) as month,
    EXTRACT(year FROM create_date) as year,
    EXTRACT(quarter FROM create_date) as quarter,
    COUNT(*) as record_count
FROM your_table
GROUP BY DATE_TRUNC('month', create_date), EXTRACT(year FROM create_date), EXTRACT(quarter FROM create_date)
```

### **Pattern 3: Conditional Aggregations**
```sql
-- Using CASE for conditional metrics
SELECT
    row_number() OVER () AS id,
    campaign_id,
    COUNT(*) as total_messages,
    COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_messages,
    COUNT(CASE WHEN status = 'error' THEN 1 END) as failed_messages,
    COUNT(CASE WHEN response_received = true THEN 1 END) as responses
FROM message_log
GROUP BY campaign_id
```

### **Pattern 4: Window Functions**
```sql
-- Running totals and rankings
SELECT
    row_number() OVER () AS id,
    partner_id,
    order_date,
    amount_total,
    -- Running total
    SUM(amount_total) OVER (PARTITION BY partner_id ORDER BY order_date) as running_total,
    -- Ranking
    ROW_NUMBER() OVER (PARTITION BY partner_id ORDER BY amount_total DESC) as revenue_rank
FROM sale_order
WHERE state = 'sale'
```

### **Pattern 5: Cross-Module Data**
```sql
-- Joining data from multiple modules
SELECT
    row_number() OVER () AS id,
    p.name as partner_name,
    p.email as partner_email,
    COUNT(DISTINCT so.id) as order_count,
    COUNT(DISTINCT ml.id) as message_count,
    COUNT(DISTINCT cl.id) as lead_count
FROM res_partner p
LEFT JOIN sale_order so ON so.partner_id = p.id AND so.state = 'sale'
LEFT JOIN mail_message ml ON ml.res_id = p.id AND ml.model = 'res.partner'
LEFT JOIN crm_lead cl ON cl.partner_id = p.id
WHERE p.is_company = false
GROUP BY p.id, p.name, p.email
```

---

## ✅ **Best Practices**

### **1. Model Design**
```python
# ✅ DO: Always use these patterns
class MyReport(models.Model):
    _auto = False                    # Never create table
    _rec_name = 'meaningful_field'   # Set display name field
    _order = 'logical_order'         # Default sort order
    
    # All fields readonly
    field1 = fields.Char(readonly=True)
    field2 = fields.Integer(readonly=True)

# ❌ DON'T: Never do these
class BadReport(models.Model):
    _auto = True                     # ❌ Will create unnecessary table
    field1 = fields.Char()           # ❌ Not readonly
    
    # ❌ Missing init() method
```

### **2. SQL Best Practices**
```sql
-- ✅ DO: Always include row_number() for ID
SELECT row_number() OVER () AS id, ...

-- ✅ DO: Use COALESCE for null handling
COALESCE(SUM(amount), 0) as total_amount

-- ✅ DO: Use proper table aliases
FROM sale_order so
JOIN res_partner p ON p.id = so.partner_id

-- ❌ DON'T: Never hardcode IDs
WHERE company_id = 1  -- ❌ Use dynamic company lookup

-- ✅ DO: Use dynamic company lookup
WHERE company_id = (SELECT id FROM res_company LIMIT 1)
```

### **3. Performance Optimization**
```sql
-- ✅ DO: Use efficient WHERE clauses
WHERE so.state = 'sale'              -- Filter early
AND so.create_date >= '2024-01-01'   -- Date filters

-- ✅ DO: Use EXISTS for better performance
WHERE EXISTS (
    SELECT 1 FROM related_table r 
    WHERE r.foreign_key = main.id
)

-- ❌ DON'T: Avoid inefficient patterns
WHERE EXTRACT(year FROM date_field) = 2024  -- ❌ Prevents index usage
```

### **4. Field Naming**
```python
# ✅ DO: Use descriptive field names
messages_sent = fields.Integer('Messages Sent', readonly=True)
success_rate_percent = fields.Float('Success Rate (%)', readonly=True)

# ❌ DON'T: Use cryptic names
msg_cnt = fields.Integer(readonly=True)  # ❌ Unclear
rate = fields.Float(readonly=True)       # ❌ Ambiguous
```

### **5. View Design**
```xml
<!-- ✅ DO: Disable editing for reports -->
<list create="false" edit="false" delete="false">

<!-- ✅ DO: Use meaningful decorations -->
<list decoration-success="success_rate > 90"
      decoration-warning="messages_failed > 0">

<!-- ✅ DO: Provide helpful filters -->
<filter name="recent" string="Last 30 Days" 
        domain="[('date', '>=', (context_today() - relativedelta(days=30)).strftime('%Y-%m-%d'))]"/>
```

---

## 🐛 **Troubleshooting**

### **Common Error 1: Missing ID Field**
```
ERROR: column "id" does not exist
```
**Solution:**
```sql
-- ✅ Always include this line
SELECT row_number() OVER () AS id, ...
```

### **Common Error 2: Field Not Readonly**
```
ERROR: Field 'field_name' is not readonly in report model
```
**Solution:**
```python
# ✅ All fields must be readonly
field_name = fields.Char(readonly=True)
```

### **Common Error 3: View Already Exists**
```
ERROR: relation "your_table_name" already exists
```
**Solution:**
```python
# ✅ Always drop existing view first
tools.drop_view_if_exists(self.env.cr, self._table)
```

### **Common Error 4: SQL Syntax Errors**
```
ERROR: syntax error at or near "FROM"
```
**Solution:**
```python
# ✅ Use proper string formatting
self.env.cr.execute("""
    CREATE OR REPLACE VIEW %s AS (
        SELECT ...
    )
""" % self._table)
```

### **Common Error 5: Permission Denied**
```
ERROR: permission denied for table
```
**Solution:**
```csv
# ✅ Add proper security rule
access_report,access.report,model_module_report,base.group_user,0,0,1,0
```

---

## ⚡ **Performance Tips**

### **1. Index Usage**
```sql
-- ✅ DO: Structure queries to use existing indexes
WHERE create_date >= '2024-01-01'    -- Uses date index
AND state = 'sale'                   -- Uses state index

-- ❌ DON'T: Break index usage
WHERE EXTRACT(year FROM create_date) = 2024  -- Breaks index
```

### **2. Subquery vs JOIN**
```sql
-- ✅ BETTER: Use JOINs for multiple values
SELECT p.name, COUNT(so.id) as order_count
FROM res_partner p
LEFT JOIN sale_order so ON so.partner_id = p.id
GROUP BY p.id, p.name

-- ⚠️ OK: Use subqueries for single values
SELECT p.name,
    (SELECT COUNT(*) FROM sale_order WHERE partner_id = p.id) as order_count
FROM res_partner p
```

### **3. Limit Data Range**
```sql
-- ✅ DO: Always filter by date ranges
WHERE create_date >= CURRENT_DATE - INTERVAL '1 year'

-- ✅ DO: Use appropriate LIMIT for large datasets
ORDER BY create_date DESC
LIMIT 10000
```

### **4. Monitor Query Performance**
```python
# ✅ DO: Test with realistic data volumes
# ✅ DO: Check query execution time in PostgreSQL logs
# ✅ DO: Use EXPLAIN ANALYZE for complex queries
```

---

## 🎯 **Summary**

### **Why SQL Views Win**
1. **✅ Well-documented** - Official Odoo support
2. **✅ Production-ready** - Used by Odoo core modules
3. **✅ High performance** - Pure PostgreSQL optimization
4. **✅ Full control** - Custom SQL for any requirement
5. **✅ Version controllable** - Python code in git

### **Quick Checklist**
- [ ] Model uses `_auto = False`
- [ ] All fields are `readonly=True`
- [ ] SQL includes `row_number() OVER () AS id`
- [ ] Uses `tools.drop_view_if_exists()`
- [ ] Security rules are read-only: `0,0,1,0`
- [ ] Views disable editing: `create="false" edit="false" delete="false"`

### **Next Steps**
1. **Study the working example** in `simple_campaign_report.py`
2. **Copy and modify** for your specific needs
3. **Test with real data** to validate performance
4. **Add to production** with confidence

**Happy reporting!** 🚀

---

*This guide represents the most reliable and well-documented approach to custom reporting in Odoo 18.0 as of July 2025.*