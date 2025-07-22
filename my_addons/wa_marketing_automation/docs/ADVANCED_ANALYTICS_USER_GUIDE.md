# Advanced Analytics User Guide

## Complete Guide to Customer Analytics and Segmentation

This comprehensive guide covers all advanced analytics features in the WhatsApp Marketing Automation module, including engagement scoring, churn prediction, cohort analysis, product category analytics, and emerging trends like social commerce and BNPL analytics.

### 🎉 Quick Update Summary

**New Features Added:**
- ✅ **Product Category Analytics** on customer records (new tab)
- ✅ **Category Performance Reports** suite (7 new reports)
- ✅ **Calculation Transparency** for all metrics
- ✅ **Fully Configurable Settings** (no more hardcoded values)
- ✅ **Multi-Currency Support** with automatic conversion
- ✅ **Dynamic Date Calculations** (no hardcoded years)

**Key Improvements:**
- All metrics now show "How is this calculated?" explanations
- Spending tier × category matrix analysis (matches Excel requirements)
- Customer spending tiers fully customizable (supports A-H naming)
- Age groups, acquisition sources all configurable
- Complete removal of hardcoded values and assumptions

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Business User Quick Guide](#business-user-quick-guide)
4. [Core Analytics Features](#core-analytics-features)
5. [Advanced Analytics Features](#advanced-analytics-features)
6. [Product Category Analytics](#product-category-analytics)
7. [Emerging Trends Analytics](#emerging-trends-analytics)
8. [Reports and Dashboards](#reports-and-dashboards)
9. [Category Performance Reports](#category-performance-reports)
10. [Practical Applications](#practical-applications)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)
13. [Integration Guide](#integration-guide)

## Overview

### What's New in Advanced Analytics

The WhatsApp Marketing Automation module now includes cutting-edge customer analytics capabilities that go far beyond traditional RFM analysis. These features help you understand your customers at a deeper level and create more effective marketing campaigns.

#### 🆕 Latest Updates

- **Product Category Analytics**: Deep insights into customer preferences by product category
- **Category Performance Reports**: Spending tier × category matrix analysis matching Excel requirements
- **Calculation Transparency**: All metrics now show clear explanations of how they're calculated
- **Dynamic Configuration**: All thresholds and settings are now fully configurable (no hardcoded values)
- **Multi-Currency Support**: Automatic currency conversion using company base currency

### Key Benefits

- **Predictive Capabilities**: Know which customers will churn before they do
- **Multi-Channel Insights**: Understand customer behavior across all touchpoints
- **Product Category Intelligence**: Understand what customers buy and predict future preferences
- **2025 Trend Alignment**: Leverage social commerce and BNPL analytics
- **Automated Scoring**: Real-time calculation of engagement and risk scores
- **Cohort Analysis**: Track customer behavior over time
- **Values-Based Targeting**: Segment by sustainability and social responsibility preferences
- **Business Transparency**: Every metric shows exactly how it's calculated

## Getting Started

### Accessing Advanced Analytics

1. **Navigate to Contacts**: Go to the Contacts app
2. **Select a Customer**: Open any individual customer record
3. **View Analytics Tabs**: You'll see new tabs for:
   - RFM Analysis
   - Engagement Analytics
   - Churn Prediction
   - Values & Preferences
   - Social Commerce
   - BNPL & Mobile Commerce
   - Demographics & Source
   - Product Categories

4. **Calculation Transparency**: Look for the "How is this calculated?" expandable sections in each tab to understand exactly how metrics are computed

### Understanding Calculation Transparency

#### What is Calculation Transparency?

Every analytics metric now includes a detailed explanation of how it's calculated. This transparency helps you:
- Understand the logic behind each score
- Trust the analytics recommendations
- Explain metrics to stakeholders
- Customize calculations if needed

#### How to Access Calculation Details

1. **In Customer Records**: Look for blue info boxes with "How is this calculated?" links
2. **Expandable Sections**: Click to expand and see:
   - Data sources used
   - Calculation formulas
   - Thresholds and scoring logic
   - Update frequency

#### Example Calculation Transparencies

**Engagement Score**:
```
Shows how actively customers interact with your business.
Looks at email opens and clicks, website visits and purchases, 
and WhatsApp message responses over the last 90 days.

Calculation:
- Email Score: (Opens × 1 + Clicks × 2) / Days × 100
- Website Score: Based on order recency and frequency
- WhatsApp Score: Response rate to campaigns
- Overall: Weighted average of available channels
```

**Demographics Analysis**:
```
Provides insights into customer age, location, and demographics.

We analyze:
- Age: Calculated from birth date if available
- Location: From primary address
- Age Group: Automatic categorization (18-24, 25-34, etc.)
- Missing Data: Clearly indicated when information unavailable
```

### Initial Setup

Before using advanced analytics, ensure:
- Customer data is populated (orders, contact information)
- UTM tracking is configured for social media campaigns
- Payment terms are set up for BNPL tracking
- Email and WhatsApp campaigns have been sent

## Business User Quick Guide

### 📊 Quick Overview - What We Measure

We track **6 key areas** of customer behavior:

1. **📈 RFM Analysis** - How valuable is this customer?
2. **💬 Engagement** - How interested is this customer?
3. **⚠️ Churn Risk** - Will this customer stop buying?
4. **🎯 Customer Journey** - Where is this customer in their relationship with us?
5. **💚 Values & Preferences** - What does this customer care about?
6. **📱 Modern Commerce** - How does this customer prefer to shop?

### 📈 RFM Analysis - Customer Value Scoring (Business View)

**The Three Scores (Each 1-5 Stars)**

**⏰ Recency Score**
- ⭐⭐⭐⭐⭐ (5) = Bought very recently (last 30 days)
- ⭐⭐⭐⭐ (4) = Bought recently (1-2 months ago)
- ⭐⭐⭐ (3) = Bought a while ago (2-6 months)
- ⭐⭐ (2) = Haven't bought in a long time (6-12 months)
- ⭐ (1) = Haven't bought in over a year

**🔄 Frequency Score**
- ⭐⭐⭐⭐⭐ (5) = Buys very often (7+ times a year)
- ⭐⭐⭐⭐ (4) = Buys regularly (4-6 times)
- ⭐⭐⭐ (3) = Buys occasionally (2-3 times)
- ⭐⭐ (2) = Rarely buys (once a year)
- ⭐ (1) = First-time buyer

**💰 Monetary Score**
- ⭐⭐⭐⭐⭐ (5) = Top spender (top 20%)
- ⭐⭐⭐⭐ (4) = High spender
- ⭐⭐⭐ (3) = Average spender
- ⭐⭐ (2) = Low spender
- ⭐ (1) = Very low spender (bottom 20%)

**Customer Segments - What They Mean**

🏆 **Champions** (Best Customers!)
- Buy often, spend a lot, bought recently
- **Action**: Give them VIP treatment, exclusive offers

⭐ **Loyal Customers**
- Buy regularly and recently
- **Action**: Reward their loyalty, ask for referrals

📈 **Potential Loyalists**
- Recent customers showing promise
- **Action**: Engage them more, build the relationship

🆕 **New Customers**
- Just made their first purchase
- **Action**: Welcome them warmly, encourage second purchase

⚠️ **At Risk**
- Used to be great customers, but haven't bought lately
- **Action**: Win them back with special offers

🚨 **Cannot Lose Them**
- High-value customers who stopped buying
- **Action**: Urgent personal outreach needed

😴 **Hibernating/Lost**
- Haven't bought in a very long time
- **Action**: Try win-back campaigns or clean from lists

### 💬 Engagement Scores - How Interested Are They?

**Overall Engagement Score (0-100)**
Think of this like a "relationship temperature":
- **80-100**: 🔥 Very Hot - Super engaged, love your brand
- **60-79**: 🌡️ Warm - Good relationship, engaged
- **40-59**: 😐 Lukewarm - Some interest, needs nurturing
- **20-39**: ❄️ Cold - Low interest, at risk
- **0-19**: 🧊 Frozen - No engagement, likely lost

### ⚠️ Churn Risk - Will They Stop Buying?

**Risk Levels - Traffic Light System**

🟢 **Very Low Risk (0-20)**
- Happy, active customers
- **Action**: Keep doing what you're doing

🟢 **Low Risk (21-40)**
- Stable customers
- **Action**: Maintain regular communication

🟡 **Medium Risk (41-60)**
- Starting to drift away
- **Action**: Increase engagement efforts

🔴 **High Risk (61-80)**
- Likely to stop buying soon
- **Action**: Immediate retention campaign

🔴 **Very High Risk (81-100)**
- About to lose them
- **Action**: Personal outreach, special offers

### 🎯 Customer Journey Stages - Where Are They?

Think of this like a relationship timeline:

**1️⃣ Awareness** 
- Just learning about you
- **Action**: Educate, build trust

**2️⃣ Consideration**
- Made first purchase, testing the waters
- **Action**: Wow them, exceed expectations

**3️⃣ Purchase**
- Regular customer, buying consistently
- **Action**: Keep them happy, cross-sell

**4️⃣ Loyalty**
- Established relationship, reliable customer
- **Action**: Reward loyalty, get feedback

**5️⃣ Advocacy**
- Your best customers, love your brand
- **Action**: Turn them into ambassadors

**6️⃣ Dormant**
- Used to buy, now inactive
- **Action**: Re-engagement needed

### 🎯 How to Use These Metrics

**For Sales Teams**

Daily Use:
1. Check customer's RFM segment before calling
2. Look at engagement score to gauge interest
3. Review churn risk for retention priorities
4. Note journey stage for appropriate messaging

**For Marketing Teams**

Campaign Planning:
1. Segment by RFM for targeted campaigns
2. Use journey stages for lifecycle marketing
3. Create value-based product recommendations
4. Optimize channel mix based on preferences

**For Management**

Strategic Insights:
- Track customer health trends
- Identify revenue risks early
- Optimize resource allocation
- Measure campaign effectiveness

### 📋 Quick Reference Cards

**✅ Healthy Customer:**
- RFM: Champion or Loyal
- Engagement: 60+
- Churn Risk: Low
- Journey: Purchase/Loyalty/Advocacy

**⚠️ At-Risk Customer:**
- RFM: At Risk or Hibernating
- Engagement: Below 40
- Churn Risk: High
- Journey: Dormant

**🔥 Urgent Actions:**
- Very High churn risk
- "Cannot Lose Them" segment
- Engagement below 20

**💡 Opportunities:**
- "Potential Loyalists"
- New customers
- High values alignment

### 🚀 Getting Started

**Your First Steps:**
1. **Identify your Champions** - Take care of your best customers
2. **Find At-Risk customers** - Save valuable relationships
3. **Welcome New Customers** - Make great first impressions
4. **Check Churn Risks** - Prevent customer loss

**Daily Routine:**
- Morning: Check high churn risk customers
- Midday: Review new customer list
- Afternoon: Plan engagement for at-risk segments

### 💡 Pro Tips

**Quick Wins**
- Call every "Cannot Lose Them" customer personally
- Send special offers to "At Risk" customers
- Thank your "Champions" unexpectedly
- Welcome "New Customers" within 24 hours

**Common Mistakes to Avoid**
- Don't ignore declining engagement scores
- Don't treat all customers the same
- Don't wait too long to act on churn risks
- Don't forget to reward loyalty

---

## Core Analytics Features

### 1. Engagement Analytics

**Purpose**: Measure customer interaction across all channels

#### Available Metrics

- **Email Engagement Score (0-100)**: Based on email opens, clicks, responses
- **Website Engagement Score (0-100)**: Based on order frequency and recency
- **WhatsApp Engagement Score (0-100)**: Based on campaign participation
- **Overall Engagement Score (0-100)**: Weighted average across all channels
- **Engagement Level**: Classification from Very Low to Very High

#### How It Works

```python
# Example calculation:
# If customer has email (weight 1), website activity (weight 1), and WhatsApp (weight 1):
# Overall Score = (Email Score + Website Score + WhatsApp Score) / 3
```

#### Business Applications

- **High Engagement (80-100)**: VIP treatment, exclusive offers
- **Medium Engagement (40-79)**: Regular campaigns, loyalty programs
- **Low Engagement (0-39)**: Win-back campaigns, re-engagement efforts

### 2. Customer Journey Stage

**Purpose**: Understand where customers are in their lifecycle

#### Journey Stages

1. **Awareness**: Never purchased, early contact
2. **Consideration**: First-time customer, evaluating
3. **Purchase**: Active customer, regular purchases
4. **Loyalty**: Established relationship, repeat buyer
5. **Advocacy**: Brand advocate, high-value loyal customer
6. **Dormant**: Inactive, potential churn risk

#### Automatic Classification

The system automatically classifies customers based on:
- Purchase history
- RFM segment
- Days since last purchase
- Order count

#### Usage Examples

```python
# Target advocacy stage customers for referral programs
[
    ('customer_journey_stage', '=', 'advocacy'),
    ('rfm_segment', 'in', ['champions', 'loyal_customers'])
]

# Win-back dormant customers
[
    ('customer_journey_stage', '=', 'dormant'),
    ('total_spent', '>', 1000)
]
```

### 3. Multi-Channel Behavior

**Purpose**: Understand how customers interact across channels

#### Metrics

- **Multi-Channel Touchpoints**: Number of channels used (email, WhatsApp, website, phone)
- **Consistency Score (0-100)**: How consistently customer uses multiple channels
- **Preferred Channel**: Primary communication channel

#### Channel Determination Logic

- **Website**: 3+ orders = Website preferred
- **WhatsApp**: Mobile + messages = WhatsApp preferred
- **Email**: Email address + no clear preference = Email preferred
- **Mixed**: Uses multiple channels equally

#### Business Applications

- **High Touchpoints (3+)**: Omnichannel customers, premium treatment
- **Single Channel**: Focus on preferred channel optimization
- **Mixed Preference**: Test different channel combinations

## Advanced Analytics Features

### 1. Churn Prediction

**Purpose**: Identify customers at risk of churning in the next 90 days

#### Churn Risk Assessment

The system uses a weighted algorithm:
- **RFM Segment (40% weight)**: Lost/hibernating = high risk
- **Recency Factor (30% weight)**: Days since last purchase
- **Engagement Factor (20% weight)**: Overall engagement score
- **Journey Stage (10% weight)**: Dormant customers = higher risk

#### Risk Levels

- **Very High Risk (81-100)**: Immediate action required
- **High Risk (61-80)**: Proactive retention campaign
- **Medium Risk (41-60)**: Monitor closely
- **Low Risk (21-40)**: Standard retention efforts
- **Very Low Risk (0-20)**: Stable customers

#### Practical Applications

```python
# Immediate retention campaign for high-risk valuable customers
[
    ('churn_risk_level', 'in', ['high', 'very_high']),
    ('total_spent', '>', 2000),
    ('rfm_segment', 'in', ['champions', 'cannot_lose_them'])
]
```

### 2. Values-Driven Purchase Propensity

**Purpose**: Understand customer preferences for sustainable, premium, and socially responsible products

#### Scoring Method

Based on product purchase history analysis:

- **Eco-Friendly Score**: Calculates percentage of eco-friendly products purchased
  - **Keywords**: `eco`, `organic`, `sustainable`, `green`, `bio`, `natural`
  - **Formula**: `(eco_friendly_products / total_products) * 100`
  - **Bonus**: 20% boost for loyal customers (Champions/Loyal RFM segments)
  - **Default**: 25.0 for customers without purchase history

- **Premium Propensity**: Scoring based on average price point thresholds
  - **>$500**: 90 points (luxury tier)
  - **>$200**: 70 points (premium tier)
  - **>$100**: 50 points (mid-range tier)
  - **>$50**: 30 points (budget-plus tier)
  - **≤$50**: 10 points (budget tier)
  - **Bonus**: 10% boost for loyal customers
  - **Default**: 25.0 for customers without purchase history

- **Social Responsibility**: Calculates percentage of socially responsible products purchased
  - **Keywords**: `fair`, `ethical`, `charity`, `community`, `social`
  - **Formula**: `(social_products / total_products) * 100`
  - **Bonus**: 20% boost for loyal customers (Champions/Loyal RFM segments)
  - **Default**: 25.0 for customers without purchase history

#### Score Ranges

- **80-100**: Strong preference, primary motivator
- **60-79**: Moderate preference, secondary factor
- **40-59**: Neutral, not a key factor
- **20-39**: Low preference, unlikely motivator
- **0-19**: No preference or insufficient data

#### Marketing Applications

```python
# Eco-friendly focused campaign
[
    ('eco_friendly_score', '>', 70),
    ('customer_journey_stage', 'in', ['loyalty', 'advocacy'])
]

# Premium product launch to high-propensity customers
[
    ('premium_product_propensity', '>', 80),
    ('rfm_segment', 'in', ['champions', 'loyal_customers'])
]
```

### 3. Cohort Analysis

**Purpose**: Track customer behavior over time by acquisition period

#### Key Metrics

- **Retention Rate**: Percentage of customers still active per period
- **Revenue per Cohort**: Total and average revenue by acquisition month
- **Customer Lifetime Value**: Average value per customer over time
- **Churn Risk Distribution**: Risk levels within each cohort

#### Accessing Cohort Analysis

1. Navigate to **WhatsApp Marketing Automation > Reports > Cohort Analysis**
2. Filter by recent cohorts (last 12 months)
3. Use pivot view for heatmap visualization
4. Switch to graph view for trend analysis

#### Business Insights

- **Identify Best Acquisition Periods**: Which months bring highest-value customers
- **Predict Revenue**: Forecast revenue from existing cohorts
- **Optimize Retention**: Compare retention rates across cohorts
- **Budget Allocation**: Invest more in high-performing acquisition channels

## Product Category Analytics

### Overview

**Purpose**: Understand customer preferences and predict future purchases based on their product category buying patterns

Product Category Analytics provides deep insights into what types of products each customer prefers, helping you:
- Personalize product recommendations
- Optimize inventory by customer segment
- Create category-specific marketing campaigns
- Identify cross-selling opportunities

### Available Metrics

#### 1. Favorite Product Categories

**What it shows**: The top 3 product categories the customer purchases most frequently

**How it's calculated**:
- Analyzes all confirmed sales orders
- Groups products by category
- Ranks by combination of:
  - Total spending in category (60% weight)
  - Number of purchases (30% weight)
  - Recency of purchases (10% weight)

**Business Application**:
- Use for personalized product recommendations
- Create category-specific promotions
- Focus inventory on popular categories

#### 2. Category Diversity Score (0-100)

**What it measures**: How varied the customer's purchases are across different categories

**Score Interpretation**:
- **80-100**: Very diverse buyer (8+ categories)
- **60-79**: Diverse buyer (6-7 categories)
- **40-59**: Moderate diversity (4-5 categories)
- **20-39**: Focused buyer (2-3 categories)
- **0-19**: Single category buyer

**Business Value**:
- **High diversity**: Good candidates for cross-selling
- **Low diversity**: Deep expertise in specific categories

#### 3. Category Purchase Patterns

**Insights Provided**:
- **Recent Focus**: Categories purchased in last 6 months
- **Historical Preferences**: All-time category preferences
- **Seasonal Patterns**: Time-based category preferences
- **Growth Categories**: Categories with increasing purchase frequency

#### 4. Top Category Analysis

**Metrics**:
- **Primary Category**: Most purchased category by revenue
- **Category Share**: Percentage of total spending in top category
- **Category Loyalty**: Consistency of category preferences over time

### Category Spending Breakdown

The system provides detailed spending analysis:
- Revenue by category
- Average order value by category
- Purchase frequency by category
- Last purchase date by category

### Using Category Analytics for Segmentation

#### High-Value Category Segments

```python
# Premium Electronics Buyers
[
    ('top_category_name', '=', 'Electronics'),
    ('average_order_value', '>', 500),
    ('rfm_segment', 'in', ['champions', 'loyal_customers'])
]

# Fashion Enthusiasts
[
    ('favorite_product_categories', 'ilike', '%Fashion%'),
    ('category_diversity_score', '<', 40),  # Focused on fashion
    ('purchase_count', '>', 5)
]
```

#### Cross-Selling Opportunities

```python
# Customers buying in only one category (ripe for expansion)
[
    ('category_diversity_score', '<', 20),
    ('total_spent', '>', 1000),
    ('customer_journey_stage', 'in', ['purchase', 'loyalty'])
]

# Diverse buyers for new category launches
[
    ('category_diversity_score', '>', 70),
    ('engagement_level', 'in', ['high', 'very_high'])
]
```

### Category-Based Campaign Examples

#### 1. Category Abandonment Prevention

Target customers who haven't purchased from their favorite category recently:
```python
[
    ('favorite_product_categories', 'ilike', '%Electronics%'),
    ('days_since_last_purchase', '>', 90),
    ('rfm_segment', '!=', 'lost')
]
```

#### 2. New Category Introduction

Introduce complementary categories to single-category buyers:
```python
[
    ('top_category_name', '=', 'Home & Garden'),
    ('category_diversity_score', '<', 30),
    ('total_spent', '>', 500)
]
```

#### 3. Seasonal Category Campaigns

Target based on historical seasonal patterns:
```python
[
    ('category_purchase_pattern', 'ilike', '%Winter Sports%'),
    ('rfm_monetary_score', '>=', 3)
]
```

### Integration with Other Analytics

Category analytics enhances other metrics:

1. **With RFM Analysis**: Identify champion customers in specific categories
2. **With Churn Prediction**: Detect category-specific churn risks
3. **With Values Analytics**: Match eco-friendly products to sustainability-conscious customers
4. **With Engagement Scores**: Correlate category preferences with channel engagement

## Emerging Trends Analytics

### 1. Social Commerce Integration

**Purpose**: Track and optimize social media driven sales

#### Metrics Tracked

- **Social Media Source**: Primary platform (Facebook, Instagram, TikTok, etc.)
- **Social Referral Count**: Number of social-driven purchases
- **Social Engagement Score**: Interaction level with social content
- **Social Conversion Rate**: Conversion from social media traffic

#### Data Sources

The system analyzes:
- UTM parameters from sale orders
- Campaign sources and mediums
- Referral patterns

#### Optimization Strategies

```python
# High-performing Instagram customers
[
    ('social_media_source', '=', 'instagram'),
    ('social_conversion_rate', '>', 50),
    ('age', '>=', 18),
    ('age', '<=', 35)
]

# Social media testing segment
[
    ('social_engagement_score', '>', 40),
    ('social_media_source', '=', 'none'),  # Not yet acquired via social
    ('age', '<=', 45)
]
```

### 2. BNPL & Mobile Commerce

**Purpose**: Understand modern payment preferences and device behavior

#### BNPL Analytics

- **Usage Frequency**: Never, Rarely, Sometimes, Frequently, Always
- **Preference Score**: Likelihood to use BNPL options
- **Target Demographics**: Age and spending patterns of BNPL users

#### Mobile Commerce Analytics

- **Device Preference**: Smartphone, Tablet, Desktop, Mixed
- **Mobile Commerce Score**: Mobile vs desktop shopping behavior
- **Average Order Values**: Spending by device type
- **Mobile Conversion Rate**: Success rate on mobile devices

#### Business Applications

```python
# BNPL-friendly segment for payment option testing
[
    ('bnpl_usage_frequency', 'in', ['frequently', 'always']),
    ('age', '>=', 18),
    ('age', '<=', 40)
]

# Mobile optimization target group
[
    ('mobile_device_preference', '=', 'smartphone'),
    ('mobile_conversion_rate', '<', 50),  # Room for improvement
    ('mobile_commerce_score', '>', 60)
]
```

## Reports and Dashboards

### Available Reports

#### Customer Analytics Reports

1. **Customer Demographics Analysis**: Age, location, purchase patterns
2. **RFM Analysis**: Recency, Frequency, Monetary segmentation
3. **Cohort Analysis**: Time-based customer behavior tracking
4. **Churn Risk Analysis**: Predictive customer retention insights
5. **Customer Acquisition Report**: Source performance and channel analysis

#### Category Performance Reports

6. **Category Sales Performance**: Spending tier × category matrix analysis
7. **Category × Spending Tier Matrix**: Cross-analysis visualization
8. **Category Growth Trends**: Time-based category performance
9. **Top Products by Category**: Product-level performance analysis
10. **Top Products Analysis**: Best performing products across all categories
11. **Top Services Analysis**: Service-specific performance metrics
12. **Products by Customer Tier**: Tier preference analysis

### Creating Custom Views

#### Pivot Table Analysis

1. Go to **Contacts > Contacts**
2. Switch to **Pivot View**
3. Add fields:
   - Rows: `customer_journey_stage`, `rfm_segment`
   - Columns: `engagement_level`, `churn_risk_level`
   - Measures: `total_spent`, `days_since_last_purchase`

#### Graph Visualizations

1. Switch to **Graph View**
2. Create charts for:
   - Engagement scores by age group
   - Churn risk by RFM segment
   - Social commerce performance by platform
   - BNPL usage by generation

### Export and Integration

- **Excel Export**: All analytics data can be exported for external analysis
- **API Access**: Integrate with BI tools via Odoo API
- **Scheduled Reports**: Set up automated report generation

## Category Performance Reports

### Overview

The Category Performance Reports provide comprehensive analysis of how different product categories perform across customer segments, matching the Excel requirements for spending tier × category matrix analysis.

### Available Reports

Navigate to **WhatsApp Marketing Automation > Reports > Category Performance**:

#### 1. Category Sales Performance

**Purpose**: Comprehensive analysis of sales performance by category and customer spending tier

**Key Metrics**:
- Total Revenue by Category × Spending Tier
- Order Count and Customer Count
- Average Order Value
- Revenue Growth Rate (vs previous period)
- Market Share Analysis

**Views Available**:
- **Pivot View**: Spending tier × category matrix (matches Excel DAYA BELI × PRODUK JASA)
- **Graph View**: Visual comparisons and trends
- **List View**: Detailed records with growth indicators

**Business Applications**:
- Identify which categories perform best with premium vs budget customers
- Optimize product mix for different customer segments
- Focus marketing efforts on high-performing combinations

#### 2. Category × Spending Tier Matrix

**Purpose**: Cross-analysis matrix showing the intersection of customer spending power and product preferences

**Special Features**:
- Heat map visualization in pivot view
- Automatic calculation of revenue share percentages
- Period comparison (default: last month with YoY comparison)
- Drill-down to specific category-tier combinations

**How to Use**:
1. Open the report
2. Select time period (default: 1 month)
3. Use pivot view for matrix analysis
4. Click cells to drill down to customer lists

#### 3. Category Growth Trends

**Purpose**: Track category performance over time with growth analysis

**Insights Provided**:
- Month-over-month growth rates
- Seasonal patterns by category
- Emerging and declining categories
- Forecast based on historical trends

**Visualization Options**:
- Line charts for trend analysis
- Bar charts for period comparison
- Stacked charts for market share evolution

#### 4. Top Products by Category

**Purpose**: Detailed product-level analysis within each category

**Key Features**:
- Top 20 products per category
- Customer tier breakdown for each product
- Shows which products appeal to VIP vs budget customers
- Growth metrics and ranking

**Special Insights**:
- **Tier Revenue Breakdown**: See revenue from VIP, Premium, Gold, etc. for each product
- **Cross-Tier Appeal**: Identify products that work across all customer segments
- **Category Champions**: Best performers in each category

#### 5. Top Products/Services Analysis

**Separate Reports for**:
- **Top Products Analysis**: Physical products ranking
- **Top Services Analysis**: Service offerings ranking

These match your Excel requirements for "Top Products by Category" and "Top Services by Category" analysis.

### Using Category Reports Effectively

#### Quick Start Guide

1. **Daily Review**:
   - Check Category × Tier Matrix for yesterday's performance
   - Identify any unusual patterns or opportunities
   - Note categories with declining performance

2. **Weekly Analysis**:
   - Review Category Growth Trends
   - Compare week-over-week performance
   - Identify categories needing attention

3. **Monthly Planning**:
   - Analyze full month Category Sales Performance
   - Plan inventory based on tier preferences
   - Adjust marketing focus based on insights

#### Advanced Analysis Techniques

**1. Finding Hidden Opportunities**:
```
Filters to apply:
- Revenue Growth Rate > 20%
- Customer Spending Tier = "Silver" or "Bronze"
- Total Revenue < $10,000
→ Identifies growing categories in mid-tier segments
```

**2. Premium Customer Focus**:
```
Filters to apply:
- Customer Spending Tier in ["VIP", "Premium", "Gold"]
- Category Revenue Share > 5%
→ Shows categories that matter to high-value customers
```

**3. Cross-Selling Candidates**:
```
Steps:
1. Go to Top Products by Category
2. Filter for products with diverse tier appeal
3. Note products with balanced revenue across tiers
→ These products work for cross-tier campaigns
```

### Report Customization

#### Time Period Configuration

All reports support flexible time periods:
- **Default**: Last month (configurable)
- **Options**: 1-12 months
- **Comparison**: Automatic vs previous period
- **Custom Ranges**: Use date filters

#### Filters and Grouping

**Common Filters**:
- Period filters (Current Month, Last 3 Months, etc.)
- Spending tier filters (Premium Tiers, Budget Tiers, etc.)
- Performance filters (High Revenue, Growing Categories, etc.)
- Product type filters (Products, Services, Consumables)

**Grouping Options**:
- By Category
- By Spending Tier
- By Period
- By Parent Category
- By Product Type

### Integration with Customer Analytics

Category reports complement customer-level analytics:

1. **From Customer to Category**:
   - View customer's favorite categories
   - Click through to category performance
   - See how their preferences compare to their tier

2. **From Category to Customers**:
   - Start with high-performing category
   - Drill down to customer list
   - Create targeted segments

3. **Campaign Creation**:
   - Use insights to create segments
   - Target based on category preferences
   - Personalize by spending tier

## Practical Applications

### Campaign Optimization

#### Engagement-Based Campaigns

```python
# Re-engagement campaign for medium engagement customers
[
    ('engagement_level', '=', 'medium'),
    ('churn_risk_level', 'in', ['medium', 'high']),
    ('total_spent', '>', 500)
]
```

#### Journey-Based Messaging

```python
# Loyalty program invitation for purchase stage customers
[
    ('customer_journey_stage', '=', 'purchase'),
    ('purchase_count', '>=', 3),
    ('days_since_last_purchase', '<=', 60)
]
```

### Product Marketing

#### Values-Based Product Launches

```python
# Eco-friendly product launch to sustainability advocates
[
    ('eco_friendly_score', '>', 70),
    ('social_responsibility_score', '>', 60),
    ('customer_journey_stage', 'in', ['loyalty', 'advocacy'])
]
```

#### Premium Product Targeting

```python
# Luxury line introduction to premium propensity customers
[
    ('premium_product_propensity', '>', 80),
    ('rfm_segment', 'in', ['champions', 'loyal_customers']),
    ('average_order_value_desktop', '>', 200)
]
```

### Retention Strategies

#### Churn Prevention

```python
# Proactive retention for high-risk valuable customers
[
    ('churn_risk_level', 'in', ['high', 'very_high']),
    ('rfm_segment', 'in', ['champions', 'cannot_lose_them']),
    ('total_spent', '>', 3000)
]
```

#### Win-Back Campaigns

```python
# Win-back dormant high-value customers
[
    ('customer_journey_stage', '=', 'dormant'),
    ('total_spent', '>', 2000),
    ('days_since_last_purchase', '>', 180),
    ('days_since_last_purchase', '<', 365)
]
```

## Best Practices

### Data Quality

1. **Regular Updates**: Ensure customer data is current and complete
2. **UTM Tracking**: Implement consistent UTM parameters for social campaigns
3. **Payment Terms**: Set up clear payment terms for BNPL detection
4. **Email Campaigns**: Send regular emails to generate engagement data

### Segmentation Strategy

1. **Start Simple**: Begin with basic RFM segments, then add complexity
2. **Test Small**: Always test with 50-100 customers before full campaigns
3. **Monitor Performance**: Track segment performance and adjust criteria
4. **Document Success**: Record successful segments for reuse

### Campaign Timing

1. **Engagement Patterns**: Send to high-engagement customers during peak hours
2. **Journey Stage**: Time messages based on customer lifecycle stage
3. **Churn Risk**: Immediate action for high-risk customers
4. **Social Commerce**: Align with social media posting schedules

### Measurement and Optimization

1. **A/B Testing**: Test different segments against each other
2. **Cohort Comparison**: Compare performance across acquisition periods
3. **Channel Optimization**: Focus on preferred channels for each segment
4. **Predictive Accuracy**: Monitor churn prediction accuracy and adjust

## Troubleshooting

### Common Issues

#### Low Engagement Scores

**Symptoms**: Most customers show low engagement scores
**Solutions**:
- Verify email campaigns are being sent
- Check WhatsApp campaign participation
- Ensure recent order data is available
- Review engagement calculation weights

#### Inaccurate Churn Predictions

**Symptoms**: Churn predictions don't match actual behavior
**Solutions**:
- Review RFM segment accuracy
- Adjust engagement scoring criteria
- Verify purchase data completeness
- Consider industry-specific factors

#### Missing Social Commerce Data

**Symptoms**: All customers show "none" for social media source
**Solutions**:
- Implement UTM tracking on social campaigns
- Verify UTM parameter mapping
- Check sale order source field population
- Set up social media campaign tracking

### Data Quality Checks

1. **Engagement Scores**: Should show variation, not all zeros
2. **Journey Stages**: Should have customers in all stages
3. **RFM Segments**: Should show normal distribution
4. **Churn Risk**: Should vary based on customer behavior

### Performance Optimization

1. **Computed Fields**: May take time to calculate for large datasets
2. **Database Indexes**: Ensure fields used in segments are indexed
3. **Batch Processing**: Process analytics updates in batches
4. **Cache Management**: Clear cache after major data updates

## Integration Guide

### CRM Integration

The advanced analytics integrate seamlessly with Odoo's CRM:
- **Lead Scoring**: Use engagement scores for lead qualification
- **Opportunity Management**: Prioritize based on churn risk
- **Pipeline Forecasting**: Use cohort analysis for revenue prediction

### Marketing Automation

- **Campaign Triggers**: Automatically trigger campaigns based on analytics
- **Dynamic Segmentation**: Segments update automatically as data changes
- **Personalization**: Use analytics data for message personalization

### Third-Party Integration

#### BI Tools

```python
# Export analytics data via API
analytics_data = odoo.env['res.partner'].search([
    ('customer_rank', '>', 0)
]).read([
    'name', 'rfm_segment', 'engagement_level',
    'churn_risk_score', 'customer_journey_stage'
])
```

#### Social Media Platforms

- **Facebook/Instagram**: Track UTM parameters from social ads
- **TikTok**: Monitor social commerce performance
- **LinkedIn**: B2B social commerce tracking

### API Endpoints

The module provides REST API access to:
- Customer analytics data
- Segment definitions
- Cohort analysis results
- Campaign performance metrics

## Configuration and Customization

### Fully Configurable Analytics

All analytics thresholds and settings are now fully configurable through the user interface - no hardcoded values remain in the system.

#### Configurable Elements

**1. Customer Spending Tiers**
- Navigate to: **WhatsApp Marketing Automation > Configuration > Customer Spending Tiers**
- Configure: Tier names, codes, thresholds, and colors
- Default: 8 tiers (VIP, Premium, Gold, Silver, Bronze, Standard, Basic, Entry)
- Customizable to match your business model (e.g., A/B/C/D/E/F/G/H)

**2. Age Group Configuration**
- Navigate to: **WhatsApp Marketing Automation > Configuration > Customer Age Groups**
- Configure: Age ranges, group names, and display order
- Default groups: 18-24, 25-34, 35-44, 45-54, 55-64, 65+
- Add custom groups as needed

**3. Acquisition Source Management**
- Navigate to: **WhatsApp Marketing Automation > Configuration > Customer Acquisition Sources**
- Configure: Source names, codes, and categories
- Track custom channels specific to your business

**4. Analytics Package Settings**
- Navigate to: **Settings > WhatsApp Marketing > Analytics Configuration**
- Enable/disable specific analytics modules
- Configure calculation parameters
- Set update frequencies

#### Multi-Currency Support

The system automatically handles multiple currencies:
- All monetary values converted to company base currency
- Consistent analysis across international customers
- No hardcoded currency assumptions
- Automatic exchange rate updates

#### Dynamic Date Calculations

All date-based analytics use dynamic calculations:
- No hardcoded years or dates
- Automatic adjustment for current period
- Configurable lookback periods
- Timezone-aware calculations

### Customization Best Practices

1. **Start with Defaults**: The system includes sensible defaults for all configurations
2. **Test Changes**: Make configuration changes in a test environment first
3. **Document Customizations**: Keep notes on why specific thresholds were chosen
4. **Regular Review**: Review configurations quarterly as your business evolves

## Conclusion

Advanced Analytics transforms your WhatsApp marketing from basic messaging to sophisticated, data-driven customer engagement. With the latest enhancements including product category analytics, calculation transparency, and fully configurable settings, you can:

1. **Predict Customer Behavior**: Know who will churn before they do
2. **Understand Product Preferences**: Deep insights into category buying patterns
3. **Optimize Channel Mix**: Focus on preferred customer channels
4. **Personalize at Scale**: Target based on values, categories, and preferences
5. **Cross-Analyze Performance**: Spending tier × category matrix insights
6. **Trust Your Data**: Full transparency on how every metric is calculated
7. **Customize Everything**: No hardcoded values - configure to match your business
8. **Stay Ahead of Trends**: Leverage 2025 commerce trends

### What's Next

1. **Explore Category Analytics**: Review the new Product Categories tab in customer records
2. **Run Category Reports**: Access the new Category Performance reports suite
3. **Check Calculation Transparency**: Understand how each metric is calculated
4. **Configure Settings**: Customize spending tiers, age groups, and sources
5. **Create Category Segments**: Use category preferences for targeted campaigns
6. **Analyze Tier × Category Matrix**: Discover which products work for which customers
7. **Monitor Growth Trends**: Track category performance over time

The enhanced analytics platform now provides complete visibility into both customer behavior and product performance, with full transparency and configurability. This positions your business at the forefront of customer intelligence, enabling sophisticated marketing strategies that drive growth and customer satisfaction.

---

**Need More Help?**

- [Segmentation Quick Reference](./SEGMENTATION_QUICK_REFERENCE.md) - Copy-paste segment examples
- [Customer Segmentation Guide](./CUSTOMER_SEGMENTATION_FROM_REPORTS_GUIDE.md) - Detailed segmentation strategies
- [Customer Demographics Reports](./CUSTOMER_DEMOGRAPHICS_REPORTS_USER_GUIDE.md) - Report usage guide