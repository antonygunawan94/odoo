# Odoo 18.0 Development Project - Operations Guide

## Project Overview
This is an Odoo 18.0 ERP system with custom modules and UI theme enhancements. The project includes WhatsApp marketing automation capabilities and modern UI themes.

## Important Odoo 18.0 Changes
- **Tree View → List View**: In Odoo 18.0, the `<tree>` XML tag has been renamed to `<list>` in view definitions
- **View Mode**: Use `view_mode="list,form"` instead of `view_mode="tree,form"`
- **View Names**: Update view names from `*.tree.*` to `*.list.*` (e.g., `res.partner.tree.dob` → `res.partner.list.dob`)
- **View IDs**: Base view IDs remain unchanged for backward compatibility (e.g., `base.view_partner_tree` still exists)
- **Migration Note**: All custom modules migrating from Odoo 17 to 18 need to update tree views to list views

## Project Structure
```
odoo/
├── addons/                   # Core Odoo modules (1000+ modules)
├── my_addons/               # Custom modules directory
│   ├── muk_web_theme/       # Modern backend theme
│   ├── muk_web_*           # UI enhancement modules
│   └── wa_marketing_automation/  # WhatsApp marketing module
├── odoo/                    # Core Odoo framework
├── venv/                    # Python virtual environment
├── .odoorc                  # Odoo configuration file
├── requirements.txt         # Python dependencies
├── Makefile                 # Development automation
├── HOW_TO_CREATE_MODULE.MD  # Module creation guide
└── odoo-bin                 # Odoo executable
```

## Development Environment Setup

### Prerequisites
- Python 3.10+ (configured in setup.py:68)
- PostgreSQL database server
- Virtual environment activated

### Configuration
- **Database**: odoo/odoo (configured in .odoorc:4)
- **Database User**: odoo (configured in .odoorc:2)
- **Addons Path**: addons,my_addons,odoo/addons (configured in .odoorc:5)
- **Web Port**: Default 8069

### Virtual Environment
```bash
# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
```

## Development Workflow

### Important Note for Claude Code Assistant
⚠️ **IMPORTANT**: When testing changes, DO NOT run `make run-dev` or `python odoo-bin` commands directly as they will timeout after 2 minutes. Instead, notify the user to test the changes manually. The assistant should focus on:
1. Making code changes
2. Running module updates (`make run-update`)
3. Asking the user to test the running server at `http://localhost:8070`

### Starting Development Server
```bash
# Quick start (recommended for development)
make run-dev

# Production mode
make run

# With specific configuration
python odoo-bin --config=.odoorc --dev=all
```

### Database Operations
```bash
# Initialize database
make run-init

# Update all modules
make run-update

# Create new database
make db-create
```

### Development Tools
```bash
# Install dependencies
make install

# Install development tools
make install-dev

# Access Odoo shell
make run-shell

# Run tests
make test

# Code formatting and linting
make format
make lint

# Clean cache files
make clean
```

## Custom Module Development

### Module Structure
Follow standard Odoo module structure in `my_addons/`:
```
your_module/
├── __init__.py
├── __manifest__.py
├── models/
├── views/
├── security/
├── data/
└── static/
```

### Creating New Modules
1. Reference the comprehensive guide: `HOW_TO_CREATE_MODULE.MD`
2. Use existing modules as templates (wa_marketing_automation, muk_web_theme)
3. Follow Odoo naming conventions

### Module Dependencies
- Core dependencies defined in requirements.txt (lines 1-92)
- Odoo module dependencies in __manifest__.py files
- UI themes depend on MuK modules chain

## Installed Custom Modules

### UI Theme Stack
- **muk_web_theme**: Main backend theme
- **muk_web_appsbar**: Enhanced app navigation
- **muk_web_chatter**: Improved messaging interface
- **muk_web_colors**: Color customization
- **muk_web_dialog**: Enhanced dialog components

