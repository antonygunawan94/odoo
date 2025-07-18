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