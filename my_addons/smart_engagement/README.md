# Smart Engagement for Odoo

A comprehensive smart engagement marketing automation solution for Odoo that enables businesses to create, manage, and execute targeted marketing campaigns through WhatsApp API and multi-channel engagement.

## 🎯 Overview

This module provides a complete smart engagement platform with advanced features for customer segmentation, personalized messaging, campaign scheduling, and performance analytics. It seamlessly integrates with Odoo's CRM and product catalog to deliver targeted, data-driven marketing campaigns across multiple channels including WhatsApp automation.

## ✨ Key Features

### Core Marketing Automation
- **🎯 Advanced Customer Segmentation**: Manual and rule-based customer targeting with 100+ predefined segments
- **📅 Flexible Campaign Scheduling**: Immediate, scheduled, and recurring campaigns
- **📝 Dynamic Message Templates**: Personalized messages with product recommendations
- **🛍️ Product Integration**: Smart product recommendations with custom formatting
- **📊 Analytics & Monitoring**: Real-time performance tracking and detailed logs
- **🔗 CRM Integration**: Automatic lead generation and opportunity management
- **⚡ Automation**: Scheduled actions and workflow automation
- **🛡️ Security**: Secure API integration with comprehensive validation

### Advanced Analytics & Intelligence (New!)
- **🧠 Engagement Analytics**: Multi-channel engagement scoring across email, WhatsApp, and website
- **🔮 Churn Prediction**: AI-powered 90-day churn probability with risk assessment
- **📈 Customer Journey Mapping**: Automatic lifecycle stage identification (Awareness → Advocacy)
- **🎯 RFM Analysis**: Recency, Frequency, Monetary segmentation with automated scoring
- **📊 Cohort Analysis**: Time-based customer behavior tracking with retention insights
- **🌱 Values-Driven Analytics**: Sustainability, premium, and social responsibility propensity
- **📱 Social Commerce Integration**: Social media source tracking and conversion optimization
- **💳 BNPL & Mobile Commerce**: Buy Now Pay Later and mobile behavior analysis
- **🔄 Multi-Channel Behavior**: Touchpoint tracking and channel preference identification

## 🚀 Quick Start

Get started in just 5 minutes:

1. **Configure WhatsApp API** - Set up your API endpoint and access token
2. **Create Customer Segment** - Define your target audience
3. **Build Campaign** - Create message template and select products
4. **Test & Launch** - Preview messages and start your campaign

[📖 **Follow the Quick Start Guide →**](docs/QUICK_START_GUIDE.md)

## 📚 Documentation

### 📋 User Guides

- [**Quick Start Guide**](docs/QUICK_START_GUIDE.md) - Get started in 5 minutes
- [**Advanced Analytics User Guide**](docs/ADVANCED_ANALYTICS_USER_GUIDE.md) - Complete guide to all analytics features
- [**Customer Demographics Reports Guide**](docs/CUSTOMER_DEMOGRAPHICS_REPORTS_USER_GUIDE.md) - Comprehensive guide to demographic analysis and reporting
- [**Segmentation from Reports Guide**](docs/CUSTOMER_SEGMENTATION_FROM_REPORTS_GUIDE.md) - How to create segments using Odoo reports
- [**Segmentation Quick Reference**](docs/SEGMENTATION_QUICK_REFERENCE.md) - Copy-paste ready segment rules

### 🛠️ Technical Documentation

- [**Templating Examples**](docs/TEMPLATING_EXAMPLES.md) - Advanced message template examples
- [**Utils Guide**](docs/UTILS_GUIDE.md) - Technical implementation and utility functions

### 📊 Advanced Analytics & Reports

- **Engagement Analytics** - Multi-channel engagement scoring and optimization
- **Churn Prediction** - AI-powered customer retention insights
- **Customer Journey Mapping** - Lifecycle stage tracking and optimization
- **RFM Analysis** - Recency, Frequency, Monetary value segmentation
- **Cohort Analysis** - Time-based customer behavior and retention tracking
- **Values-Driven Analytics** - Sustainability, premium, and social responsibility insights
- **Social Commerce Analytics** - Social media source tracking and conversion optimization
- **BNPL & Mobile Commerce** - Modern payment and device behavior analysis
- **Customer Demographics Analysis** - Age-based insights and purchase patterns
- **Integration with Odoo Reports** - Leverage sales, invoice, and CRM data

### 📊 Visual Guides

The documentation includes interactive diagrams showing:

- Campaign workflow and execution flow
- System architecture and component relationships
- Feature overview and capabilities map
- Scheduling and automation processes

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────┐
│                Campaign Management                   │
├─────────────────────────────────────────────────────┤
│  Customer Segmentation  │  Product Recommendations  │
├─────────────────────────────────────────────────────┤
│              Message Templates                      │
├─────────────────────────────────────────────────────┤
│              Scheduling Engine                      │
├─────────────────────────────────────────────────────┤
│            WhatsApp API Integration                 │
├─────────────────────────────────────────────────────┤
│           Advanced Analytics Engine                 │
├─────────────────────────────────────────────────────┤
│ Engagement │ Churn Pred │ Journey │ RFM │ Cohort    │
├─────────────────────────────────────────────────────┤
│ Social Commerce │ BNPL Analytics │ Values-Driven   │
├─────────────────────────────────────────────────────┤
│              Analytics & Logging                   │
└─────────────────────────────────────────────────────┘
```

### Key Models

- **Campaign**: Core campaign management and execution
- **Customer Segmentation**: Target audience definition and filtering
- **Configuration**: WhatsApp API setup and management
- **API Logs**: Performance monitoring and error tracking
- **Customer Demographics Report**: Age-based analytics and insights
- **Cohort Analysis Report**: Time-based customer behavior tracking
- **Extended Partner Model**: 25+ new analytics fields for comprehensive customer intelligence

## 🔧 Installation

### Prerequisites

- Odoo 18.0 or later
- WhatsApp API endpoint
- CRM module (for lead generation)

### Installation Steps

1. **Install the Module**

   ```bash
   # Place the module in your addons directory
   cp -r smart_engagement /path/to/odoo/addons/

   # Install in Odoo
   odoo-bin -d your_database -i smart_engagement
   ```

2. **Configure Dependencies**

   - Ensure CRM module is installed
   - Configure WhatsApp API
   - Set up customer data and product catalog

3. **Initial Setup**
   - Navigate to Smart Engagement → Configuration
   - Enter your API details and test connection
   - Create your first customer segment (required for campaigns)
   - Launch your first campaign

## 🎛️ Configuration

### WhatsApp API Setup

```
Base URL: https://your-whatsapp-api.com
Access Token: your_access_token_here
Send Path: /send-message
Health Check Path: /health
```

### Required API Endpoints

- `GET /health` - Connection testing
- `POST /send-message` - Message delivery

## 📝 Message Templates

### Basic Template

```
Hi {customer_name}!