### Business Modules
- **wa_marketing_automation**: WhatsApp marketing campaigns
  - Campaign management
  - Customer segmentation  
  - API integration
  - Scheduled actions

## WhatsApp Marketing Automation Module

### Module Overview
**Location**: `my_addons/wa_marketing_automation/`
**Version**: 18.0.1.0.0  
**Author**: Antony Gunawan
**Dependencies**: base, mail, crm

This is the primary business module for WhatsApp marketing automation with sophisticated campaign management, customer segmentation, and CRM integration.

### Architecture & Key Models

#### Core Models (4 main models):
1. **`wa_marketing_automation.campaign`** *(models/campaign.py:16)*
   - **Purpose**: Main campaign management with complex scheduling logic
   - **Key Methods**: `action_run()`, `action_test()`, `action_preview_messages()`
   - **Features**: State management, cron job scheduling, product recommendations

2. **`wa_marketing_automation.customer_segmentation`** *(models/customer_segmentation.py:10)*
   - **Purpose**: Customer targeting with manual/rule-based segmentation
   - **Validation**: Ensures customers have phone/mobile fields
   - **Rules Engine**: Safe domain expression evaluation

3. **`wa_marketing_automation.configuration`** *(models/configuration.py:9)*
   - **Purpose**: Singleton API configuration management
   - **Features**: Connection testing, URL validation
   - **Security**: Prevents multiple configurations

4. **`wa_marketing_automation.whatsapp_api_log`** *(models/whatsapp_api_log.py:4)*
   - **Purpose**: API call logging and monitoring
   - **Tracking**: Success/error status, execution types, recipient counts

### Development Workflows

#### Working with Campaign Logic
```bash
# Access models directly via Odoo shell
make run-shell

# In shell - test campaign methods
campaign = env['wa_marketing_automation.campaign'].browse(1)
campaign.action_preview_messages()  # Test message rendering
campaign.action_test()              # Send test message
```

#### Template Development
**File**: `utils.py:334` - `MessageTemplateRenderer` class
- **Template parsing**: Handles nested braces and complex expressions
- **Product formatting**: Multi-currency support with custom templates
- **Validation**: Template-product consistency checking

#### Debugging Scheduled Actions
```bash
# View active cron jobs
grep -r "Campaign" /var/log/odoo/odoo.log

# Check scheduled actions in UI
# Navigate to: WhatsApp Marketing Automation > Scheduled Actions
```

### Key File Locations

#### Models
- **Campaign logic**: `models/campaign.py` (1669 lines)
- **Customer segmentation**: `models/customer_segmentation.py` 
- **Configuration**: `models/configuration.py`
- **API logging**: `models/whatsapp_api_log.py`

#### Views  
- **Campaign UI**: `views/campaign_views.xml`
- **Menu structure**: `views/menu.xml`
- **Configuration**: `views/configuration_views.xml`

#### Utils & Helpers
- **Template rendering**: `utils.py:334-495`
- **Phone validation**: `utils.py:244-268` 
- **Currency formatting**: `utils.py:14-91`
- **Message sanitization**: `utils.py:271-311`

#### Data & Security
- **Cron cleanup job**: `data/ir_cron_data.xml`
- **Access rights**: `security/ir.model.access.csv`

### Testing & Debugging

#### Module-Specific Testing
```bash
# Test individual campaign components
python odoo-bin --test-enable --stop-after-init -i wa_marketing_automation

# Debug template rendering
# Set logging level in utils.py:11 to DEBUG
```

#### Common Development Tasks

1. **Adding New Template Variables**:
   - Update `MessageTemplateRenderer.render()` method *(utils.py:348)*
   - Add to context dictionary *(utils.py:364-367)*

2. **Modifying Campaign States**:
   - Update state selection *(campaign.py:24-34)*
   - Add corresponding action methods
   - Update UI buttons *(views/campaign_views.xml:36-48)*

