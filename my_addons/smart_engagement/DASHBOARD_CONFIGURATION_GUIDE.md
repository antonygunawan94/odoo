# 📊 Odoo Dashboard Configuration Guide
## Complete Manual Setup Without Code Changes

---

## 📋 Table of Contents
1. [Product Categorization Setup](#1-product-categorization-setup)
2. [Sales Source Tracking](#2-sales-source-tracking)
3. [Customer Age Group Configuration](#3-customer-age-group-configuration)
4. [Branch/Location Management](#4-branchlocation-management)
5. [Target vs Actual Tracking](#5-target-vs-actual-tracking)
6. [Customer Segmentation](#6-customer-segmentation)
7. [Report Configuration](#7-report-configuration)
8. [Automated Actions](#8-automated-actions)
9. [Dashboard Creation](#9-dashboard-creation)
10. [Excel Integration](#10-excel-integration)

---

## 1. Product Categorization Setup

### 🎯 Purpose
Create A-H product rankings as shown in your marketing reports.

### 📍 Navigation Paths

#### Option A: Product Categories (Recommended)
**Path:** `Inventory → Configuration → Product Categories`

**Steps:**
1. Click "Create"
2. Set up hierarchy:
   ```
   📁 All Products
   ├── 📁 Physical Products
   │   ├── Category A (Premium - Top Revenue)
   │   ├── Category B (High Revenue)
   │   ├── Category C (Medium-High Revenue)
   │   ├── Category D (Medium Revenue)
   │   ├── Category E (Medium-Low Revenue)
   │   ├── Category F (Low Revenue)
   │   ├── Category G (Very Low Revenue)
   │   └── Category H (Minimal Revenue)
   ├── 📁 Treatment Services
   │   ├── Facial Treatments
   │   ├── Body Treatments
   │   ├── Medical Aesthetic
   │   └── Wellness Services
   └── 📁 Redemption Items
       └── Loyalty Point Redemptions
   ```

**Category Configuration Fields:**
- **Category Name**: e.g., "Category A"
- **Parent Category**: Select "Physical Products"
- **Force Removal Strategy**: FIFO
- **Costing Method**: Average Cost
- **Inventory Valuation**: Automated

#### Option B: Product Attributes
**Path:** `Sales → Configuration → Products → Attributes`

**Steps:**
1. Create attribute "Product Ranking"
2. Add values: A, B, C, D, E, F, G, H
3. Create attribute "Sales Source"
4. Add values: Product, Treatment, Redemption

#### Option C: Internal Reference System
**Path:** When creating/editing products

**Naming Convention:**
- Products: `PRD-A-001`, `PRD-B-001`
- Treatments: `TRT-FAC-001`, `TRT-BOD-001`
- Redemptions: `RDM-001`

---

## 2. Sales Source Tracking

### 🎯 Purpose
Separate Products, Treatments, and Redemptions in reports.

### 📍 Implementation Options

#### Option A: Product Type Field (Best for Services)
**Path:** `Sales → Products → Products`

**Configuration per Product:**
1. **General Tab:**
   - Product Type: 
     - Consumable (for physical products)
     - Service (for treatments)
   - Can be Sold: ✓
   - Can be Purchased: ✓/✗

2. **Sales Tab:**
   - Income Account: 
     - Product Sales (for products)
     - Service Income (for treatments)
     - Redemption Account (for loyalty)

#### Option B: Product Tags
**Path:** `Sales → Configuration → Product Tags`

**Create Tags:**
1. **Source Tags:**
   - `PRODUCT` (Color: Blue)
   - `TREATMENT` (Color: Green)
   - `REDEMPTION` (Color: Orange)

2. **Category Tags:**
   - `CERAH` (All Cerah products)
   - `ACNE` (Acne treatment products)
   - `PHYTO` (Phyto treatment)
   - `KOREAN` (Korean products)

**Bulk Tagging:**
1. Go to Products list view
2. Select multiple products
3. Action → Add Tags

#### Option C: Custom Product Categories
**Path:** `Sales → Configuration → Product Categories`

**Structure:**
```
📁 Sales Sources
├── 📁 Product Sales
│   ├── 📁 Skincare
│   │   ├── Day Cream
│   │   ├── Night Cream
│   │   ├── Serum
│   │   └── Cleanser
│   └── 📁 Supplements
├── 📁 Treatment Revenue
│   ├── 📁 Facial Treatments
│   │   ├── Phyto Treatment
│   │   ├── Korean Acne Clear
│   │   └── Instant Glow
│   └── 📁 Body Treatments
└── 📁 Redemptions
    └── Loyalty Redemptions
```

---

## 3. Customer Age Group Configuration

### 🎯 Purpose
Automatically categorize customers by generation.

### 📍 Navigation Path
**Path:** `Smart Engagement → Configuration → Customer Age Groups`

### 📊 Recommended Configuration

| Group Name | Code | Min Age | Max Age | Birth Years |
|------------|------|---------|---------|-------------|
| Gen Alpha | alpha | 0 | 11 | 2013-2025 |
| Gen Z | gen_z | 12 | 27 | 1997-2012 |
| Millennial | millennial | 28 | 43 | 1981-1996 |
| Gen X | gen_x | 44 | 59 | 1965-1980 |
| Boomers | boomers | 60 | 78 | 1946-1964 |
| Silent Gen | silent | 79 | 95 | 1928-1945 |

### 🔧 Configuration Steps
1. **Create Age Group:**
   - Name: "Gen Z (12-27 years)"
   - Code: gen_z
   - Min Age: 12
   - Max Age: 27
   - Description: "Digital natives, social media savvy"

2. **View Analytics:**
   - Customer Count (auto-calculated)
   - Total Revenue (auto-calculated)
   - Average Age (auto-calculated)
   - Average Spending (auto-calculated)

3. **Bulk Update:**
   - Click "Update Customer Analytics"
   - System recalculates all customer assignments

---

## 4. Branch/Location Management

### 🎯 Purpose
Track performance by outlet/branch.

### 📍 Multiple Options Available

#### Option A: Sales Teams (Recommended)
**Path:** `Sales → Configuration → Sales Teams`

**Setup:**
1. **Create Team per Branch:**
   ```
   Team Name: "Jakarta - Plaza Indonesia"
   Team Leader: [Branch Manager]
   Email Alias: jakarta.pi@company.com
   Members: [Add all branch staff]
   ```

2. **Dashboard Features:**
   - Revenue Target
   - Invoiced This Month
   - Pipeline
   - Activities

**Reporting:** Filter any sales report by team

#### Option B: Operating Units (Multi-Company)
**Path:** `Settings → Users & Companies → Companies`

**Structure:**
```
🏢 Parent Company
├── 🏪 Jakarta Branch
├── 🏪 Surabaya Branch
├── 🏪 Bandung Branch
└── 🏪 Online Store
```

**Benefits:**
- Separate accounting
- Branch-specific pricing
- Independent inventory

#### Option C: Warehouses/Locations
**Path:** `Inventory → Configuration → Warehouses`

**Setup per Branch:**
1. **Warehouse Configuration:**
   - Name: "WH/Jakarta-PI"
   - Short Name: "JKT-PI"
   - Address: [Branch address]

2. **Location Structure:**
   ```
   WH/Jakarta-PI
   ├── Receipts
   ├── Stock
   │   ├── Treatment Room 1
   │   ├── Treatment Room 2
   │   └── Retail Display
   └── Delivery
   ```

#### Option D: Analytic Accounts
**Path:** `Accounting → Configuration → Analytic Accounting → Analytic Accounts`

**Structure:**
```
📊 Company Analytics
├── 📍 By Location
│   ├── Jakarta - Plaza Indonesia
│   ├── Jakarta - Grand Indonesia  
│   └── Surabaya - Tunjungan Plaza
├── 📈 By Department
│   ├── Retail Sales
│   ├── Treatment Services
│   └── Online Sales
└── 🎯 By Campaign
    ├── Q1 2025 Promotion
    └── Member Anniversary
```

**Usage:**
- Tag on Sales Orders
- Tag on Invoices
- Detailed P&L by branch

#### Option E: Partner Company Field
**Path:** `Contacts → Configuration → Localization`

**Custom Usage:**
1. Add company field to partners
2. Set "Plaza Indonesia" as company
3. Link customers to branches
4. Group reports by partner company

---

## 5. Target vs Actual Tracking

### 🎯 Purpose
Monitor sales achievement against targets.

### 📍 Available Options

#### Option A: CRM Quotas
**Path:** `CRM → Configuration → Quotas`

**Setup:**
1. **Define Quota:**
   - User: [Salesperson/Team]
   - Period: Monthly/Quarterly
   - Target: IDR 600,000,000
   - Product Line: All/Specific

2. **Track Achievement:**
   - Dashboard shows progress
   - Automatic calculation
   - Email alerts at milestones

#### Option B: Budget Management
**Path:** `Accounting → Configuration → Management → Budgetary Positions`

**Steps:**
1. **Create Budget:**
   ```
   Name: "2025 Sales Budget"
   Period: Jan 2025 - Dec 2025
   ```

2. **Add Lines:**
   | Account | Jan | Feb | Mar | Q1 Total |
   |---------|-----|-----|-----|----------|
   | Product Sales | 400M | 420M | 450M | 1,270M |
   | Service Income | 200M | 210M | 220M | 630M |
   | Total | 600M | 630M | 670M | 1,900M |

3. **Compare Actual:**
   - Reports → Budget Analysis
   - Shows variance by month/account

#### Option C: Custom Fields on Sales Team
**Path:** `Settings → Technical → Fields`

**Add to sales.team:**
1. monthly_target (Float)
2. quarterly_target (Float)
3. yearly_target (Float)

**Simple Tracking:**
- Update targets monthly
- Create custom report
- Compare with actual sales

#### Option D: Project Tasks for Targets
**Path:** `Project → Create Project "Sales Targets"`

**Monthly Task Template:**
```
Task: "January 2025 Sales Target"
Assigned to: Sales Manager
Description: 
- Target: IDR 600,000,000
- Product: IDR 400,000,000
- Treatment: IDR 200,000,000
Checklist:
□ Week 1: 150M (25%)
□ Week 2: 300M (50%)
□ Week 3: 450M (75%)
□ Week 4: 600M (100%)
```

---

## 6. Customer Segmentation

### 🎯 Purpose
Group customers for targeted marketing.

### 📍 Configuration Options

#### Option A: Partner Tags (Most Flexible)
**Path:** `Contacts → Configuration → Contact Tags`

**Recommended Tag Structure:**

**1. Value Tier Tags:**
- 🏆 VIP (Top 1% - Spending >50M/year)
- 💎 Premium (Top 10% - Spending >10M/year)
- 🥇 Gold (Top 25% - Spending >5M/year)
- 🥈 Silver (Top 50% - Spending >1M/year)
- 🥉 Bronze (Active customers <1M/year)

**2. Customer Type Tags:**
- 🏢 B2B - Clinic
- 🏢 B2B - Spa/Salon
- 👤 B2C - Individual
- 👥 B2C - Referral Source

**3. Behavior Tags:**
- 🆕 New Customer (First 3 months)
- 🔄 Repeat Customer (2+ purchases)
- 😴 Dormant (No purchase >6 months)
- 🎂 Birthday Month
- 📱 WhatsApp Subscriber

**4. Preference Tags:**
- 🌿 Eco-Conscious
- 💰 Price-Sensitive  
- ⭐ Premium Seeker
- 🏃 Convenience Buyer

#### Option B: Marketing Lists
**Path:** `Email Marketing → Mailing Lists`

**Create Dynamic Lists:**
1. **VIP Customers:**
   - Filter: Total Sales > 50,000,000
   - Auto-update: Daily

2. **Birthday This Month:**
   - Filter: Birth Month = Current Month
   - Auto-update: Daily

3. **Inactive Customers:**
   - Filter: Last Order Date < 6 months ago
   - Auto-update: Weekly

#### Option C: Customer Properties
**Path:** `Sales → Configuration → Settings → Customer Accounts`

**Add Properties:**
- Customer Since (Date)
- Preferred Branch (Selection)
- Skin Type (Selection)
- Treatment Preference (Multiple)
- Contact Preference (Email/SMS/WhatsApp)

---

## 7. Report Configuration

### 🎯 Purpose
Create standard reports matching Excel format.

### 📍 Built-in Reports Configuration

#### A. Sales Analysis
**Path:** `Sales → Reporting → Sales`

**Standard Filters to Save:**

**1. "Monthly Sales by Source"**
- Group by: Product Category (Level 1)
- Filter: This Month
- Measures: Untaxed Amount, Tax, Total

**2. "Sales by Generation"**
- Group by: Customer > Age Group
- Measures: Count, Total, Average

**3. "Branch Performance"**
- Group by: Sales Team
- Sub-group: Product Category
- Measures: Quantity, Revenue

**Save Filter Steps:**
1. Apply all filters/groups
2. Favorites → Save current search
3. Name: "Monthly Sales by Source"
4. Default: ✓ (if used daily)
5. Shared: ✓ (for team access)

#### B. Customer Reports
**Path:** `Smart Engagement → Reports → Customer Demographics`

**Key Views:**

**1. List View Columns:**
- Customer Name
- Age Group
- Total Spent
- Order Count
- Last Purchase
- Branch
- Tags

**2. Pivot Table:**
- Rows: Age Group, City
- Columns: Month
- Measures: Customer Count, Revenue

**3. Graph View:**
- Bar Chart: Revenue by Age Group
- Line Chart: Monthly Trend
- Pie Chart: Customer Distribution

#### C. Product Performance
**Path:** `Smart Engagement → Reports → Product Category Performance`

**Configure:**
1. **Top Products View:**
   - Sort: Revenue Descending
   - Limit: 20 records
   - Show: Rank, Product, Qty, Revenue, %

2. **Category Analysis:**
   - Group by: Category (A-H)
   - Show: Items, Revenue, Margin, Growth%

---

## 8. Automated Actions

### 🎯 Purpose
Automatically tag and categorize without manual work.

### 📍 Setup Automated Rules
**Path:** `Settings → Technical → Automation → Automated Actions`

#### Essential Automation Rules

**1. Auto-Tag VIP Customers**
```yaml
Name: "Tag VIP Customers"
Model: Contact (res.partner)
Trigger: On Update
Before Update Domain: 
  - Total Sales < 50,000,000
Apply Domain:
  - Total Sales >= 50,000,000
Action: Add Tag "VIP"
```

**2. New Customer Welcome**
```yaml
Name: "Tag New Customers"
Model: Contact
Trigger: On Creation
Condition: Customer Rank > 0
Actions:
  - Add Tag "New Customer"
  - Send Welcome Email
  - Create Activity for Sales
```

**3. Dormant Customer Alert**
```yaml
Name: "Mark Dormant Customers"
Model: Contact
Trigger: Based on Time Condition
Filter: Last Order Date
Date Field: Last Sale Date
Delay: 180 days
Action: 
  - Add Tag "Dormant"
  - Create Re-activation Task
```

**4. Birthday Month Tagging**
```yaml
Name: "Birthday This Month"
Model: Contact
Trigger: Based on Time Condition
Execute Every: 1 Month
Filter: Birth Date is set
Condition: Month of Birth Date = Current Month
Action: Add Tag "Birthday Month"
Remove Tag After: 1 Month
```

**5. Branch Assignment**
```yaml
Name: "Assign to Branch Team"
Model: Sale Order
Trigger: On Creation
Condition: Based on delivery address
Actions: Set Sales Team based on location
```

---

## 9. Dashboard Creation

### 🎯 Purpose
Executive dashboard matching Excel reports.

### 📍 Creating Custom Dashboards

#### Option A: My Dashboard
**Path:** `Home → Customize → Add Item to Dashboard`

**Steps:**
1. Go to any report
2. Apply desired filters
3. Click ⭐ Add to My Dashboard
4. Choose visualization:
   - 📊 Bar Chart
   - 📈 Line Graph  
   - 🥧 Pie Chart
   - 🔢 Number Card
   - 📋 List

**Recommended Dashboard Items:**

**Row 1 - KPIs:**
- MTD Sales (Number)
- Target Achievement % (Gauge)
- Customer Count (Number)
- Avg Transaction (Number)

**Row 2 - Charts:**
- Sales by Source (Pie)
- Daily Trend (Line)
- Top 5 Products (Bar)
- By Generation (Bar)

**Row 3 - Lists:**
- Pending Orders
- Today's Appointments
- Low Stock Alerts

#### Option B: Custom Dashboard Module
**Path:** `Apps → Dashboard Builder` (Install if needed)

**Features:**
- Drag-and-drop design
- Real-time updates
- Multiple layouts
- Export to PDF

#### Option C: Spreadsheet Dashboard
**Path:** `Documents → Spreadsheets`

**Create Live Excel in Odoo:**
1. New Spreadsheet
2. Insert → Pivot Table
3. Select Odoo Data
4. Design like Excel
5. Auto-updates from database

---

## 10. Excel Integration

### 🎯 Purpose
Export data matching current Excel format.

### 📍 Export Options

#### A. Direct Export
**From Any List View:**
1. Select records (or all)
2. Action → Export
3. Choose fields:
   ```
   ✓ Customer Name
   ✓ Age Group  
   ✓ Total Sales
   ✓ Product Categories Purchased
   ✓ Branch
   ✓ Tags
   ```
4. Export format: XLSX

#### B. Scheduled Exports
**Path:** `Settings → Technical → Automation → Scheduled Actions`

**Create Automated Export:**
```yaml
Name: "Daily Sales Report Export"
Model: Sale Order
Execute Every: 1 Day at 06:00
Action: 
  - Generate Report
  - Save to: /reports/daily/
  - Email to: management@company.com
```

#### C. Power Query Connection
**From Excel:**
1. Data → Get Data → From Other Sources
2. Odoo API URL: https://your-odoo.com/api
3. Authentication: API Key
4. Select tables:
   - sale_order
   - res_partner
   - product_product

**Auto-refresh:** Every hour

#### D. Google Sheets Integration
**Using Odoo API:**
1. Create Google Apps Script
2. Fetch Odoo data via JSON-RPC
3. Update sheets automatically
4. Share live dashboards

---

## 📋 Implementation Checklist

### Week 1: Foundation
- [ ] Set up Product Categories (A-H)
- [ ] Configure Sales Teams for branches
- [ ] Create Age Groups configuration
- [ ] Design tag structure
- [ ] Import/update customer birthdays

### Week 2: Classification
- [ ] Tag existing products
- [ ] Categorize customers
- [ ] Set up analytic accounts
- [ ] Configure automated actions
- [ ] Create saved report filters

### Week 3: Reporting
- [ ] Build standard report views
- [ ] Create dashboard layout
- [ ] Set up scheduled exports
- [ ] Test Excel integration
- [ ] Train team on usage

### Week 4: Optimization
- [ ] Review data quality
- [ ] Adjust categorizations
- [ ] Fine-tune automations
- [ ] Create user guides
- [ ] Set up alerts

---

## 💡 Pro Tips

1. **Start Simple**
   - Begin with product categories
   - Add complexity gradually
   - Test with small data sets

2. **Use Templates**
   - Create one perfect product
   - Duplicate for similar items
   - Bulk update via import

3. **Regular Maintenance**
   - Weekly: Review new customers
   - Monthly: Update targets
   - Quarterly: Analyze categories

4. **Training Focus**
   - One feature at a time
   - Document everything
   - Create video guides

5. **Data Quality**
   - Standardize naming
   - Regular cleanup
   - Validation rules

---

## 🆘 Troubleshooting

**Common Issues:**

**1. Reports not matching:**
- Check filters
- Verify date ranges
- Confirm grouping

**2. Missing data:**
- Check user permissions
- Verify record rules
- Confirm field visibility

**3. Slow performance:**
- Add database indexes
- Archive old data
- Optimize views

**4. Export problems:**
- Check field permissions
- Verify export limits
- Try smaller batches

---

## 📞 Need Help?

1. **Odoo Documentation:** help.odoo.com
2. **Community Forum:** odoo.com/forum
3. **Video Tutorials:** youtube.com/odoo
4. **Support Ticket:** Via your Odoo instance

---

*This guide covers all manual configuration options available in Odoo 18.0 without any code modifications. Follow the steps sequentially for best results.*