We have new products for you:
{products}

Best regards,
Your Team
```

### Advanced Template

```
Hello {customer_name}!

Special offers just for you:

{products:product_item_format(🛍️ {product_name}
💰 Price: {product_price}
📦 Code: {product_code}

)}

Order now by replying to this message!
```

## 🎯 Use Cases

### E-commerce

- Product promotions and recommendations
- Cart abandonment recovery
- New product announcements
- Seasonal marketing campaigns
- Age-based product targeting
- RFM-based customer loyalty programs

### Service Businesses

- Appointment reminders
- Service promotions
- Customer feedback collection
- Event notifications
- Birthday and anniversary campaigns
- Demographic-specific service offerings

### B2B Marketing

- Lead nurturing sequences
- Customer onboarding
- Account management touchpoints
- Product update notifications
- Company size-based segmentation
- Industry-specific campaigns

## 📊 Customer Insights & Segmentation

### Advanced Analytics

Our module now includes comprehensive customer analytics:

- **Demographic Analysis**: Age distribution, purchase patterns by age group
- **RFM Segmentation**: Identify Champions, At-Risk, and New customers
- **Lifetime Value**: Track CLV by demographics and segments
- **Purchase Patterns**: Frequency, recency, and monetary analysis

### Smart Segmentation

Create targeted segments using data from:

- **Odoo Reports**: Sales, invoices, CRM pipeline
- **Custom Demographics**: Age, location, behavior
- **Combined Criteria**: Mix demographic and behavioral data

Example segments:
- High-value millennials (age 28-43 with spend > $5000)
- Birthday month customers with recent purchases
- At-risk champions (high value but declining activity)
- Geographic campaigns by state or city

## 📊 Analytics & Monitoring

### Key Metrics

- **Messages Sent**: Total messages delivered
- **Success Rate**: Delivery success percentage
- **Error Rate**: Failed delivery percentage
- **Execution Time**: Average processing time

### Monitoring Tools

- Real-time campaign dashboard
- Detailed API logs
- Error tracking and alerting
- Performance optimization insights

## 🛡️ Security & Compliance

### Data Protection

- Secure API token management
- Customer data privacy protection
- Audit trail and logging
- GDPR compliance features

### WhatsApp Compliance

- Message policy compliance
- Rate limiting adherence
- Opt-out management
- Content validation

## 🔍 Troubleshooting

### Common Issues

1. **Connection Failed** - Check API endpoint and token
2. **Messages Not Sending** - Verify phone numbers and API logs
3. **Template Errors** - Use preview function and validate syntax
4. **Performance Issues** - Monitor API logs and optimize segments

### Debug Mode

Enable detailed logging:

```
Settings → Technical → Logging → Add logger for 'smart_engagement'
```

## 🤝 Support

### Getting Help

- Review the comprehensive documentation
- Check API logs for detailed error information
- Test with small segments first
- Use the preview and test functions

### Resources

- [Quick Start](docs/QUICK_START_GUIDE.md) - Fast setup guide
- [Advanced Analytics](docs/ADVANCED_ANALYTICS_USER_GUIDE.md) - Complete analytics guide
- [Customer Demographics Reports](docs/CUSTOMER_DEMOGRAPHICS_REPORTS_USER_GUIDE.md) - Demographics analysis
- [Segmentation Guide](docs/CUSTOMER_SEGMENTATION_FROM_REPORTS_GUIDE.md) - Segment creation
- [Segmentation Quick Reference](docs/SEGMENTATION_QUICK_REFERENCE.md) - Copy-paste segments
- [Templating Examples](docs/TEMPLATING_EXAMPLES.md) - Template examples

## 📄 License

This module is licensed under LGPL-3. See the LICENSE file for details.

## 👨‍💻 Author

**Antony Gunawan**

- Smart Engagement Automation Expert
- Odoo Integration Specialist

---

## 🚀 Get Started Now!

Ready to transform your customer engagement with advanced WhatsApp marketing automation?

1. [**Quick Start Guide**](docs/QUICK_START_GUIDE.md) - Get running in 5 minutes
2. [**Advanced Analytics Guide**](docs/ADVANCED_ANALYTICS_USER_GUIDE.md) - Unlock powerful customer insights
3. [**Customer Demographics Reports**](docs/CUSTOMER_DEMOGRAPHICS_REPORTS_USER_GUIDE.md) - Analyze your customer base
4. [**Create Smart Segments**](docs/CUSTOMER_SEGMENTATION_FROM_REPORTS_GUIDE.md) - Target the right customers

_Transform your customer communication with intelligent WhatsApp marketing automation powered by advanced analytics!_
