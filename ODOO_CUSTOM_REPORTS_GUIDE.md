# Odoo Custom Reports Development Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Report Types in Odoo](#report-types-in-odoo)
3. [Report Architecture](#report-architecture)
4. [Creating PDF Reports](#creating-pdf-reports)
5. [Creating Excel Reports](#creating-excel-reports)
6. [Advanced Report Features](#advanced-report-features)
7. [Practical Examples](#practical-examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Resources](#resources)

---

## Introduction

Odoo provides a powerful reporting system that allows developers to create custom reports for business needs. This guide covers everything from basic PDF reports to advanced Excel reports with charts and dynamic data.

### What You'll Learn
- How to create custom PDF reports using QWeb templates
- How to generate Excel reports with formatting
- How to add custom report actions and buttons
- How to implement dynamic data filtering
- Best practices for report development

### Prerequisites
- Basic knowledge of Odoo development
- Understanding of Python and XML
- Familiarity with QWeb templating system

---

## Report Types in Odoo

### 1. **QWeb PDF Reports**
- **Purpose**: Generate PDF documents (invoices, receipts, contracts)
- **Technology**: QWeb templating engine + wkhtmltopdf
- **Use Cases**: Business documents, certificates, labels

### 2. **QWeb HTML Reports**
- **Purpose**: Web-based reports viewed in browser
- **Technology**: QWeb templating engine
- **Use Cases**: Dashboards, data tables, preview reports

### 3. **Excel Reports**
- **Purpose**: Spreadsheet reports with calculations
- **Technology**: Python libraries (xlsxwriter, openpyxl)
- **Use Cases**: Financial reports, data analysis, bulk data export

### 4. **Custom Python Reports**
- **Purpose**: Complex data processing and custom formats
- **Technology**: Pure Python with custom logic
- **Use Cases**: Custom file formats, API integrations

---

## Report Architecture

### Core Components

```
Custom Report Structure:
├── models/
│   ├── __init__.py
│   └── report_model.py          # Report model (optional)
├── reports/
│   ├── __init__.py
│   ├── report_controller.py     # Report generation logic
│   └── report_template.xml      # QWeb template
├── data/
│   └── report_data.xml          # Report registration
└── __manifest__.py              # Module dependencies
```

### Key Models and Classes

1. **`ir.actions.report`**: Defines report metadata
2. **`AbstractModel`**: Base class for report models
3. **`@api.model`**: Decorators for report methods
4. **QWeb templates**: HTML/XML templates for rendering

---

## Creating PDF Reports

### Step 1: Define Report Action

Create a report action in `data/report_data.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Report Action Definition -->
        <record id="action_customer_report" model="ir.actions.report">
            <field name="name">Customer Report</field>
            <field name="model">res.partner</field>
            <field name="report_type">qweb-pdf</field>
            <field name="report_name">your_module.customer_report_template</field>
            <field name="report_file">your_module.customer_report_template</field>
            <field name="binding_model_id" ref="base.model_res_partner"/>
            <field name="binding_type">report</field>
            <field name="paperformat_id" ref="base.paperformat_euro"/>
        </record>
    </data>
</odoo>
```

### Step 2: Create Report Model

Create `models/customer_report.py`:

```python
from odoo import api, models
from datetime import datetime


class CustomerReport(models.AbstractModel):
    _name = 'report.your_module.customer_report_template'
    _description = 'Customer Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Generate report data for the template
        """
        # Get the record(s) for which report is generated
        customers = self.env['res.partner'].browse(docids)
        
        # Prepare additional data
        report_data = {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': customers,
            'time': datetime.now(),
            'get_total_invoices': self._get_total_invoices,
            'get_customer_stats': self._get_customer_stats,
        }
        
        return report_data

    def _get_total_invoices(self, partner_id):
        """Calculate total invoices for a customer"""
        invoices = self.env['account.move'].search([
            ('partner_id', '=', partner_id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')
        ])
        return sum(invoices.mapped('amount_total'))

    def _get_customer_stats(self, partner_id):
        """Get customer statistics"""
        partner = self.env['res.partner'].browse(partner_id)
        return {
            'total_orders': len(partner.sale_order_ids),
            'total_invoices': len(partner.invoice_ids),
            'last_order_date': partner.sale_order_ids[-1].date_order if partner.sale_order_ids else None,
        }
```

### Step 3: Create QWeb Template

Create `reports/customer_report_template.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="customer_report_template">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="customer">
                <t t-call="web.external_layout">
                    <div class="page">
                        <!-- Header -->
                        <div class="oe_structure">
                            <div class="row">
                                <div class="col-6">
                                    <h3>Customer Report</h3>
                                </div>
                                <div class="col-6 text-right">
                                    <p>Generated: <span t-esc="time.strftime('%Y-%m-%d %H:%M:%S')"/></p>
                                </div>
                            </div>
                        </div>

                        <!-- Customer Information -->
                        <div class="row mt-4">
                            <div class="col-12">
                                <h4>Customer Information</h4>
                                <table class="table table-bordered">
                                    <tr>
                                        <td><strong>Name:</strong></td>
                                        <td t-field="customer.name"/>
                                    </tr>
                                    <tr>
                                        <td><strong>Email:</strong></td>
                                        <td t-field="customer.email"/>
                                    </tr>
                                    <tr>
                                        <td><strong>Phone:</strong></td>
                                        <td t-field="customer.phone"/>
                                    </tr>
                                    <tr>
                                        <td><strong>Address:</strong></td>
                                        <td>
                                            <div t-field="customer.street"/>
                                            <div t-field="customer.street2"/>
                                            <div>
                                                <span t-field="customer.city"/>, 
                                                <span t-field="customer.state_id.name"/> 
                                                <span t-field="customer.zip"/>
                                            </div>
                                            <div t-field="customer.country_id.name"/>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </div>

                        <!-- Customer Statistics -->
                        <div class="row mt-4">
                            <div class="col-12">
                                <h4>Statistics</h4>
                                <t t-set="stats" t-value="get_customer_stats(customer.id)"/>
                                <table class="table table-bordered">
                                    <tr>
                                        <td><strong>Total Orders:</strong></td>
                                        <td t-esc="stats['total_orders']"/>
                                    </tr>
                                    <tr>
                                        <td><strong>Total Invoices:</strong></td>
                                        <td t-esc="stats['total_invoices']"/>
                                    </tr>
                                    <tr>
                                        <td><strong>Total Invoice Amount:</strong></td>
                                        <td t-esc="get_total_invoices(customer.id)" t-options='{"widget": "monetary", "display_currency": customer.currency_id}'/>
                                    </tr>
                                    <tr t-if="stats['last_order_date']">
                                        <td><strong>Last Order Date:</strong></td>
                                        <td t-esc="stats['last_order_date']" t-options='{"widget": "date"}'/>
                                    </tr>
                                </table>
                            </div>
                        </div>

                        <!-- Recent Orders -->
                        <div class="row mt-4">
                            <div class="col-12">
                                <h4>Recent Orders</h4>
                                <table class="table table-sm table-bordered">
                                    <thead>
                                        <tr>
                                            <th>Order #</th>
                                            <th>Date</th>
                                            <th>Amount</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <t t-foreach="customer.sale_order_ids[:5]" t-as="order">
                                            <tr>
                                                <td t-field="order.name"/>
                                                <td t-field="order.date_order" t-options='{"widget": "date"}'/>
                                                <td t-field="order.amount_total" t-options='{"widget": "monetary", "display_currency": order.currency_id}'/>
                                                <td t-field="order.state"/>
                                            </tr>
                                        </t>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Footer -->
                        <div class="oe_structure">
                            <div class="row">
                                <div class="col-12 text-center mt-4">
                                    <hr/>
                                    <p>This report was generated automatically by the system.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>
```

### Step 4: Add Report Button to Form View

Create `views/customer_views.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_partner_form_report_button" model="ir.ui.view">
        <field name="name">res.partner.form.report.button</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_form"/>
        <field name="arch" type="xml">
            <div class="oe_button_box" position="inside">
                <button name="%(action_customer_report)d" 
                        type="action" 
                        class="oe_stat_button" 
                        icon="fa-file-pdf-o">
                    <div class="o_field_widget o_stat_info">
                        <span class="o_stat_text">Customer</span>
                        <span class="o_stat_text">Report</span>
                    </div>
                </button>
            </div>
        </field>
    </record>
</odoo>
```

---

## Creating Excel Reports

### Step 1: Install Required Dependencies

Add to `__manifest__.py`:

```python
{
    'name': 'Custom Reports',
    'depends': ['base', 'account', 'sale'],
    'external_dependencies': {
        'python': ['xlsxwriter'],
    },
    # ... other fields
}
```

### Step 2: Create Excel Report Model

Create `models/excel_report.py`:

```python
import io
import base64
from datetime import datetime
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


class CustomerExcelReport(models.TransientModel):
    _name = 'customer.excel.report'
    _description = 'Customer Excel Report Generator'

    # Filter fields
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    partner_ids = fields.Many2many('res.partner', string='Customers')
    include_orders = fields.Boolean('Include Orders', default=True)
    include_invoices = fields.Boolean('Include Invoices', default=True)
    
    # Output fields
    excel_file = fields.Binary('Excel File', readonly=True)
    file_name = fields.Char('File Name', readonly=True)

    def action_generate_report(self):
        """Generate Excel report"""
        if not xlsxwriter:
            raise UserError(_('Please install xlsxwriter: pip install xlsxwriter'))

        # Create Excel file in memory
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Define formats
        formats = self._get_excel_formats(workbook)
        
        # Generate worksheets
        self._create_summary_sheet(workbook, formats)
        if self.include_orders:
            self._create_orders_sheet(workbook, formats)
        if self.include_invoices:
            self._create_invoices_sheet(workbook, formats)
        
        # Close workbook and save
        workbook.close()
        output.seek(0)
        
        # Encode to base64
        excel_data = base64.b64encode(output.read())
        
        # Update record
        self.write({
            'excel_file': excel_data,
            'file_name': f'customer_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        })
        
        # Return download action
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model={self._name}&id={self.id}&field=excel_file&filename_field=file_name&download=true',
            'target': 'self',
        }

    def _get_excel_formats(self, workbook):
        """Define Excel cell formats"""
        return {
            'header': workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#4CAF50',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            }),
            'subheader': workbook.add_format({
                'bold': True,
                'font_size': 10,
                'bg_color': '#E8F5E8',
                'border': 1,
                'align': 'center'
            }),
            'currency': workbook.add_format({
                'num_format': '$#,##0.00',
                'border': 1,
                'align': 'right'
            }),
            'date': workbook.add_format({
                'num_format': 'yyyy-mm-dd',
                'border': 1,
                'align': 'center'
            }),
            'number': workbook.add_format({
                'num_format': '#,##0',
                'border': 1,
                'align': 'right'
            }),
            'text': workbook.add_format({
                'border': 1,
                'text_wrap': True,
                'valign': 'top'
            }),
            'total': workbook.add_format({
                'bold': True,
                'num_format': '$#,##0.00',
                'border': 1,
                'bg_color': '#F0F0F0',
                'align': 'right'
            })
        }

    def _create_summary_sheet(self, workbook, formats):
        """Create summary worksheet"""
        sheet = workbook.add_worksheet('Summary')
        
        # Set column widths
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 15)
        
        # Header
        sheet.merge_range('A1:E1', 'Customer Report Summary', formats['header'])
        
        # Report info
        row = 2
        sheet.write(row, 0, 'Report Date:', formats['subheader'])
        sheet.write(row, 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), formats['text'])
        
        row += 1
        sheet.write(row, 0, 'Period:', formats['subheader'])
        sheet.write(row, 1, f"{self.date_from} to {self.date_to}", formats['text'])
        
        # Data headers
        row += 2
        headers = ['Customer Name', 'Total Orders', 'Total Invoices', 'Order Amount', 'Invoice Amount']
        for col, header in enumerate(headers):
            sheet.write(row, col, header, formats['subheader'])
        
        # Get data
        customers = self.partner_ids if self.partner_ids else self.env['res.partner'].search([('is_company', '=', False)])
        
        row += 1
        total_orders = 0
        total_invoices = 0
        total_order_amount = 0
        total_invoice_amount = 0
        
        for customer in customers:
            # Get customer data
            orders = self.env['sale.order'].search([
                ('partner_id', '=', customer.id),
                ('date_order', '>=', self.date_from),
                ('date_order', '<=', self.date_to)
            ])
            
            invoices = self.env['account.move'].search([
                ('partner_id', '=', customer.id),
                ('move_type', '=', 'out_invoice'),
                ('invoice_date', '>=', self.date_from),
                ('invoice_date', '<=', self.date_to)
            ])
            
            order_amount = sum(orders.mapped('amount_total'))
            invoice_amount = sum(invoices.mapped('amount_total'))
            
            # Write row
            sheet.write(row, 0, customer.name, formats['text'])
            sheet.write(row, 1, len(orders), formats['number'])
            sheet.write(row, 2, len(invoices), formats['number'])
            sheet.write(row, 3, order_amount, formats['currency'])
            sheet.write(row, 4, invoice_amount, formats['currency'])
            
            # Update totals
            total_orders += len(orders)
            total_invoices += len(invoices)
            total_order_amount += order_amount
            total_invoice_amount += invoice_amount
            
            row += 1
        
        # Totals row
        sheet.write(row, 0, 'TOTAL', formats['total'])
        sheet.write(row, 1, total_orders, formats['total'])
        sheet.write(row, 2, total_invoices, formats['total'])
        sheet.write(row, 3, total_order_amount, formats['total'])
        sheet.write(row, 4, total_invoice_amount, formats['total'])

    def _create_orders_sheet(self, workbook, formats):
        """Create orders worksheet"""
        sheet = workbook.add_worksheet('Orders')
        
        # Set column widths
        sheet.set_column('A:A', 15)  # Order Number
        sheet.set_column('B:B', 20)  # Customer
        sheet.set_column('C:C', 12)  # Date
        sheet.set_column('D:D', 15)  # Amount
        sheet.set_column('E:E', 10)  # Status
        
        # Headers
        headers = ['Order #', 'Customer', 'Date', 'Amount', 'Status']
        for col, header in enumerate(headers):
            sheet.write(0, col, header, formats['subheader'])
        
        # Get orders data
        domain = [
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to)
        ]
        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))
        
        orders = self.env['sale.order'].search(domain, order='date_order desc')
        
        row = 1
        for order in orders:
            sheet.write(row, 0, order.name, formats['text'])
            sheet.write(row, 1, order.partner_id.name, formats['text'])
            sheet.write(row, 2, order.date_order, formats['date'])
            sheet.write(row, 3, order.amount_total, formats['currency'])
            sheet.write(row, 4, order.state, formats['text'])
            row += 1

    def _create_invoices_sheet(self, workbook, formats):
        """Create invoices worksheet"""
        sheet = workbook.add_worksheet('Invoices')
        
        # Set column widths
        sheet.set_column('A:A', 15)  # Invoice Number
        sheet.set_column('B:B', 20)  # Customer
        sheet.set_column('C:C', 12)  # Date
        sheet.set_column('D:D', 15)  # Amount
        sheet.set_column('E:E', 10)  # Status
        
        # Headers
        headers = ['Invoice #', 'Customer', 'Date', 'Amount', 'Status']
        for col, header in enumerate(headers):
            sheet.write(0, col, header, formats['subheader'])
        
        # Get invoices data
        domain = [
            ('move_type', '=', 'out_invoice'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to)
        ]
        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))
        
        invoices = self.env['account.move'].search(domain, order='invoice_date desc')
        
        row = 1
        for invoice in invoices:
            sheet.write(row, 0, invoice.name, formats['text'])
            sheet.write(row, 1, invoice.partner_id.name, formats['text'])
            sheet.write(row, 2, invoice.invoice_date, formats['date'])
            sheet.write(row, 3, invoice.amount_total, formats['currency'])
            sheet.write(row, 4, invoice.state, formats['text'])
            row += 1
```

### Step 3: Create Wizard View

Create `views/excel_report_views.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_customer_excel_report_form" model="ir.ui.view">
        <field name="name">customer.excel.report.form</field>
        <field name="model">customer.excel.report</field>
        <field name="arch" type="xml">
            <form string="Customer Excel Report">
                <group>
                    <group>
                        <field name="date_from"/>
                        <field name="date_to"/>
                    </group>
                    <group>
                        <field name="partner_ids" widget="many2many_tags"/>
                        <field name="include_orders"/>
                        <field name="include_invoices"/>
                    </group>
                </group>
                <footer>
                    <button name="action_generate_report" string="Generate Report" type="object" class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <record id="action_customer_excel_report" model="ir.actions.act_window">
        <field name="name">Customer Excel Report</field>
        <field name="res_model">customer.excel.report</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>

    <menuitem id="menu_customer_excel_report"
              name="Customer Excel Report"
              parent="account.menu_finance_reports"
              action="action_customer_excel_report"
              sequence="10"/>
</odoo>
```

---

## Advanced Report Features

### 1. Dynamic Report Parameters

Create parameterized reports with user input:

```python
class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    
    date_from = fields.Date('From Date', required=True)
    date_to = fields.Date('To Date', required=True)
    partner_ids = fields.Many2many('res.partner', string='Customers')
    report_type = fields.Selection([
        ('summary', 'Summary'),
        ('detailed', 'Detailed'),
        ('comparison', 'Comparison')
    ], default='summary')
    
    def action_print_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner_ids': self.partner_ids.ids,
            'report_type': self.report_type,
        }
        return self.env.ref('your_module.action_dynamic_report').report_action(self, data=data)
```

### 2. Multi-Language Support

Add translations to your reports:

```xml
<template id="report_template">
    <t t-call="web.external_layout">
        <div class="page">
            <h2 t-esc="env._('Customer Report')"/>
            <p t-esc="env._('Generated on: %s') % datetime.now().strftime('%Y-%m-%d')"/>
            <!-- More content -->
        </div>
    </t>
</template>
```

### 3. Conditional Formatting

Add dynamic styling based on data:

```xml
<t t-foreach="docs" t-as="invoice">
    <tr t-attf-class="#{invoice.state == 'paid' and 'text-success' or 'text-danger'}">
        <td t-field="invoice.name"/>
        <td t-field="invoice.amount_total"/>
        <td>
            <span t-if="invoice.state == 'paid'" class="badge badge-success">Paid</span>
            <span t-else="" class="badge badge-danger">Unpaid</span>
        </td>
    </tr>
</t>
```

### 4. Charts and Graphs

Add charts using Chart.js:

```xml
<div class="row">
    <div class="col-6">
        <canvas id="salesChart" width="400" height="200"></canvas>
    </div>
</div>

<script>
    var ctx = document.getElementById('salesChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: <t t-raw="chart_labels"/>,
            datasets: [{
                label: 'Sales',
                data: <t t-raw="chart_data"/>,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        }
    });
</script>
```

---

## Practical Examples

### Example 1: Smart Engagement Campaign Report

Perfect for your `smart_engagement` module:

```python
class SmartEngagementCampaignReport(models.AbstractModel):
    _name = 'report.smart_engagement.campaign_report'
    _description = 'Smart Engagement Campaign Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        campaigns = self.env['smart_engagement.campaign'].browse(docids)
        
        report_data = {
            'doc_ids': docids,
            'doc_model': 'smart_engagement.campaign',
            'docs': campaigns,
            'time': datetime.now(),
            'get_campaign_stats': self._get_campaign_stats,
            'get_message_status': self._get_message_status,
        }
        
        return report_data

    def _get_campaign_stats(self, campaign_id):
        """Get campaign statistics"""
        campaign = self.env['smart_engagement.campaign'].browse(campaign_id)
        logs = self.env['smart_engagement.whatsapp_api_log'].search([
            ('campaign_id', '=', campaign_id)
        ])
        
        return {
            'total_sent': len(logs),
            'successful': len(logs.filtered(lambda l: l.status == 'success')),
            'failed': len(logs.filtered(lambda l: l.status == 'error')),
            'pending': len(logs.filtered(lambda l: l.status == 'pending')),
            'success_rate': (len(logs.filtered(lambda l: l.status == 'success')) / len(logs) * 100) if logs else 0,
        }

    def _get_message_status(self, campaign_id):
        """Get message status breakdown"""
        logs = self.env['smart_engagement.whatsapp_api_log'].search([
            ('campaign_id', '=', campaign_id)
        ])
        
        status_counts = {}
        for log in logs:
            status_counts[log.status] = status_counts.get(log.status, 0) + 1
        
        return status_counts
```

### Example 2: Customer Segmentation Report

```python
class CustomerSegmentationReport(models.AbstractModel):
    _name = 'report.smart_engagement.segmentation_report'
    _description = 'Customer Segmentation Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        segments = self.env['smart_engagement.customer_segmentation'].browse(docids)
        
        return {
            'doc_ids': docids,
            'doc_model': 'smart_engagement.customer_segmentation',
            'docs': segments,
            'time': datetime.now(),
            'get_segment_customers': self._get_segment_customers,
            'get_age_distribution': self._get_age_distribution,
        }

    def _get_segment_customers(self, segment_id):
        """Get customers in segment"""
        segment = self.env['smart_engagement.customer_segmentation'].browse(segment_id)
        domain = safe_eval(segment.domain) if segment.domain else []
        return self.env['res.partner'].search(domain)

    def _get_age_distribution(self, customers):
        """Get age distribution of customers"""
        age_groups = {
            '18-25': 0,
            '26-35': 0,
            '36-45': 0,
            '46-55': 0,
            '56+': 0,
            'Unknown': 0
        }
        
        for customer in customers:
            if customer.age:
                if customer.age <= 25:
                    age_groups['18-25'] += 1
                elif customer.age <= 35:
                    age_groups['26-35'] += 1
                elif customer.age <= 45:
                    age_groups['36-45'] += 1
                elif customer.age <= 55:
                    age_groups['46-55'] += 1
                else:
                    age_groups['56+'] += 1
            else:
                age_groups['Unknown'] += 1
        
        return age_groups
```

### Example 3: Sales Performance Report

```python
class SalesPerformanceReport(models.AbstractModel):
    _name = 'report.your_module.sales_performance_report'
    _description = 'Sales Performance Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        # Get sales data
        sales_data = self._get_sales_data(date_from, date_to)
        
        return {
            'time': datetime.now(),
            'date_from': date_from,
            'date_to': date_to,
            'sales_data': sales_data,
            'top_customers': self._get_top_customers(date_from, date_to),
            'top_products': self._get_top_products(date_from, date_to),
            'monthly_trend': self._get_monthly_trend(date_from, date_to),
        }

    def _get_sales_data(self, date_from, date_to):
        """Get sales data summary"""
        orders = self.env['sale.order'].search([
            ('date_order', '>=', date_from),
            ('date_order', '<=', date_to),
            ('state', 'in', ['sale', 'done'])
        ])
        
        return {
            'total_orders': len(orders),
            'total_revenue': sum(orders.mapped('amount_total')),
            'average_order_value': sum(orders.mapped('amount_total')) / len(orders) if orders else 0,
            'total_customers': len(orders.mapped('partner_id')),
        }

    def _get_top_customers(self, date_from, date_to, limit=10):
        """Get top customers by revenue"""
        query = """
            SELECT partner_id, SUM(amount_total) as total_revenue
            FROM sale_order
            WHERE date_order >= %s AND date_order <= %s
            AND state IN ('sale', 'done')
            GROUP BY partner_id
            ORDER BY total_revenue DESC
            LIMIT %s
        """
        
        self.env.cr.execute(query, (date_from, date_to, limit))
        results = self.env.cr.fetchall()
        
        customers = []
        for partner_id, revenue in results:
            partner = self.env['res.partner'].browse(partner_id)
            customers.append({
                'name': partner.name,
                'revenue': revenue,
                'orders_count': len(partner.sale_order_ids.filtered(
                    lambda o: o.date_order >= date_from and o.date_order <= date_to
                ))
            })
        
        return customers

    def _get_top_products(self, date_from, date_to, limit=10):
        """Get top products by quantity sold"""
        query = """
            SELECT pol.product_id, SUM(pol.product_uom_qty) as total_qty, SUM(pol.price_subtotal) as total_revenue
            FROM sale_order_line pol
            JOIN sale_order so ON pol.order_id = so.id
            WHERE so.date_order >= %s AND so.date_order <= %s
            AND so.state IN ('sale', 'done')
            GROUP BY pol.product_id
            ORDER BY total_qty DESC
            LIMIT %s
        """
        
        self.env.cr.execute(query, (date_from, date_to, limit))
        results = self.env.cr.fetchall()
        
        products = []
        for product_id, qty, revenue in results:
            product = self.env['product.product'].browse(product_id)
            products.append({
                'name': product.name,
                'quantity': qty,
                'revenue': revenue,
                'avg_price': revenue / qty if qty else 0
            })
        
        return products

    def _get_monthly_trend(self, date_from, date_to):
        """Get monthly sales trend"""
        query = """
            SELECT DATE_TRUNC('month', date_order) as month, 
                   COUNT(*) as orders_count, 
                   SUM(amount_total) as total_revenue
            FROM sale_order
            WHERE date_order >= %s AND date_order <= %s
            AND state IN ('sale', 'done')
            GROUP BY DATE_TRUNC('month', date_order)
            ORDER BY month
        """
        
        self.env.cr.execute(query, (date_from, date_to))
        results = self.env.cr.fetchall()
        
        trend = []
        for month, orders, revenue in results:
            trend.append({
                'month': month.strftime('%Y-%m'),
                'orders': orders,
                'revenue': revenue
            })
        
        return trend
```

---

## Best Practices

### 1. **Performance Optimization**

```python
# ❌ Bad: N+1 queries
for partner in partners:
    orders = partner.sale_order_ids
    total = sum(orders.mapped('amount_total'))

# ✅ Good: Batch queries
partners_with_orders = partners.with_context(
    prefetch_fields=['sale_order_ids']
)
for partner in partners_with_orders:
    total = sum(partner.sale_order_ids.mapped('amount_total'))

# ✅ Better: Use raw SQL for complex calculations
query = """
    SELECT partner_id, SUM(amount_total)
    FROM sale_order
    WHERE partner_id IN %s
    GROUP BY partner_id
"""
env.cr.execute(query, (tuple(partner_ids),))
```

### 2. **Error Handling**

```python
@api.model
def _get_report_values(self, docids, data=None):
    try:
        # Report generation logic
        docs = self.env['model.name'].browse(docids)
        
        if not docs:
            raise UserError(_('No records found to generate report.'))
        
        # ... rest of logic
        
    except Exception as e:
        _logger.error(f"Error generating report: {str(e)}")
        raise UserError(_('Error generating report: %s') % str(e))
```

### 3. **Memory Management**

```python
# For large datasets, use batching
def _process_large_dataset(self, records):
    batch_size = 1000
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        # Process batch
        yield self._process_batch(batch)
```

### 4. **Security**

```python
# Always validate user permissions
def _get_report_values(self, docids, data=None):
    # Check if user has access to records
    docs = self.env['model.name'].browse(docids)
    docs.check_access_rights('read')
    docs.check_access_rule('read')
    
    # Filter based on user access
    accessible_docs = docs.filtered(lambda d: d.user_has_access())
```

### 5. **Internationalization**

```python
# Use proper translations
from odoo.tools.translate import _

def _get_report_values(self, docids, data=None):
    return {
        'title': _('Sales Report'),
        'date_format': self.env['res.lang']._lang_get(self.env.user.lang).date_format,
        'currency_symbol': self.env.user.company_id.currency_id.symbol,
    }
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. **"Report not found" Error**
```
Problem: Report template not found
Solution: Check template ID in report action matches template name
```

#### 2. **PDF Generation Fails**
```
Problem: wkhtmltopdf not installed or configured
Solution: Install wkhtmltopdf and configure in system parameters
```

#### 3. **Memory Issues with Large Reports**
```
Problem: OutOfMemoryError with large datasets
Solution: Use batching and pagination
```

#### 4. **Slow Report Generation**
```
Problem: Report takes too long to generate
Solution: Optimize queries, use proper indexing, add caching
```

### Debug Tips

1. **Enable Developer Mode**: Add `?debug=1` to URL
2. **Check Server Logs**: Look for error messages in odoo.log
3. **Use pdb**: Add `import pdb; pdb.set_trace()` for debugging
4. **Profile Queries**: Use `self.env.cr.query_log` to check SQL queries

---

## Resources

### Official Documentation
- [Odoo Reports Documentation](https://www.odoo.com/documentation/18.0/developer/reference/backend/reports.html)
- [QWeb Templates](https://www.odoo.com/documentation/18.0/developer/reference/frontend/qweb.html)

### Libraries and Tools
- **xlsxwriter**: Excel file generation
- **reportlab**: PDF generation
- **matplotlib**: Charts and graphs
- **wkhtmltopdf**: PDF conversion tool

### Sample Code Repository
```bash
# Clone examples
git clone https://github.com/odoo/odoo.git
cd odoo/addons/account/report/  # Check existing reports
```

---

## Conclusion

This guide provides a comprehensive foundation for creating custom reports in Odoo. Start with simple PDF reports and gradually implement more complex features like Excel exports, charts, and dynamic parameters.

Remember to:
- Follow Odoo coding standards
- Optimize for performance
- Handle errors gracefully
- Test thoroughly with real data
- Document your custom reports

Happy reporting! 📊