# Customer Segmentation from Reports Guide

## How to Create Customer Segments Using Odoo Reports and Custom Demographics Reports

This comprehensive guide explains how to leverage data from both Odoo's built-in reports and custom demographic reports to create effective customer segments in the Smart Engagement module.

## Table of Contents

1. [Overview](#overview)
2. [Available Reports and Their Insights](#available-reports-and-their-insights)
3. [Understanding Report Data](#understanding-report-data)
4. [Step-by-Step Segmentation Process](#step-by-step-segmentation-process)
5. [Common Segmentation Strategies](#common-segmentation-strategies)
6. [Advanced Segmentation Techniques](#advanced-segmentation-techniques)
7. [Best Practices](#best-practices)
8. [Examples and Use Cases](#examples-and-use-cases)
9. [Troubleshooting](#troubleshooting)

## Overview

Customer segmentation in Smart Engagement allows you to target specific groups of customers based on various criteria. By combining insights from multiple reports, you can create highly targeted segments that improve campaign effectiveness and customer engagement.

### Key Benefits of Report-Based Segmentation

- **Data-Driven Decisions**: Use actual customer behavior and demographics
- **Multi-Dimensional Analysis**: Combine financial, behavioral, and demographic data
- **Dynamic Segments**: Create rules that automatically update as data changes
- **Targeted Campaigns**: Send relevant messages to the right customers

## Available Reports and Their Insights

### Odoo Built-in Reports

#### 1. Sales Analysis (sale.report)
**Location**: Sales > Reporting > Sales
**Key Insights**:
- Total revenue by customer
- Purchase frequency
- Product preferences
- Order trends over time
- Average order value

**Useful for Segments**:
- High-value customers (revenue > X)
- Frequent buyers (orders > Y per month)
- Product category preferences
- Seasonal buyers

#### 2. Invoice Analysis (account.invoice.report)
**Location**: Accounting > Reporting > Invoices
**Key Insights**:
- Payment behavior
- Outstanding amounts
- Invoice frequency
- Payment terms usage

**Useful for Segments**:
- Prompt payers vs late payers
- Credit risk assessment
- Payment method preferences

#### 3. Customer Activity (res.partner)
**Location**: Contacts > Reporting > Partners
**Key Insights**:
- Last activity date
- Communication preferences
- Geographic distribution
- Company vs individual

**Useful for Segments**:
- Active vs inactive customers
- Geographic targeting
- B2B vs B2C segments

#### 4. CRM Pipeline (crm.lead)
**Location**: CRM > Reporting > Pipeline Analysis
**Key Insights**:
- Opportunity values
- Conversion rates
- Sales cycle length
- Lead sources

**Useful for Segments**:
- Hot prospects
- Nurture candidates
- Win-back targets

### Custom Demographics Reports

#### 1. Customer Demographics Overview
**Key Insights**:
- Age distribution
- Gender split
- Location demographics
- Purchase behavior by age

**Useful for Segments**:
- Age-based targeting
- Life stage marketing
- Geographic campaigns

#### 2. Customer Purchase Patterns by Age
**Key Insights**:
- Spending by age group
- Product preferences by age
- Purchase frequency by demographics

**Useful for Segments**:
- High-value age groups
- Product-specific age targeting
- Lifecycle marketing

#### 3. RFM Analysis with Demographics
**Key Insights**:
- Recency scores (1-5 scale)
- Frequency scores (1-5 scale)  
- Monetary scores (1-5 scale)
- Combined with age data

**Useful for Segments**:
- Champions (high RFM across all dimensions)
- At-risk customers (high value but declining activity)
- New customers to nurture (high recency, low frequency)

> 📖 **For detailed RFM explanations**, see the [Advanced Analytics User Guide](./ADVANCED_ANALYTICS_USER_GUIDE.md#business-user-quick-guide)

#### 4. Customer Lifetime Value by Demographics
**Key Insights**:
- CLV by age group
- Retention rates
- Growth potential

**Useful for Segments**:
- High CLV targets
- Retention focus groups
- Growth opportunity segments

## Understanding Report Data

### Key Metrics to Extract

1. **Behavioral Metrics**
   - Purchase frequency
   - Average order value
   - Last purchase date
   - Product categories bought
   - Channel preferences

2. **Demographic Metrics**
   - Age and age groups
   - Gender
   - Location (city, state, country)
   - Company affiliation
   - Contact preferences

3. **Financial Metrics**
   - Total revenue
   - Outstanding balances
   - Payment history
   - Discount usage
   - Return rates

4. **Engagement Metrics**
   - Email open rates
   - Campaign responses
   - Support tickets
   - Activity levels

### Data Analysis Process

1. **Export Report Data**
   - Use Excel export for detailed analysis
   - Note key thresholds and patterns
   - Identify segments visually

2. **Cross-Reference Reports**
   - Compare customer lists across reports
   - Find correlations (e.g., age vs spending)
   - Identify unique segments

3. **Define Segment Criteria**
   - Set clear thresholds
   - Combine multiple criteria
   - Ensure segments are actionable

## Step-by-Step Segmentation Process

### Phase 1: Data Gathering

1. **Access Reports**
   ```
   Sales > Reporting > Sales
   Accounting > Reporting > Invoices
   Smart Engagement > Reports > Customer Demographics
   ```

2. **Filter and Export Data**
   - Apply date ranges (last 12 months recommended)
   - Filter by active customers only
   - Export to Excel for analysis

3. **Analyze Patterns**
   - Create pivot tables
   - Look for natural groupings
   - Identify outliers and special cases

### Phase 2: Segment Definition

1. **Navigate to Segmentation**
   ```
   Smart Engagement > Configuration > Customer Segments
   ```

2. **Create New Segment**
   - Click "Create"
   - Enter descriptive name
   - Choose segmentation type:
     - Manual Selection (for specific lists)
     - Dynamic Rules (for auto-updating)

3. **Define Rules Based on Reports**

#### Example: High-Value Young Professionals
```python
# Domain filter combining multiple criteria
[
    ('age', '>=', 25),
    ('age', '<=', 35),
    ('rfm_score', '>=', 10),
    ('monetary_score', '>=', 4)
]
# OR using traditional criteria:
[
    ('age', '>=', 25),
    ('age', '<=', 35),
    ('total_spent', '>', 5000),
    ('days_since_last_purchase', '<=', 180)
]
```

### Phase 3: Rule Configuration

1. **Basic Rules Structure**
   ```
   Field | Operator | Value
   ```

2. **Combining Conditions**
   - Use AND logic: All conditions must be true
   - Use OR logic: Any condition can be true
   - Nest conditions for complex logic

3. **Available Fields for Rules**
   - **Demographics**: age, date_of_birth, gender
   - **Geographic**: city, state_id, country_id
   - **Financial**: total_invoiced, credit_limit, total_spent
   - **Behavioral**: last_purchase_date, order_count, days_since_last_purchase, purchase_count
   - **RFM Analysis**: rfm_segment, rfm_score, recency_score, frequency_score, monetary_score
   - **Custom**: Any field added to res.partner

### Phase 4: Validation and Testing

1. **Preview Segment**
   - Click "Preview Customers"
   - Verify customer list matches expectations
   - Check segment size

2. **Test with Small Campaign**
   - Create test campaign
   - Send to segment subset
   - Monitor responses

3. **Refine Rules**
   - Adjust thresholds based on results
   - Add or remove conditions
   - Re-test as needed

## Common Segmentation Strategies

### 1. RFM-Based Segments

**Champions (R=5, F=5, M=5)**
```python
[
    ('rfm_segment', '=', 'champions'),
    ('active', '=', True)
]
# OR using individual scores:
[
    ('recency_score', '=', 5),
    ('frequency_score', '=', 5),
    ('monetary_score', '=', 5)
]
```

**At Risk (R=2, F=3-4, M=3-4)**
```python
[
    ('rfm_segment', '=', 'at_risk'),
    ('active', '=', True)
]
# OR using individual scores:
[
    ('recency_score', '=', 2),
    ('frequency_score', '>=', 3),
    ('frequency_score', '<=', 4),
    ('monetary_score', '>=', 3),
    ('monetary_score', '<=', 4)
]
```

**Cannot Lose Them (High Value, Inactive)**
```python
[
    ('rfm_segment', '=', 'cannot_lose_them'),
    ('active', '=', True)
]
# OR using individual scores:
[
    ('recency_score', '<=', 2),
    ('frequency_score', '>=', 4),
    ('monetary_score', '>=', 4)
]
```

### 2. Demographic-Based Segments

**Millennials with High Spending**
```python
[
    ('age', '>=', 28),
    ('age', '<=', 43),
    ('total_invoiced', '>', 2000)
]
```

**Senior Citizens for Special Offers**
```python
[
    ('age', '>=', 65),
    ('is_company', '=', False)
]
```

### 3. Behavioral Segments

**Frequent Buyers**
```python
[
    ('sale_order_count', '>', 12),
    ('last_purchase_date', '>', fields.Date.today() - timedelta(days=90))
]
```

**Dormant High-Value Customers**
```python
[
    ('total_revenue', '>', 5000),
    ('last_purchase_date', '<', fields.Date.today() - timedelta(days=180))
]
```

### 4. Geographic Segments

**Urban High Spenders**
```python
[
    ('city', 'in', ['New York', 'Los Angeles', 'Chicago']),
    ('total_invoiced', '>', 3000)
]
```

## Advanced Segmentation Techniques

### 1. Multi-Report Correlation

**Process**:
1. Export customer IDs from each report
2. Use VLOOKUP in Excel to combine data
3. Identify customers appearing in multiple high-value categories
4. Create segment with specific IDs

### 2. Predictive Segments

**Based on CLV Analysis**:
- Identify customers with rising CLV trend
- Target before they plateau
- Focus on age groups with highest CLV potential

### 3. Lifecycle Segmentation

**New Customer Journey**:
- First purchase: Welcome series
- 30 days: Satisfaction check
- 60 days: Cross-sell based on first purchase
- 90 days: Loyalty program invitation

### 4. Custom Calculated Fields

**Add to res.partner**:
```python
# Customer score combining multiple factors
customer_score = fields.Float(
    compute='_compute_customer_score',
    store=True
)

@api.depends('age', 'total_invoiced', 'last_purchase_date')
def _compute_customer_score(self):
    # Implement scoring logic
```

## Best Practices

### 1. Segment Sizing
- **Minimum**: 50 customers (statistical significance)
- **Maximum**: 5,000 customers (personalization limit)
- **Ideal**: 200-1,000 customers

### 2. Update Frequency
- **Dynamic Rules**: Real-time updates
- **Manual Lists**: Weekly/monthly review
- **Campaign Results**: After each campaign

### 3. Testing Strategy
- Always test with 10% sample first
- Compare against control group
- Measure key metrics:
  - Open rates
  - Response rates
  - Conversion rates
  - ROI

### 4. Documentation
- Document segment logic
- Track performance metrics
- Note successful combinations
- Share insights with team

## Examples and Use Cases

### Use Case 1: Birthday Month Campaign

**Data Sources**:
- Customer Demographics Report (date_of_birth)
- Sales Analysis (purchase history)

**Segment Rule**:
```python
[
    ('date_of_birth', '!=', False),
    ('birth_month', '=', current_month),
    ('last_purchase_date', '>', fields.Date.today() - timedelta(days=365))
]
```

**Campaign**: Special birthday discount with personalized product recommendations

### Use Case 2: Win-Back Campaign

**Data Sources**:
- RFM Analysis (identify "Cannot Lose Them" segment)
- Invoice Analysis (payment history)

**Segment Rule**:
```python
[
    ('rfm_segment', '=', 'cannot_lose_them'),
    ('active', '=', True)
]
# OR using manual criteria:
[
    ('recency_score', '<=', 2),
    ('frequency_score', '>=', 4),
    ('monetary_score', '>=', 4),
    ('total_spent', '>', 1000)
]
```

**Campaign**: Exclusive "We Miss You" offer with premium incentive

### Use Case 3: Product Launch to Early Adopters

**Data Sources**:
- Sales Analysis (first purchase dates)
- Customer Demographics (age group)

**Segment Rule**:
```python
[
    ('first_purchase_category', 'in', ['Electronics', 'Gadgets']),
    ('age', '>=', 25),
    ('age', '<=', 45),
    ('purchase_frequency', '>', 3)
]
```

**Campaign**: Exclusive early access to new tech products

### Use Case 4: Regional Seasonal Campaign

**Data Sources**:
- Geographic data from contacts
- Seasonal purchase patterns

**Segment Rule**:
```python
[
    ('state_id.name', 'in', ['California', 'Arizona', 'Nevada']),
    ('last_summer_purchase', '>', 500),
    ('is_active', '=', True)
]
```

**Campaign**: Summer collection preview for warm-weather states

## Troubleshooting

### Common Issues and Solutions

1. **Segment Too Small**
   - Broaden criteria
   - Extend date ranges
   - Remove restrictive conditions

2. **Segment Too Large**
   - Add more specific criteria
   - Increase thresholds
   - Focus on recent activity

3. **No Results**
   - Check field names and syntax
   - Verify data exists in fields
   - Test each condition separately

4. **Performance Issues**
   - Limit computed fields in rules
   - Use indexed fields when possible
   - Consider manual selection for complex logic

### Validation Checklist

- [ ] Segment size is appropriate (50-5,000)
- [ ] Rules are logically sound
- [ ] Test data confirms expectations
- [ ] Campaign message matches segment
- [ ] Tracking is configured
- [ ] Success metrics are defined

## Integration with Campaign Creation

### Workflow

1. **Create Segment** (as described above)
2. **Design Campaign**
   - Navigate to Campaigns
   - Select your segment
   - Craft message for segment characteristics

3. **Personalization**
   - Use segment insights for message customization
   - Reference relevant products/services
   - Adjust tone for demographics

4. **Schedule and Monitor**
   - Choose optimal send time for segment
   - Monitor real-time results
   - Adjust future segments based on performance

### Measurement and Optimization

1. **Track Segment Performance**
   - Response rates by segment
   - Conversion rates
   - Revenue per segment

2. **Iterate and Improve**
   - Refine high-performing segments
   - Retire low-performing ones
   - Test new combinations

3. **Share Insights**
   - Document successful segments
   - Create templates for reuse
   - Train team on effective segmentation

## Conclusion

Effective customer segmentation combines art and science. By leveraging data from multiple Odoo reports and custom demographics analysis, you can create highly targeted segments that drive better campaign results. Remember to:

- Start with clear objectives
- Use data to guide decisions
- Test and refine continuously
- Document what works
- Scale successful approaches

The combination of Odoo's built-in reporting and custom demographic insights provides a powerful foundation for sophisticated customer segmentation in your WhatsApp marketing campaigns.