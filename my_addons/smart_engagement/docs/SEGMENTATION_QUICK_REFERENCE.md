# Customer Segmentation Quick Reference

## Common Segment Rules - Copy & Paste Ready

### 🎯 High-Value Customers
```python
[
    ('total_invoiced', '>', 5000),
    ('is_company', '=', False),
    ('active', '=', True)
]
```

### 👥 Age-Based Segments

**Gen Z (18-27)**
```python
[
    ('age', '>=', 18),
    ('age', '<=', 27),
    ('active', '=', True)
]
```

**Millennials (28-43)**
```python
[
    ('age', '>=', 28),
    ('age', '<=', 43),
    ('active', '=', True)
]
```

**Gen X (44-59)**
```python
[
    ('age', '>=', 44),
    ('age', '<=', 59),
    ('active', '=', True)
]
```

**Baby Boomers (60-78)**
```python
[
    ('age', '>=', 60),
    ('age', '<=', 78),
    ('active', '=', True)
]
```

### 💰 RFM Segments

> 📖 **New to RFM Analysis?** See the [Advanced Analytics User Guide](./ADVANCED_ANALYTICS_USER_GUIDE.md#business-user-quick-guide) for detailed explanations of RFM scoring, customer segments, and business applications.

**Champions (Best Customers)**
```python
[
    ('rfm_segment', '=', 'champions'),
    ('active', '=', True)
]
# OR using RFM scores:
[
    ('rfm_score', '>=', 12),
    ('recency_score', '>=', 4),
    ('frequency_score', '>=', 4),
    ('monetary_score', '>=', 4)
]
```

**At Risk Customers**
```python
[
    ('rfm_segment', '=', 'at_risk'),
    ('active', '=', True)
]
# OR using specific criteria:
[
    ('recency_score', '<=', 2),
    ('frequency_score', '>=', 2),
    ('monetary_score', '>=', 3)
]
```

**New Customers**
```python
[
    ('rfm_segment', '=', 'new_customers'),
    ('active', '=', True)
]
# OR using recency and frequency:
[
    ('recency_score', '>=', 4),
    ('frequency_score', '<=', 2),
    ('monetary_score', '<=', 2)
]
```

**Cannot Lose Them (High Value, Inactive)**
```python
[
    ('rfm_segment', '=', 'cannot_lose_them'),
    ('active', '=', True)
]
# OR using specific criteria:
[
    ('recency_score', '<=', 2),
    ('frequency_score', '>=', 4),
    ('monetary_score', '>=', 4)
]
```

**Loyal Customers**
```python
[
    ('rfm_segment', '=', 'loyal_customers'),
    ('active', '=', True)
]
```

**Potential Loyalists**
```python
[
    ('rfm_segment', '=', 'potential_loyalists'),
    ('active', '=', True)
]
```

### 🗓️ Time-Based Segments

**Recent Purchasers (Last 30 Days)**
```python
[
    ('sale_order_ids.date_order', '>', fields.Date.today() - timedelta(days=30)),
    ('sale_order_ids.state', 'in', ['sale', 'done'])
]
```

**Birthday This Month**
```python
[
    ('date_of_birth', '!=', False),
    ('birth_month', '=', fields.Date.today().month)
]
```

**Anniversary Customers**
```python
[
    ('create_date_month', '=', fields.Date.today().month),
    ('customer_rank', '>', 0)
]
```

### 📍 Geographic Segments

**Major Cities**
```python
[
    ('city', 'in', ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
    ('country_id.code', '=', 'US')
]
```

**State-Based**
```python
[
    ('state_id.code', 'in', ['CA', 'TX', 'FL', 'NY']),
    ('is_company', '=', False)
]
```

### 🛒 Purchase Behavior

**Frequent Buyers**
```python
[
    ('sale_order_count', '>', 12),  # More than once per month
    ('active', '=', True)
]
```

**Big Spenders**
```python
[
    ('sale_order_ids.amount_total', '>', 1000),  # Any order over $1000
    ('sale_order_ids.state', 'in', ['sale', 'done'])
]
```

**Discount Seekers**
```python
[
    ('sale_order_ids.amount_discount', '>', 0),
    ('sale_order_count', '>', 3)
]
```

### 🔄 Engagement Segments

**Active Customers**
```python
[
    ('sale_order_ids.date_order', '>', fields.Date.today() - timedelta(days=90)),
    ('email', '!=', False),
    ('mobile', '!=', False)
]
```

**Dormant Customers**
```python
[
    ('sale_order_ids.date_order', '<', fields.Date.today() - timedelta(days=180)),
    ('total_invoiced', '>', 0)
]
```

### 🎁 Special Segments

**VIP Customers (Top 10%)**
```python
[
    ('total_invoiced', '>', 10000),
    ('sale_order_count', '>', 20),
    ('active', '=', True)
]
```

**First-Time Buyers**
```python
[
    ('sale_order_count', '=', 1),
    ('sale_order_ids.state', 'in', ['sale', 'done'])
]
```

**B2B Customers**
```python
[
    ('is_company', '=', True),
    ('customer_rank', '>', 0),
    ('active', '=', True)
]
```

### 📊 Advanced Analytics Segments

**High Engagement Customers**
```python
[
    ('engagement_level', '=', 'very_high'),
    ('overall_engagement_score', '>', 80),
    ('active', '=', True)
]
```

**Multi-Channel Champions**
```python
[
    ('multichannel_touchpoints', '>=', 3),
    ('multichannel_consistency_score', '>', 70),
    ('preferred_channel', '!=', 'mixed')
]
```

**At-Risk High Engagement**
```python
[
    ('churn_risk_level', 'in', ['high', 'very_high']),
    ('overall_engagement_score', '>', 60),
    ('rfm_segment', 'in', ['champions', 'loyal_customers'])
]
```

**Journey Stage Targeting**
```python
# Advocacy Stage (Brand Advocates)
[
    ('customer_journey_stage', '=', 'advocacy'),
    ('rfm_segment', 'in', ['champions', 'loyal_customers']),
    ('active', '=', True)
]

# Dormant Customers (Win-Back)
[
    ('customer_journey_stage', '=', 'dormant'),
    ('churn_risk_score', '>', 60),
    ('total_spent', '>', 1000)
]
```

### 🌱 Values-Driven Segments

**Sustainability Advocates**
```python
[
    ('eco_friendly_score', '>', 70),
    ('premium_product_propensity', '>', 50),
    ('active', '=', True)
]
```

**Premium Product Enthusiasts**
```python
[
    ('premium_product_propensity', '>', 80),
    ('rfm_segment', 'in', ['champions', 'loyal_customers']),
    ('social_responsibility_score', '>', 60)
]
```

**Socially Conscious Buyers**
```python
[
    ('social_responsibility_score', '>', 75),
    ('eco_friendly_score', '>', 60),
    ('customer_journey_stage', 'in', ['loyalty', 'advocacy'])
]
```

### 📱 Social Commerce Segments

**Social Media Customers**
```python
[
    ('social_media_source', '!=', 'none'),
    ('social_engagement_score', '>', 40),
    ('social_referral_count', '>', 1)
]
```

**Instagram Shoppers**
```python
[
    ('social_media_source', '=', 'instagram'),
    ('social_conversion_rate', '>', 30),
    ('age', '>=', 18),
    ('age', '<=', 35)
]
```

**Facebook Commerce**
```python
[
    ('social_media_source', '=', 'facebook'),
    ('social_referral_count', '>', 2),
    ('social_engagement_score', '>', 50)
]
```

**High Social Conversion**
```python
[
    ('social_conversion_rate', '>', 60),
    ('social_media_source', '!=', 'none'),
    ('customer_journey_stage', 'in', ['purchase', 'loyalty'])
]
```

### 💳 BNPL & Mobile Commerce Segments

**BNPL Frequent Users**
```python
[
    ('bnpl_usage_frequency', 'in', ['frequently', 'always']),
    ('bnpl_preference_score', '>', 60),
    ('active', '=', True)
]
```

**Mobile-First Customers**
```python
[
    ('mobile_device_preference', '=', 'smartphone'),
    ('mobile_commerce_score', '>', 70),
    ('mobile_conversion_rate', '>', 50)
]
```

**High Mobile Spenders**
```python
[
    ('average_order_value_mobile', '>', 150),
    ('mobile_commerce_score', '>', 60),
    ('mobile_device_preference', 'in', ['smartphone', 'tablet'])
]
```

**Cross-Device Shoppers**
```python
[
    ('mobile_device_preference', '=', 'mixed'),
    ('average_order_value_mobile', '>', 0),
    ('average_order_value_desktop', '>', 0)
]
```

**BNPL + Mobile Combo**
```python
[
    ('bnpl_preference_score', '>', 40),
    ('mobile_commerce_score', '>', 60),
    ('age', '>=', 18),
    ('age', '<=', 40)
]
```

## Quick Tips

### Combining Conditions

**AND Logic (All conditions must be true)**
```python
[
    ('age', '>', 25),
    ('city', '=', 'New York'),
    ('total_invoiced', '>', 1000)
]
```

**OR Logic (Any condition can be true)**
```python
[
    '|', '|',
    ('total_invoiced', '>', 5000),
    ('sale_order_count', '>', 20),
    ('vip_customer', '=', True)
]
```

**Complex Logic (Mix of AND/OR)**
```python
[
    ('active', '=', True),
    '|',
    ('age', '<', 30),
    '&',
    ('age', '>=', 30),
    ('total_invoiced', '>', 5000)
]
# Active AND (Age < 30 OR (Age >= 30 AND Total > 5000))
```

### Common Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `age` | Integer | Computed from date_of_birth |
| `date_of_birth` | Date | Customer's birth date |
| `total_invoiced` | Float | Total amount invoiced |
| `sale_order_count` | Integer | Number of sales orders |
| `customer_rank` | Integer | Customer ranking (> 0 = is customer) |
| `city` | Char | City name |
| `state_id` | Many2one | State/Province |
| `country_id` | Many2one | Country |
| `mobile` | Char | Mobile phone number |
| `email` | Char | Email address |
| `create_date` | Datetime | When contact was created |
| `active` | Boolean | Is contact active |
| `is_company` | Boolean | Company vs Individual |
| **RFM Fields** | | |
| `rfm_segment` | Selection | RFM segment (champions, at_risk, etc.) |
| `rfm_score` | Integer | Combined RFM score (3-15) |
| `recency_score` | Integer | Recency score (1-5) |
| `frequency_score` | Integer | Frequency score (1-5) |
| `monetary_score` | Integer | Monetary score (1-5) |
| `days_since_last_purchase` | Integer | Days since last purchase |
| `purchase_count` | Integer | Purchase count (last 12 months) |
| `total_spent` | Float | Total spent (last 12 months) |
| **Advanced Analytics Fields** | | |
| `engagement_level` | Selection | Overall engagement level (very_low to very_high) |
| `overall_engagement_score` | Float | Combined engagement score (0-100) |
| `email_engagement_score` | Float | Email engagement score (0-100) |
| `website_engagement_score` | Float | Website engagement score (0-100) |
| `whatsapp_engagement_score` | Float | WhatsApp engagement score (0-100) |
| `customer_journey_stage` | Selection | Current journey stage (awareness to advocacy) |
| `multichannel_touchpoints` | Integer | Number of channels customer uses |
| `multichannel_consistency_score` | Float | Multi-channel consistency (0-100) |
| `preferred_channel` | Selection | Primary communication channel |
| `churn_risk_level` | Selection | Churn risk level (very_low to very_high) |
| `churn_risk_score` | Float | Churn probability in next 90 days (0-100) |
| `eco_friendly_score` | Float | Preference for eco-friendly products (0-100) |
| `premium_product_propensity` | Float | Likelihood to buy premium products (0-100) |
| `social_responsibility_score` | Float | Preference for ethical brands (0-100) |
| `social_media_source` | Selection | Primary social media source |
| `social_referral_count` | Integer | Number of social media referrals |
| `social_engagement_score` | Float | Social media engagement (0-100) |
| `social_conversion_rate` | Float | Social media conversion rate (0-100) |
| `bnpl_usage_frequency` | Selection | BNPL usage frequency |
| `bnpl_preference_score` | Float | BNPL preference score (0-100) |
| `mobile_device_preference` | Selection | Preferred device for shopping |
| `mobile_commerce_score` | Float | Mobile vs desktop behavior (0-100) |
| `mobile_conversion_rate` | Float | Mobile conversion rate (0-100) |
| `average_order_value_mobile` | Float | Average order value on mobile |
| `average_order_value_desktop` | Float | Average order value on desktop |

### Date Calculations

```python
# Import at top of domain definition
from datetime import timedelta
import fields

# Last 30 days
fields.Date.today() - timedelta(days=30)

# Last 3 months
fields.Date.today() - timedelta(days=90)

# Last year
fields.Date.today() - timedelta(days=365)

# Specific date
'2024-01-01'

# Current month
fields.Date.today().month

# Current year
fields.Date.today().year
```

## Testing Your Segments

1. **Always Preview First**
   - Click "Preview Customers" button
   - Check customer count
   - Verify a few customers match expectations

2. **Start Small**
   - Test with 10-20 customers first
   - Send test campaign
   - Monitor results

3. **Common Mistakes to Avoid**
   - Using wrong field names
   - Forgetting to check `active = True`
   - Making segments too narrow
   - Not testing with preview

## Need More Help?

See the full guide: [CUSTOMER_SEGMENTATION_FROM_REPORTS_GUIDE.md](./CUSTOMER_SEGMENTATION_FROM_REPORTS_GUIDE.md)