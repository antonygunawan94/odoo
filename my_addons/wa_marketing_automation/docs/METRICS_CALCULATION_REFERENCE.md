# Metrics Calculation Reference Guide

## Comprehensive Technical Documentation for All Analytics Metrics

This document provides detailed explanations of how every metric in the WhatsApp Marketing Automation module is calculated, including formulas, algorithms, and business logic.

## Table of Contents

1. [RFM Analysis Calculations](#rfm-analysis-calculations)
2. [Engagement Score Calculations](#engagement-score-calculations)
3. [Churn Prediction Algorithm](#churn-prediction-algorithm)
4. [Customer Journey Stage Logic](#customer-journey-stage-logic)
5. [Multi-Channel Behavior Scoring](#multi-channel-behavior-scoring)
6. [Values-Driven Propensity Calculations](#values-driven-propensity-calculations)
7. [Social Commerce Metrics](#social-commerce-metrics)
8. [BNPL & Mobile Commerce Calculations](#bnpl--mobile-commerce-calculations)
9. [Cohort Analysis SQL Logic](#cohort-analysis-sql-logic)
10. [Customer Demographics Calculations](#customer-demographics-calculations)

---

## RFM Analysis Calculations

### Overview
RFM (Recency, Frequency, Monetary) analysis segments customers based on their purchasing behavior over the last 12 months.

### Data Source
- **Table**: `sale_order` (filtered by `state IN ('sale', 'done')`)
- **Time Window**: Last 12 months from current date
- **Partner Filter**: `customer_rank > 0` (actual customers only)

### 1. Days Since Last Purchase (Recency)

**Formula**:
```python
days_since_last_purchase = (today - last_order_date).days
```

**Implementation**:
```python
def _compute_rfm_data(self):
    for partner in self:
        if not hasattr(partner, 'sale_order_ids'):
            partner.days_since_last_purchase = 9999
            continue
            
        twelve_months_ago = date.today() - timedelta(days=365)
        recent_orders = partner.sale_order_ids.filtered(
            lambda o: o.state in ('sale', 'done') and 
            o.date_order.date() >= twelve_months_ago
        )
        
        if recent_orders:
            last_order_date = max(recent_orders.mapped('date_order')).date()
            partner.days_since_last_purchase = (date.today() - last_order_date).days
        else:
            partner.days_since_last_purchase = 9999
```

**Business Logic**:
- `0-30 days`: Very recent customers (high recency)
- `31-90 days`: Recent customers (medium recency)
- `91-365 days`: Older customers (low recency)
- `>365 days`: Very old customers (very low recency)

### 2. Purchase Count (Frequency)

**Formula**:
```python
purchase_count = COUNT(sale_orders WHERE state IN ('sale', 'done') AND date_order >= twelve_months_ago)
```

**Implementation**:
```python
if recent_orders:
    partner.purchase_count = len(recent_orders)
else:
    partner.purchase_count = 0
```

**Business Logic**:
- `1 order`: New customer
- `2-3 orders`: Occasional customer
- `4-6 orders`: Regular customer
- `7+ orders`: Frequent customer

### 3. Total Spent (Monetary)

**Formula**:
```python
total_spent = SUM(sale_order.amount_total WHERE state IN ('sale', 'done') AND date_order >= twelve_months_ago)
```

**Implementation**:
```python
if recent_orders:
    partner.total_spent = sum(recent_orders.mapped('amount_total'))
else:
    partner.total_spent = 0
```

### 4. RFM Scoring Algorithm

Each RFM component is scored from 1-5 using quintile-based scoring:

**Recency Score (Inverse Scoring)**:
```python
def _compute_rfm_scores(self):
    # Get all customers with purchases
    customers = self.search([('customer_rank', '>', 0), ('days_since_last_purchase', '<', 9999)])
    
    if not customers:
        return
    
    # Calculate quintiles for recency (lower days = higher score)
    recency_values = customers.mapped('days_since_last_purchase')
    recency_quintiles = [
        sorted(recency_values)[int(len(recency_values) * 0.2)],
        sorted(recency_values)[int(len(recency_values) * 0.4)],
        sorted(recency_values)[int(len(recency_values) * 0.6)],
        sorted(recency_values)[int(len(recency_values) * 0.8)]
    ]
    
    for partner in customers:
        # Recency scoring (inverse - recent purchases get higher scores)
        if partner.days_since_last_purchase <= recency_quintiles[0]:
            partner.recency_score = 5
        elif partner.days_since_last_purchase <= recency_quintiles[1]:
            partner.recency_score = 4
        elif partner.days_since_last_purchase <= recency_quintiles[2]:
            partner.recency_score = 3
        elif partner.days_since_last_purchase <= recency_quintiles[3]:
            partner.recency_score = 2
        else:
            partner.recency_score = 1
```

**Frequency Score (Direct Scoring)**:
```python
# Calculate quintiles for frequency (higher count = higher score)
frequency_values = customers.mapped('purchase_count')
frequency_quintiles = [
    sorted(frequency_values)[int(len(frequency_values) * 0.2)],
    sorted(frequency_values)[int(len(frequency_values) * 0.4)],
    sorted(frequency_values)[int(len(frequency_values) * 0.6)],
    sorted(frequency_values)[int(len(frequency_values) * 0.8)]
]

for partner in customers:
    # Frequency scoring (direct - more purchases get higher scores)
    if partner.purchase_count >= frequency_quintiles[3]:
        partner.frequency_score = 5
    elif partner.purchase_count >= frequency_quintiles[2]:
        partner.frequency_score = 4
    elif partner.purchase_count >= frequency_quintiles[1]:
        partner.frequency_score = 3
    elif partner.purchase_count >= frequency_quintiles[0]:
        partner.frequency_score = 2
    else:
        partner.frequency_score = 1
```

**Monetary Score (Direct Scoring)**:
```python
# Calculate quintiles for monetary (higher spend = higher score)
monetary_values = customers.mapped('total_spent')
monetary_quintiles = [
    sorted(monetary_values)[int(len(monetary_values) * 0.2)],
    sorted(monetary_values)[int(len(monetary_values) * 0.4)],
    sorted(monetary_values)[int(len(monetary_values) * 0.6)],
    sorted(monetary_values)[int(len(monetary_values) * 0.8)]
]

for partner in customers:
    # Monetary scoring (direct - higher spend gets higher scores)
    if partner.total_spent >= monetary_quintiles[3]:
        partner.monetary_score = 5
    elif partner.total_spent >= monetary_quintiles[2]:
        partner.monetary_score = 4
    elif partner.total_spent >= monetary_quintiles[1]:
        partner.monetary_score = 3
    elif partner.total_spent >= monetary_quintiles[0]:
        partner.monetary_score = 2
    else:
        partner.monetary_score = 1
```

### 5. RFM Segment Classification

**Algorithm**:
```python
def _compute_rfm_segments(self):
    for partner in self:
        R, F, M = partner.recency_score, partner.frequency_score, partner.monetary_score
        
        # Champions: High RFM scores
        if R >= 4 and F >= 4 and M >= 4:
            partner.rfm_segment = 'champions'
        
        # Loyal Customers: High recency and frequency
        elif R >= 3 and F >= 4:
            partner.rfm_segment = 'loyal_customers'
        
        # Potential Loyalists: High recency and monetary
        elif R >= 4 and M >= 3:
            partner.rfm_segment = 'potential_loyalists'
        
        # New Customers: High recency, low frequency
        elif R >= 4 and F <= 2:
            partner.rfm_segment = 'new_customers'
        
        # Promising: Medium recency and frequency
        elif R >= 3 and F >= 2:
            partner.rfm_segment = 'promising'
        
        # Need Attention: Medium recency, low frequency
        elif R >= 2 and F <= 2:
            partner.rfm_segment = 'need_attention'
        
        # About to Sleep: Low recency, medium frequency
        elif R <= 2 and F >= 2:
            partner.rfm_segment = 'about_to_sleep'
        
        # At Risk: Low recency, high frequency/monetary
        elif R <= 2 and (F >= 4 or M >= 4):
            partner.rfm_segment = 'at_risk'
        
        # Cannot Lose Them: Low recency, high frequency and monetary
        elif R <= 2 and F >= 4 and M >= 4:
            partner.rfm_segment = 'cannot_lose_them'
        
        # Hibernating: Low RFM scores
        elif R <= 2 and F <= 2:
            partner.rfm_segment = 'hibernating'
        
        # Lost: Very low recency
        elif R == 1:
            partner.rfm_segment = 'lost'
        
        else:
            partner.rfm_segment = 'others'
```

**Overall RFM Score**:
```python
partner.rfm_score = (R + F + M) / 3 * 20  # Scale to 0-100
```

---

## Engagement Score Calculations

### Overview
Engagement scores measure customer interaction across multiple channels (email, website, WhatsApp) on a 0-100 scale.

### 1. Email Engagement Score

**Data Sources**:
- `mail.message` (email opens, clicks)
- `mail.tracking.event` (email interactions)
- Campaign participation records

**Formula**:
```python
def _compute_email_engagement(self):
    base_score = 0
    
    # Email responsiveness (40% weight)
    if partner.message_ids:
        recent_messages = partner.message_ids.filtered(
            lambda m: m.date >= (datetime.now() - timedelta(days=90))
        )
        if recent_messages:
            base_score += 40
    
    # Email campaigns participation (30% weight)
    # This would integrate with email marketing campaigns
    # For now, we simulate based on message activity
    if partner.email and partner.message_ids:
        message_count = len(partner.message_ids)
        if message_count >= 10:
            base_score += 30
        elif message_count >= 5:
            base_score += 20
        elif message_count >= 2:
            base_score += 10
    
    # Email communication frequency (30% weight)
    if partner.email:
        base_score += 30
    
    return min(base_score, 100)
```

### 2. Website Engagement Score

**Data Sources**:
- `sale_order` (purchase activity)
- Order frequency and recency
- Website behavior indicators

**Formula**:
```python
def _compute_website_engagement(self):
    base_score = 0
    
    # Recent purchase activity (50% weight)
    if partner.days_since_last_purchase <= 30:
        base_score += 50
    elif partner.days_since_last_purchase <= 90:
        base_score += 30
    elif partner.days_since_last_purchase <= 180:
        base_score += 15
    
    # Purchase frequency (30% weight)
    if partner.purchase_count >= 5:
        base_score += 30
    elif partner.purchase_count >= 3:
        base_score += 20
    elif partner.purchase_count >= 1:
        base_score += 10
    
    # Order value trends (20% weight)
    if partner.total_spent >= 1000:
        base_score += 20
    elif partner.total_spent >= 500:
        base_score += 15
    elif partner.total_spent >= 100:
        base_score += 10
    
    return min(base_score, 100)
```

### 3. WhatsApp Engagement Score

**Data Sources**:
- `wa_marketing_automation.whatsapp_api_log` (campaign responses)
- Message delivery and response rates
- Campaign participation

**Formula**:
```python
def _compute_whatsapp_engagement(self):
    base_score = 0
    
    # WhatsApp campaigns participation (60% weight)
    # This would be calculated from campaign logs
    if partner.mobile:
        # Check if customer has participated in WhatsApp campaigns
        # For now, we simulate based on mobile presence and message activity
        if partner.message_ids:
            base_score += 40
        base_score += 20  # Base score for having mobile number
    
    # Response rate to WhatsApp messages (40% weight)
    # This would be calculated from API logs
    # For now, we simulate based on overall engagement
    if partner.message_ids and partner.mobile:
        response_rate = min(len(partner.message_ids) * 5, 40)
        base_score += response_rate
    
    return min(base_score, 100)
```

### 4. Overall Engagement Score

**Formula**:
```python
def _compute_overall_engagement(self):
    scores = []
    weights = []
    
    # Email engagement (weight: 1)
    if partner.email:
        scores.append(partner.email_engagement_score)
        weights.append(1)
    
    # Website engagement (weight: 1)
    if partner.sale_order_ids:
        scores.append(partner.website_engagement_score)
        weights.append(1)
    
    # WhatsApp engagement (weight: 1)
    if partner.mobile:
        scores.append(partner.whatsapp_engagement_score)
        weights.append(1)
    
    # Calculate weighted average
    if scores:
        partner.overall_engagement_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
    else:
        partner.overall_engagement_score = 0
```

### 5. Engagement Level Classification

**Algorithm**:
```python
def _compute_engagement_level(self):
    score = partner.overall_engagement_score
    
    if score >= 80:
        partner.engagement_level = 'very_high'
    elif score >= 60:
        partner.engagement_level = 'high'
    elif score >= 40:
        partner.engagement_level = 'medium'
    elif score >= 20:
        partner.engagement_level = 'low'
    else:
        partner.engagement_level = 'very_low'
```

---

## Churn Prediction Algorithm

### Overview
Churn prediction calculates the probability (0-100) that a customer will churn in the next 90 days using a weighted multi-factor model.

### Churn Risk Score Calculation

**Formula**:
```python
def _compute_churn_prediction(self):
    # Multi-factor churn prediction model
    churn_score = 0
    
    # Factor 1: RFM Segment (40% weight)
    rfm_risk = {
        'lost': 90,
        'hibernating': 80,
        'at_risk': 70,
        'cannot_lose_them': 60,
        'about_to_sleep': 50,
        'need_attention': 40,
        'promising': 20,
        'potential_loyalists': 15,
        'loyal_customers': 10,
        'new_customers': 25,
        'champions': 5,
        'others': 30
    }
    churn_score += rfm_risk.get(partner.rfm_segment, 30) * 0.4
    
    # Factor 2: Recency Factor (30% weight)
    if partner.days_since_last_purchase <= 30:
        recency_risk = 10
    elif partner.days_since_last_purchase <= 90:
        recency_risk = 25
    elif partner.days_since_last_purchase <= 180:
        recency_risk = 50
    elif partner.days_since_last_purchase <= 365:
        recency_risk = 75
    else:
        recency_risk = 95
    
    churn_score += recency_risk * 0.3
    
    # Factor 3: Engagement Factor (20% weight)
    engagement_risk = 100 - partner.overall_engagement_score
    churn_score += engagement_risk * 0.2
    
    # Factor 4: Journey Stage Factor (10% weight)
    journey_risk = {
        'advocacy': 5,
        'loyalty': 15,
        'purchase': 25,
        'consideration': 35,
        'awareness': 45,
        'dormant': 85
    }
    churn_score += journey_risk.get(partner.customer_journey_stage, 50) * 0.1
    
    partner.churn_risk_score = min(churn_score, 100)
```

### Churn Risk Level Classification

**Algorithm**:
```python
def _compute_churn_risk_level(self):
    score = partner.churn_risk_score
    
    if score >= 81:
        partner.churn_risk_level = 'very_high'
    elif score >= 61:
        partner.churn_risk_level = 'high'
    elif score >= 41:
        partner.churn_risk_level = 'medium'
    elif score >= 21:
        partner.churn_risk_level = 'low'
    else:
        partner.churn_risk_level = 'very_low'
```

---

## Customer Journey Stage Logic

### Overview
Customer journey stages automatically classify customers based on their purchase behavior and engagement patterns.

### Stage Classification Algorithm

**Implementation**:
```python
def _compute_journey_stage(self):
    for partner in self:
        if not partner.is_company:
            # B2C Customer Journey
            if partner.customer_rank == 0:
                # Never purchased
                partner.customer_journey_stage = 'awareness'
            elif partner.sale_order_count == 1:
                # First-time customer
                partner.customer_journey_stage = 'consideration'
            elif partner.rfm_segment in ('champions', 'loyal_customers'):
                # High-value loyal customers
                partner.customer_journey_stage = 'advocacy'
            elif partner.days_since_last_purchase <= 90:
                # Active customers
                partner.customer_journey_stage = 'purchase'
            elif partner.days_since_last_purchase <= 180:
                # Recent customers building loyalty
                partner.customer_journey_stage = 'loyalty'
            else:
                # Dormant customers
                partner.customer_journey_stage = 'dormant'
        else:
            # B2B Customer Journey
            if partner.customer_rank == 0:
                partner.customer_journey_stage = 'awareness'
            elif partner.sale_order_count >= 5:
                partner.customer_journey_stage = 'loyalty'
            else:
                partner.customer_journey_stage = 'purchase'
```

### Journey Stage Definitions

1. **Awareness** (0 orders): Potential customers, never purchased
2. **Consideration** (1 order): First-time customers, evaluating
3. **Purchase** (2+ orders, recent): Active customers, regular purchases
4. **Loyalty** (2+ orders, building relationship): Established customers
5. **Advocacy** (Champions/Loyal RFM): Brand advocates, high-value customers
6. **Dormant** (>180 days): Inactive customers, churn risk

---

## Multi-Channel Behavior Scoring

### Overview
Multi-channel behavior tracks customer touchpoints across email, WhatsApp, phone, and website channels.

### Channel Detection Algorithm

**Implementation**:
```python
def _compute_multichannel_behavior(self):
    for partner in self:
        # Count available channels
        channels = []
        if partner.email:
            channels.append('email')
        if partner.mobile:
            channels.append('whatsapp')
        if partner.phone:
            channels.append('phone')
        if partner.sale_order_ids:
            channels.append('website')
        
        # Count touchpoints
        partner.multichannel_touchpoints = len(channels)
        
        # Determine preferred channel based on activity
        if partner.sale_order_ids and len(partner.sale_order_ids) >= 3:
            partner.preferred_channel = 'website'
        elif partner.mobile and partner.message_ids:
            partner.preferred_channel = 'whatsapp'
        elif partner.email:
            partner.preferred_channel = 'email'
        elif partner.phone:
            partner.preferred_channel = 'phone'
        else:
            partner.preferred_channel = 'mixed'
```

### Consistency Score Calculation

**Formula**:
```python
def _compute_consistency_score(self):
    touchpoints = partner.multichannel_touchpoints
    
    if touchpoints >= 3:
        partner.multichannel_consistency_score = 85.0
    elif touchpoints == 2:
        partner.multichannel_consistency_score = 60.0
    elif touchpoints == 1:
        partner.multichannel_consistency_score = 30.0
    else:
        partner.multichannel_consistency_score = 0.0
```

---

## Values-Driven Propensity Calculations

### Overview
Values-driven propensity analyzes customer preferences for sustainability, premium products, and social responsibility based on purchase history.

### 1. Sustainability Preference Score

**Algorithm**:
```python
def _compute_sustainability_preference(self):
    if not partner.sale_order_ids:
        partner.sustainability_preference_score = 0
        return
    
    orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
    total_products = 0
    sustainable_products = 0
    
    # Keywords indicating sustainable products
    sustainability_keywords = [
        'eco', 'organic', 'green', 'sustainable', 'bamboo', 'recycled',
        'biodegradable', 'renewable', 'fair trade', 'carbon neutral'
    ]
    
    for order in orders:
        for line in order.order_line:
            total_products += 1
            product_name = line.product_id.name.lower()
            
            if any(keyword in product_name for keyword in sustainability_keywords):
                sustainable_products += 1
    
    if total_products > 0:
        preference_ratio = sustainable_products / total_products
        partner.sustainability_preference_score = preference_ratio * 100
    else:
        partner.sustainability_preference_score = 0
```

### 2. Premium Product Propensity

**Algorithm**:
```python
def _compute_premium_propensity(self):
    if not partner.sale_order_ids:
        partner.premium_product_propensity = 0
        return
    
    orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
    
    # Calculate average order value
    if orders:
        avg_order_value = sum(orders.mapped('amount_total')) / len(orders)
        
        # Premium propensity based on spending patterns
        if avg_order_value >= 500:
            partner.premium_product_propensity = 90
        elif avg_order_value >= 300:
            partner.premium_product_propensity = 70
        elif avg_order_value >= 200:
            partner.premium_product_propensity = 50
        elif avg_order_value >= 100:
            partner.premium_product_propensity = 30
        else:
            partner.premium_product_propensity = 10
    else:
        partner.premium_product_propensity = 0
```

### 3. Social Responsibility Score

**Algorithm**:
```python
def _compute_social_responsibility_score(self):
    if not partner.sale_order_ids:
        partner.social_responsibility_score = 0
        return
    
    orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
    total_products = 0
    social_products = 0
    
    # Keywords indicating socially responsible products
    social_keywords = [
        'charity', 'donation', 'social', 'community', 'ethical',
        'fair trade', 'local', 'artisan', 'support', 'cause'
    ]
    
    for order in orders:
        for line in order.order_line:
            total_products += 1
            product_name = line.product_id.name.lower()
            
            if any(keyword in product_name for keyword in social_keywords):
                social_products += 1
    
    if total_products > 0:
        responsibility_ratio = social_products / total_products
        partner.social_responsibility_score = responsibility_ratio * 100
    else:
        partner.social_responsibility_score = 0
```

---

## Social Commerce Metrics

### Overview
Social commerce metrics track customer acquisition and behavior from social media platforms using UTM parameters and source tracking.

### 1. Social Media Source Detection

**Algorithm**:
```python
def _compute_social_commerce_metrics(self):
    if not partner.sale_order_ids:
        partner.social_media_source = 'none'
        return
    
    orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
    social_sources = []
    
    # Check for social media sources in UTM data
    for order in orders:
        if order.source_id:
            source_name = order.source_id.name.lower()
            
            # Platform detection
            if 'facebook' in source_name or 'fb' in source_name:
                social_sources.append('facebook')
            elif 'instagram' in source_name or 'ig' in source_name:
                social_sources.append('instagram')
            elif 'twitter' in source_name:
                social_sources.append('twitter')
            elif 'linkedin' in source_name:
                social_sources.append('linkedin')
            elif 'tiktok' in source_name:
                social_sources.append('tiktok')
            elif 'youtube' in source_name:
                social_sources.append('youtube')
            elif any(social in source_name for social in ['social', 'share', 'referral']):
                social_sources.append('other')
    
    # Determine primary social media source
    if social_sources:
        from collections import Counter
        most_common = Counter(social_sources).most_common(1)
        partner.social_media_source = most_common[0][0]
    else:
        partner.social_media_source = 'none'
```

### 2. Social Engagement Score

**Formula**:
```python
def _compute_social_engagement_score(self):
    base_score = 0
    
    # Social media source presence (50% weight)
    if partner.social_media_source != 'none':
        base_score += 50
    
    # Social referral activity (30% weight)
    if partner.social_referral_count >= 5:
        base_score += 30
    elif partner.social_referral_count >= 2:
        base_score += 20
    elif partner.social_referral_count >= 1:
        base_score += 10
    
    # Social conversion activity (20% weight)
    if partner.social_conversion_rate >= 50:
        base_score += 20
    elif partner.social_conversion_rate >= 25:
        base_score += 15
    elif partner.social_conversion_rate >= 10:
        base_score += 10
    
    partner.social_engagement_score = base_score
```

### 3. Social Conversion Rate

**Formula**:
```python
def _compute_social_conversion_rate(self):
    if not partner.sale_order_ids:
        partner.social_conversion_rate = 0
        return
    
    total_orders = len(partner.sale_order_ids)
    social_orders = partner.social_referral_count
    
    if total_orders > 0:
        conversion_rate = (social_orders / total_orders) * 100
        partner.social_conversion_rate = min(conversion_rate, 100)
    else:
        partner.social_conversion_rate = 0
```

---

## BNPL & Mobile Commerce Calculations

### Overview
BNPL (Buy Now Pay Later) and mobile commerce metrics track modern payment preferences and device usage patterns.

### 1. BNPL Usage Detection

**Algorithm**:
```python
def _compute_bnpl_behavior(self):
    if not partner.sale_order_ids:
        partner.bnpl_usage_frequency = 'never'
        return
    
    orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
    bnpl_orders = 0
    
    # BNPL keywords in payment terms
    bnpl_keywords = [
        'installment', 'split', 'bnpl', 'klarna', 'afterpay', 
        'sezzle', 'affirm', 'pay later', 'monthly'
    ]
    
    for order in orders:
        if order.payment_term_id:
            payment_term_name = order.payment_term_id.name.lower()
            if any(keyword in payment_term_name for keyword in bnpl_keywords):
                bnpl_orders += 1
    
    # Determine BNPL usage frequency
    if bnpl_orders == 0:
        partner.bnpl_usage_frequency = 'never'
    elif bnpl_orders <= 2:
        partner.bnpl_usage_frequency = 'rarely'
    elif bnpl_orders <= 5:
        partner.bnpl_usage_frequency = 'sometimes'
    elif bnpl_orders <= 10:
        partner.bnpl_usage_frequency = 'frequently'
    else:
        partner.bnpl_usage_frequency = 'always'
```

### 2. BNPL Preference Score

**Formula**:
```python
def _compute_bnpl_preference_score(self):
    if len(orders) > 0:
        bnpl_preference = (bnpl_orders / len(orders)) * 100
        partner.bnpl_preference_score = min(bnpl_preference, 100)
    else:
        partner.bnpl_preference_score = 0
```

### 3. Mobile Commerce Analysis

**Algorithm** (Simplified - in production would use web analytics):
```python
def _compute_mobile_commerce_behavior(self):
    if not partner.sale_order_ids:
        partner.mobile_device_preference = 'unknown'
        return
    
    orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done'))
    mobile_orders = 0
    
    # Simulate mobile behavior based on order characteristics
    # In production, this would use actual device tracking data
    for order in orders:
        # Heuristic: smaller orders, mobile numbers, specific times
        if (order.amount_total < 200 and partner.mobile and 
            order.create_date.hour in [7, 8, 12, 13, 17, 18, 19, 20, 21]):
            mobile_orders += 1
    
    total_orders = len(orders)
    if total_orders > 0:
        mobile_ratio = mobile_orders / total_orders
        
        if mobile_ratio >= 0.7:
            partner.mobile_device_preference = 'smartphone'
        elif mobile_ratio >= 0.4:
            partner.mobile_device_preference = 'mixed'
        elif mobile_ratio >= 0.1:
            partner.mobile_device_preference = 'tablet'
        else:
            partner.mobile_device_preference = 'desktop'
    else:
        partner.mobile_device_preference = 'unknown'
```

---

## Cohort Analysis SQL Logic

### Overview
Cohort analysis tracks customer behavior over time using complex SQL queries to group customers by acquisition period.

### Core CTE Structure

**SQL Implementation**:
```sql
WITH cohort_data AS (
    -- Get customer acquisition dates (first order date)
    SELECT 
        rp.id as partner_id,
        DATE_TRUNC('month', MIN(so.date_order)) as cohort_period,
        TO_CHAR(DATE_TRUNC('month', MIN(so.date_order)), 'YYYY-MM') as cohort_period_month
    FROM res_partner rp
    LEFT JOIN sale_order so ON rp.id = so.partner_id AND so.state IN ('sale', 'done')
    WHERE rp.is_company = false 
    AND rp.active = true
    AND rp.customer_rank > 0
    GROUP BY rp.id
),
period_data AS (
    -- Generate periods (months) for analysis
    SELECT 
        cohort_period,
        cohort_period_month,
        generate_series(0, 23) as period_number  -- 24 months of data
    FROM (
        SELECT DISTINCT cohort_period, cohort_period_month 
        FROM cohort_data 
        WHERE cohort_period IS NOT NULL
    ) cohorts
),
customer_activity AS (
    -- Calculate customer activity for each period
    SELECT 
        cd.partner_id,
        cd.cohort_period,
        cd.cohort_period_month,
        pd.period_number,
        cd.cohort_period + (pd.period_number || ' months')::interval as analysis_period,
        
        -- Check if customer was active in this period
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM sale_order so2 
                WHERE so2.partner_id = cd.partner_id 
                AND so2.state IN ('sale', 'done')
                AND DATE_TRUNC('month', so2.date_order) = cd.cohort_period + (pd.period_number || ' months')::interval
            ) THEN 1 
            ELSE 0 
        END as is_active,
        
        -- Calculate revenue for this period
        COALESCE((
            SELECT SUM(so3.amount_total) 
            FROM sale_order so3 
            WHERE so3.partner_id = cd.partner_id 
            AND so3.state IN ('sale', 'done')
            AND DATE_TRUNC('month', so3.date_order) = cd.cohort_period + (pd.period_number || ' months')::interval
        ), 0) as period_revenue
        
    FROM cohort_data cd
    JOIN period_data pd ON cd.cohort_period = pd.cohort_period
    WHERE cd.cohort_period + (pd.period_number || ' months')::interval <= DATE_TRUNC('month', CURRENT_DATE)
)
```

### Key Metrics Calculations

**Retention Rate**:
```sql
-- Retention rate calculation
ROUND(
    (COUNT(CASE WHEN is_active = 1 THEN 1 END) * 100.0 / 
    NULLIF((SELECT COUNT(DISTINCT partner_id) FROM cohort_data cd2 WHERE cd2.cohort_period = ca.cohort_period), 0))::numeric,
    2
) as retention_rate
```

**Customer Lifetime Value**:
```sql
-- CLV calculation
ROUND(
    (AVG(cumulative_revenue) / NULLIF(
        (SELECT COUNT(DISTINCT partner_id) FROM cohort_data cd4 WHERE cd4.cohort_period = ca.cohort_period), 
        0
    ))::numeric,
    2
) as customer_lifetime_value
```

**Average Revenue Per Customer**:
```sql
-- ARPC calculation
ROUND(
    (SUM(period_revenue) / NULLIF(COUNT(CASE WHEN is_active = 1 THEN 1 END), 0))::numeric,
    2
) as average_revenue_per_customer
```

---

## Customer Demographics Calculations

### Overview
Customer demographics analysis provides age-based insights and purchase patterns.

### Age Calculation

**Formula**:
```python
def _compute_age(self):
    for partner in self:
        if partner.date_of_birth:
            today = date.today()
            born = partner.date_of_birth
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            partner.age = age
        else:
            partner.age = 0
```

### Age Display Format

**Implementation**:
```python
def _compute_age_display(self):
    for partner in self:
        if partner.age > 0:
            partner.age_display = f"{partner.age} years old"
        else:
            partner.age_display = "Age not set"
```

### Demographics SQL View

**SQL Implementation**:
```sql
CREATE OR REPLACE VIEW wa_marketing_automation_customer_demographics_report AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY rp.id) as id,
        rp.id as partner_id,
        rp.name as customer_name,
        rp.age,
        
        -- Age group classification
        CASE 
            WHEN rp.age < 18 THEN 'Under 18'
            WHEN rp.age BETWEEN 18 AND 25 THEN '18-25'
            WHEN rp.age BETWEEN 26 AND 35 THEN '26-35'
            WHEN rp.age BETWEEN 36 AND 45 THEN '36-45'
            WHEN rp.age BETWEEN 46 AND 55 THEN '46-55'
            WHEN rp.age BETWEEN 56 AND 65 THEN '56-65'
            WHEN rp.age > 65 THEN 'Over 65'
            ELSE 'Unknown'
        END as age_group,
        
        -- Purchase metrics
        COALESCE(rp.total_spent, 0) as total_spent,
        COALESCE(rp.purchase_count, 0) as purchase_count,
        COALESCE(rp.days_since_last_purchase, 9999) as days_since_last_purchase,
        
        -- Average order value
        CASE 
            WHEN rp.purchase_count > 0 THEN ROUND((rp.total_spent / rp.purchase_count)::numeric, 2)
            ELSE 0
        END as average_order_value,
        
        -- RFM Analysis
        rp.rfm_segment,
        rp.rfm_score,
        
        -- Engagement metrics
        rp.overall_engagement_score,
        rp.engagement_level
        
    FROM res_partner rp
    WHERE rp.is_company = false 
    AND rp.active = true
    AND rp.customer_rank > 0
    AND rp.age > 0
)
```

---

## Performance Considerations

### Database Optimization

1. **Indexes**: All computed fields are marked with `store=True` for database indexing
2. **Batch Processing**: Computations are performed in batches to avoid memory issues
3. **Selective Updates**: Only recalculate when dependencies change using `@api.depends`

### Computation Efficiency

**Defensive Programming**:
```python
# Always check for required dependencies
if not hasattr(partner, 'sale_order_ids'):
    partner.field_name = default_value
    continue
```

**Safe Calculations**:
```python
# Avoid division by zero
if total_orders > 0:
    rate = (success_orders / total_orders) * 100
else:
    rate = 0
```

### Memory Management

**Large Dataset Handling**:
```python
# Process in chunks for large datasets
def _compute_metric_batch(self):
    chunk_size = 1000
    for i in range(0, len(self), chunk_size):
        chunk = self[i:i + chunk_size]
        # Process chunk
```

---

## Validation and Testing

### Data Quality Checks

1. **Range Validation**: All scores are clamped to 0-100 range
2. **Null Safety**: Default values for missing data
3. **Type Validation**: Proper data type conversion
4. **Business Logic Validation**: Ensures calculations make business sense

### Testing Scenarios

**Test Cases**:
```python
# Test new customer (no orders)
# Test single order customer
# Test high-value customer
# Test dormant customer
# Test customer with missing data
```

### Debugging Tools

**Logging**:
```python
import logging
_logger = logging.getLogger(__name__)

def _compute_metric(self):
    _logger.info(f"Computing metric for {len(self)} partners")
    # Computation logic
```

---

## Conclusion

This comprehensive reference provides the complete technical foundation for understanding, maintaining, and extending the analytics capabilities of the WhatsApp Marketing Automation module. Each calculation is designed to provide actionable business insights while maintaining computational efficiency and data accuracy.

### Key Principles

1. **Transparency**: All calculations are fully documented and explainable
2. **Robustness**: Defensive programming prevents errors with missing data
3. **Scalability**: Efficient algorithms handle large customer datasets
4. **Accuracy**: Precise formulas ensure reliable business insights
5. **Maintainability**: Clear code structure enables easy updates and extensions

### Future Enhancements

The modular design allows for easy addition of new metrics and refinement of existing calculations based on business requirements and customer feedback.