3. **Extending Product Recommendations**:
   - Modify `product_recommendation_type` selection *(campaign.py:60-69)*
   - Add validation in `_check_template_products_consistency()` *(campaign.py:605)*

4. **API Integration Changes**:
   - Update `_action_send_messages()` method *(campaign.py:1473)*
   - Modify configuration model *(models/configuration.py)*

### Integration Points

#### CRM Integration
- **Opportunity creation**: `_create_opportunities()` *(campaign.py:930)*
- **UTM source tracking**: `_get_or_create_campaign_source()` *(campaign.py:997)*
- **Stage management**: Methods for handling won/lost opportunities

#### Product Integration  
- **Dynamic recommendations**: Via domain rules with `safe_eval()`
- **Price formatting**: Multi-currency support *(utils.py:14-91)*
- **Template formatting**: Custom product display templates

#### Cron Job Management
- **Cleanup automation**: `data/ir_cron_data.xml:6` (runs every 5 minutes)
- **Dynamic job creation**: Per-campaign scheduling *(campaign.py:1092-1185)*

### Documentation
The module includes 15 comprehensive documentation files:
- **Quick Start**: `QUICK_START_GUIDE.md`
- **User Guide**: `USER_GUIDE.md` 
- **Technical Reference**: `UTILS_GUIDE.md`
- **Visual Guides**: Multiple step-by-step guides
- **Best Practices**: `BEST_PRACTICES_GUIDE.md`

### Performance Considerations
- **Batch processing**: Multiple recipients per API call
- **Async scheduling**: Cron jobs prevent UI blocking  
- **Cleanup automation**: Prevents cron job accumulation
- **Safe evaluation**: Secure rule processing with `odoo.tools.safe_eval`

### Module Update Workflow
```bash
# After model changes
make run-update

# For view changes only 
# Refresh browser or restart with --dev=all flag

# For adding new dependencies
# Update __manifest__.py, then:
make run-update
```

### Analytics Metric Description Standards

When adding new analytics metrics to the WhatsApp Marketing Automation module, follow these business-friendly description standards to ensure consistency and user understanding:

#### Configuration Settings Description Format
All metric descriptions in `views/res_config_settings_views.xml` should follow this structure:

```xml
<setting string="Metric Name" help="[What it shows]. [What it analyzes]. [Data sources]. [How to use it]." />
```

**Required components:**
1. **What it shows**: Clear explanation of what the metric measures in business terms
2. **What it analyzes**: Specific data or behavior patterns examined
3. **Data sources**: Where the data comes from (orders, emails, website, etc.)
4. **How to use it**: Actionable business insights and use cases

**Example:**
```xml
<setting string="Eco-Friendly Score" help="Shows how much customers prefer environmentally-friendly products. Calculates the percentage of their purchases that include eco-friendly, organic, sustainable, green, bio, or natural products. Based on product purchase history and keyword analysis. Use this to target customers with sustainable product offerings and create eco-focused marketing campaigns." />
```

#### Customer Views Description Format
All metric descriptions in `views/res_partner_views.xml` should follow this structure:

```xml
<div class="alert alert-info" role="alert">
    <strong>[Business-Friendly Title]:</strong><br />
    [Brief explanation of what this shows]<br /><br />
    <strong>What we analyze:</strong>
    <ul>
        <li><strong>[Metric 1]:</strong> [Explanation in business terms]</li>
        <li><strong>[Metric 2]:</strong> [Explanation in business terms]</li>
    </ul>
    <strong>Data sources:</strong> [List all data sources used]<br /><br />
    <strong>Use this to:</strong> [Actionable business recommendations]
</div>
```

#### Writing Guidelines

1. **Use Business Language**: Avoid technical jargon, use terms business people understand
2. **Focus on Value**: Explain what the metric helps achieve, not just what it calculates
3. **Include Data Sources**: Always mention where the data comes from (builds trust)
4. **Provide Actions**: Give specific ways to use the metric for business decisions
5. **Be Consistent**: Use the same format and structure across all metrics

