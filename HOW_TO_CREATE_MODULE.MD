# How to Create Odoo Modules - Complete Setup Guide

This guide will walk you through setting up a fresh Odoo installation and creating custom modules/addons from scratch.

## Prerequisites

Before starting, ensure you have:

- Python 3.8+ installed
- PostgreSQL database server running
- Odoo 18.0 installed
- Basic understanding of Python and XML

## Step 1: Setup .odoorc Configuration

The `.odoorc` file is a configuration file that tells Odoo how to connect to your database and where to find your custom addons.

### 1.1 Create .odoorc file

Create a `.odoorc` file in your home directory (`C:\Users\<username>\.odoorc` on Windows or `~/.odoorc` on Linux/Mac):

```ini
[options]
# Database configuration
db_host = localhost
db_port = 5432
db_user = your_db_user
db_password = your_db_password
dbfilter = your_database_name

# Server configuration
http_port = 8069
workers = 0

# Addons path - include both standard addons and your custom addons
addons_path = /path/to/odoo/addons,/path/to/odoo/my_addons

# Logging
log_level = info
log_handler = :INFO

# Development settings
dev_mode = reload,qweb,werkzeug,xml
```

### 1.2 Create Custom Addons Directory

1. Create your custom addons directory:

   ```bash
   mkdir my_addons
   ```

2. Update the `addons_path` in your `.odoorc` file to include this directory:
   ```ini
   addons_path = /path/to/odoo/addons,/path/to/odoo/my_addons
   ```

### 1.3 Example .odoorc for this project

Based on the current project structure:

```ini
[options]
# Database configuration
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
dbfilter = odoo_db

# Server configuration
http_port = 8069
workers = 0

# Addons path
addons_path = C:\Users\anton\labs\odoo\odoo\addons,C:\Users\anton\labs\odoo\odoo\my_addons

# Development settings
dev_mode = reload,qweb,werkzeug,xml
log_level = info
```

## Step 2: Create Your Custom Addon Directory

### 2.1 Basic Module Structure

Every Odoo module follows a standard directory structure. Create your module directory inside `my_addons/`:

```
my_addons/
└── your_module_name/
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    │   ├── __init__.py
    │   └── your_model.py
    ├── views/
    │   ├── __init__.py
    │   ├── your_views.xml
    │   └── menu.xml
    ├── security/
    │   └── ir.model.access.csv
    ├── data/
    │   └── data.xml (optional)
    └── static/
        └── description/
            └── icon.png (optional)
```

### 2.2 Create the Module Directory

```bash
cd my_addons
mkdir your_module_name
cd your_module_name
mkdir models views security data static/description
```

## Step 3: Create Module Files

Based on the `smart_engagement` reference module, here's how to create each component:

### 3.1 Create **manifest**.py

The manifest file defines your module's metadata and dependencies:

```python
{
    "name": "Your Module Name",
    "version": "18.0.1.0.0",
    "category": "Your Category",
    "summary": "Brief description of your module",
    "description": """
        Detailed description of your module functionality.
        You can include multiple lines here.
    """,
    "author": "Your Name",
    "depends": ["base", "mail"],  # Dependencies on other modules
    "data": [
        "security/ir.model.access.csv",
        "views/your_views.xml",
        "views/menu.xml",
        "data/data.xml",  # Optional
    ],
    "demo": [
        # Demo data files (optional)
    ],
    "installable": True,
    "auto_install": False,
    "application": True,  # Set to True if this is a main application
    "license": "LGPL-3",
}
```

### 3.2 Create Module **init**.py

The main module initialization file:

```python
from . import models
```

### 3.3 Create Models

#### models/**init**.py

```python
from . import your_model
```

#### models/your_model.py

Example based on the campaign model:

```python
from odoo import api, fields, models


class YourModel(models.Model):
    _name = "your_module.your_model"
    _description = "Your Model Description"
    _rec_name = "name"  # Field to use as record name

    # Basic fields
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)

    # Date fields
    create_date = fields.Datetime(string="Created On", readonly=True)
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")

    # Selection field
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')

    # Relational fields
    user_id = fields.Many2one('res.users', string="Responsible User", default=lambda self: self.env.user)
    partner_ids = fields.Many2many('res.partner', string="Partners")

    # Computed fields
    total_partners = fields.Integer(string="Total Partners", compute="_compute_total_partners")

    @api.depends('partner_ids')
    def _compute_total_partners(self):
        for record in self:
            record.total_partners = len(record.partner_ids)

    # Methods
    def action_start(self):
        self.state = 'active'

    def action_done(self):
        self.state = 'done'
```

### 3.4 Create Views

#### views/**init**.py

```python
# This file can be empty or contain view-related imports
```

#### views/your_views.xml