#### Examples of Good vs Bad Descriptions

**❌ Bad (Technical):**
```
"Multi-channel engagement analysis with adaptive weights: Email (40%), Website (35%), WhatsApp (25%)"
```

**✅ Good (Business-Friendly):**
```
"Shows how actively customers interact with your business. Looks at email opens and clicks, website visits and purchases, and WhatsApp message responses over the last 90 days."
```

#### Standard Metric Categories

When creating new metrics, categorize them properly:

1. **Core Analytics**: Always enabled (RFM, basic engagement)
2. **Behavioral Analytics**: Customer preferences and values
3. **Commerce Analytics**: Sales channels and payment behavior

Each category should have clear business value and use cases documented.

#### Configuration Field Naming

- Use descriptive field names: `eco_friendly_keywords` not `ef_kw`
- Include units in labels: `"Email Engagement Period (days)"`
- Provide sensible defaults and placeholders
- Group related fields visually in the UI

This ensures all analytics metrics are accessible to business users while maintaining technical accuracy.

## Analytics Metrics Development Guidelines

### CRITICAL: Avoid Heuristic-Based Metrics

When developing new analytics metrics, **NEVER** use indirect heuristics or assumptions. Always use direct, reliable data sources that actually measure what you claim to be measuring.

#### ❌ Examples of BAD Metric Logic (Heuristics to Avoid):

1. **Website Engagement Based on Order Timing**:
   ```python
   # WRONG - Orders ≠ Website Activity
   # Customers can order offline, by phone, in-store, etc.
   website_engagement = "recent orders with small amounts"
   ```

2. **Mobile Commerce Based on Order Amount**:
   ```python
   # WRONG - Order amount ≠ Device type
   # Small orders don't necessarily mean mobile usage
   mobile_usage = "orders under $50 on weekends"
   ```

3. **Channel Preference Based on Contact Method**:
   ```python
   # WRONG - Contact availability ≠ Preference
   # Having a phone number doesn't mean they prefer calls
   preferred_channel = "has phone number = prefers phone"
   ```

#### ✅ Examples of GOOD Metric Logic (Direct Data Sources):

1. **Email Engagement Based on Actual Email Data**:
   ```python
   # CORRECT - Use actual email interaction data
   email_messages = partner.message_ids.filtered(lambda m: m.message_type == 'email')
   opens_clicks = email_messages.mapped('email_opens') + email_messages.mapped('email_clicks')
   ```

2. **WhatsApp Success Based on Business Results**:
   ```python
   # CORRECT - Use won CRM opportunities with WhatsApp source
   won_whatsapp_deals = crm_leads.filtered(lambda l: 
       l.probability == 100 and 
       l.source_id.name.startswith('WhatsApp Campaign')
   )
   ```

3. **Website Engagement Based on Actual Website Activity**:
   ```python
   # CORRECT - Use actual website tracking data (when available)
   website_sessions = website_tracking_data.filter(partner_id=partner.id)
   page_views = website_sessions.sum('page_views')
   ```

#### Development Validation Checklist

Before implementing any new metric, ask these questions:

1. **Direct Measurement**: Does this metric directly measure what it claims to measure?
2. **Data Source Reliability**: Is the data source actually representative of the behavior?
3. **Business Logic Validation**: Would a business user agree this logic makes sense?
4. **False Positive Check**: Could this metric be high/low for reasons unrelated to what we're measuring?
5. **Transparency**: Can we clearly explain to a business user how this is calculated?

#### Fundamental Rules for Analytics Metrics

1. **Business Results > Activity Tracking**: Prefer metrics based on actual business outcomes (sales, conversions) over activity assumptions
2. **Direct Data > Heuristics**: Always use direct data sources when available
3. **Disable Rather Than Mislead**: If reliable data isn't available, disable the metric with clear documentation rather than using unreliable heuristics
4. **Validate Assumptions**: Test edge cases and validate that the metric behaves as expected in real scenarios
5. **Provide Transparency**: Every metric must have a clear calculation transparency display

#### Code Review Focus Areas

When reviewing analytics code, pay special attention to:

- Any logic that assumes behavior based on indirect indicators
- Metrics that use order timing/amounts to infer non-purchase behaviors  
- Channel preference logic based on contact information availability
- Any calculation that uses "heuristic" or "assumption" in comments
- Metrics without clear, direct data source documentation

#### Documentation Requirements

Every new metric must include:
- Clear explanation of data sources used
- Business logic validation reasoning
- Calculation transparency method
- Known limitations and edge cases
- Examples of when the metric might be misleading

This approach ensures analytics remain trustworthy and actionable for business decision-making.

## Database Configuration
- **Host**: localhost (default)
- **Port**: 5432 (PostgreSQL default)
- **Database**: odoo
- **User**: odoo
- **Password**: odoo (configured in .odoorc)

## Testing Strategy
- Run tests with: `make test`
- Module-specific tests in each addon's tests/ directory
- Framework supports Python unittest and Odoo test decorators

## Code Quality
- **Linting**: flake8 (install with `make install-dev`)
- **Formatting**: black (install with `make install-dev`)
- **Python Version**: 3.10+ (setup.py:68)

## Security Considerations
- Admin password is hashed in .odoorc:6
- Module access rights defined in security/ir.model.access.csv
- Follow Odoo security best practices

## Production Deployment
- Use `make run` for production mode
- Configure proper database credentials
- Remove --dev flags
- Set up proper logging and monitoring

## Troubleshooting

### Common Issues
1. **Module not found**: Check addons_path in .odoorc
2. **Database connection**: Verify PostgreSQL service and credentials
3. **Permission errors**: Check file permissions and user access
4. **Import errors**: Ensure virtual environment is activated
5. **XML validation error**: "Element odoo has extra content: data" means XML structure issues
   - All XML view files must have structure: `<odoo><data>...</data></odoo>`
6. **CSV security file error**: "No matching record found for external id" in CSV files
   - CSV files don't support `#` comments - remove lines entirely, don't try to comment them out

### Development Tools
- Use `make run-shell` for interactive debugging
- Enable developer mode with --dev=all flag
- Check logs for detailed error information

### Server Command Timeouts
**IMPORTANT**: Server commands (like `make run-dev`, `make run-update`) may timeout after 2 minutes when run through automated tools. If testing module changes:
1. Notify developer about changes that need testing
2. Run commands manually in terminal for better reliability
3. Use `make run-update -d odoo` with database parameter for module updates

## References
- **Odoo Documentation**: https://www.odoo.com/documentation/18.0/
- **Module Creation Guide**: HOW_TO_CREATE_MODULE.MD
- **Contributing**: CONTRIBUTING.md
- **Security**: SECURITY.md

## Quick Commands Reference
```bash
# Essential development commands
make help              # Show all available commands
make run-dev          # Start development server
make run-shell        # Access Odoo shell
make test             # Run tests
make clean            # Clean cache files
make install-dev      # Install dev dependencies

# Database operations
make run-init         # Initialize database
make run-update       # Update modules
make db-create        # Create database

# Code quality
make lint             # Check code style
make format           # Format code
```

## Module Development Workflow
1. Create module structure in my_addons/
2. Define models in models/
3. Create views in views/
4. Set security permissions in security/
5. Update module via Apps menu or make run-update
6. Test functionality
7. Document changes

## Environment Variables
Configure via .odoorc file:
- Database settings (lines 2-4)
- Addons path (line 5)
- Admin password (line 6)

This setup provides a robust development environment for Odoo ERP customization with modern UI enhancements and marketing automation capabilities.