Example based on the campaign views:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Action Window -->
    <record id="your_model_action" model="ir.actions.act_window">
        <field name="name">Your Model</field>
        <field name="res_model">your_module.your_model</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create a new record to get started.
            </p>
        </field>
    </record>

    <!-- List View -->
    <record id="your_model_list_view" model="ir.ui.view">
        <field name="name">your_module.your_model.list</field>
        <field name="model">your_module.your_model</field>
        <field name="arch" type="xml">
            <list string="Your Model">
                <field name="name"/>
                <field name="state"/>
                <field name="date_start"/>
                <field name="date_end"/>
                <field name="total_partners"/>
                <field name="user_id"/>
            </list>
        </field>
    </record>

    <!-- Form View -->
    <record id="your_model_form_view" model="ir.ui.view">
        <field name="name">your_module.your_model.form</field>
        <field name="model">your_module.your_model</field>
        <field name="arch" type="xml">
            <form string="Your Model">
                <header>
                    <button name="action_start" string="Start" type="object" class="btn-primary"
                            invisible="state != 'draft'"/>
                    <button name="action_done" string="Mark as Done" type="object" class="btn-primary"
                            invisible="state != 'active'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,active,done"/>
                </header>
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="user_id"/>
                            <field name="active"/>
                        </group>
                        <group>
                            <field name="date_start"/>
                            <field name="date_end"/>
                            <field name="total_partners"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Description">
                            <field name="description"/>
                        </page>
                        <page string="Partners">
                            <field name="partner_ids">
                                <list>
                                    <field name="name"/>
                                    <field name="email"/>
                                    <field name="phone"/>
                                </list>
                            </field>
                        </page>
                    </notebook>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="your_model_search_view" model="ir.ui.view">
        <field name="name">your_module.your_model.search</field>
        <field name="model">your_module.your_model</field>
        <field name="arch" type="xml">
            <search>
                <field name="name"/>
                <field name="user_id"/>
                <filter string="Active" name="active" domain="[('active', '=', True)]"/>
                <filter string="Draft" name="draft" domain="[('state', '=', 'draft')]"/>
                <filter string="Active Records" name="active_records" domain="[('state', '=', 'active')]"/>
                <group expand="0" string="Group By">
                    <filter string="Status" name="group_state" context="{'group_by': 'state'}"/>
                    <filter string="Responsible User" name="group_user" context="{'group_by': 'user_id'}"/>
                </group>
            </search>
        </field>
    </record>

</odoo>
```

#### views/menu.xml

Create menu items to access your module:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Main Menu -->
    <menuitem id="your_module_main_menu"
              name="Your Module"
              sequence="10"/>

    <!-- Sub Menu -->
    <menuitem id="your_module_submenu"
              name="Your Models"
              parent="your_module_main_menu"
              sequence="10"/>

    <!-- Menu Item -->
    <menuitem id="your_model_menu"
              name="Your Model"
              parent="your_module_submenu"
              action="your_model_action"
              sequence="10"/>

</odoo>
```

### 3.5 Create Security

#### security/ir.model.access.csv

Define access rights for your models:

```csv
id,name,model_id:id,group_id:id,perm_create,perm_write,perm_read,perm_unlink
access_your_module_your_model,access.your_module.your_model,model_your_module_your_model,base.group_user,1,1,1,1
```

Columns explanation:

- `id`: Unique identifier for the access rule
- `name`: Human-readable name
- `model_id:id`: Reference to the model (format: model_module_name_model_name)
- `group_id:id`: User group that gets these permissions
- `perm_create`: Create permission (1=yes, 0=no)
- `perm_write`: Write permission (1=yes, 0=no)
- `perm_read`: Read permission (1=yes, 0=no)
- `perm_unlink`: Delete permission (1=yes, 0=no)

## Step 4: Install and Test Your Module

### 4.1 Start Odoo with your configuration

```bash
./odoo-bin -c ~/.odoorc --dev=reload,qweb,werkzeug,xml
```

### 4.2 Install your module

1. Go to Apps menu
2. Click "Update Apps List"
3. Search for your module name
4. Click "Install"

### 4.3 Access your module

Navigate to your module through the main menu you created.

## Development Tips

### Best Practices

1. **Naming Conventions**:

   - Module names: use underscores (e.g., `your_module_name`)
   - Model names: use dots (e.g., `your_module.your_model`)
   - Field names: use underscores (e.g., `field_name`)

2. **Version Control**:

   - Always use version control for your custom modules
   - Keep your custom modules in a separate repository

3. **Testing**:

   - Test your module thoroughly before deploying to production
   - Use Odoo's testing framework for automated tests

4. **Documentation**:
   - Document your module's functionality
   - Add helpful descriptions in manifest files

### Common Issues and Solutions

1. **Module not appearing**: Check that the module path is correctly added to `addons_path` in `.odoorc`
2. **Access denied**: Verify security permissions in `ir.model.access.csv`
3. **View errors**: Check XML syntax and field names in view definitions
4. **Import errors**: Ensure all `__init__.py` files are present and contain correct imports

## Reference Structure (smart_engagement)

This guide is based on the existing `smart_engagement` module structure:

```
smart_engagement/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── campaign.py
│   └── customer_segmentation.py
├── views/
│   ├── __init__.py
│   ├── campaign_views.xml
│   ├── customer_segmentation_views.xml
│   └── menu.xml
└── security/
    └── ir.model.access.csv
```

You can examine this module for additional examples and inspiration for your own modules.

## Additional Resources

- [Odoo Official Documentation](https://www.odoo.com/documentation/18.0/)
- [Odoo Developer Guide](https://www.odoo.com/documentation/18.0/developer.html)
- [Odoo Model Reference](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html)
- [Odoo View Architecture](https://www.odoo.com/documentation/18.0/developer/reference/backend/views.html)
