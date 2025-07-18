# Utils Organization Guide for Odoo

This guide explains how to organize utility functions in your Odoo addon for better code maintainability and reusability.

## 📁 File Structure

```
my_addon/
├── __init__.py                 # Import models only
├── utils.py                    # ✅ General utilities (Method 1)
├── models/
│   ├── __init__.py            # Import all models
│   ├── utils.py               # ✅ Model-specific utilities (Method 2)
│   ├── campaign.py            # Your models
│   └── ...
└── ...
```

## 🎯 When to Create Utils

### ✅ Good candidates for utils:

- **Data formatting functions** (price, currency, phone numbers)
- **Template rendering logic**
- **Validation functions**
- **Common calculations**
- **API helpers**
- **Text processing functions**
- **Helper classes that don't need database access**

### ❌ Keep in models:

- **Business logic specific to one model**
- **Database operations requiring `self`**
- **Computed fields**
- **Model-specific actions**

## 📝 Method 1: Addon Root Utils (`utils.py`)

**Best for:** General utility functions that can be used across different models.

```python
# my_addon/utils.py
def format_price_with_currency(price, currency_code=None):
    """General price formatting utility."""
    # Implementation here
    pass

def validate_phone_number(phone):
    """Phone validation utility."""
    # Implementation here
    pass
```

**Usage in models:**

```python
# models/campaign.py
from ..utils import format_price_with_currency, validate_phone_number

class Campaign(models.Model):
    _name = "my_addon.campaign"

    def some_method(self):
        formatted_price = format_price_with_currency(100.0, "USD")
        is_valid, clean_phone = validate_phone_number("+1234567890")
```

## 🔧 Method 2: Model Utils (`models/utils.py`)

**Best for:** Utilities that work with Odoo models and recordsets.

```python
# models/utils.py
from odoo import fields

def get_company_currency(env):
    """Get company currency - needs env access."""
    return env.company.currency_id

def safe_field_access(record, field_name, default=None):
    """Safely access record fields."""
    return getattr(record, field_name, default) or default
```

**Usage in models:**

```python
# models/campaign.py
from .utils import get_company_currency, safe_field_access

class Campaign(models.Model):
    _name = "my_addon.campaign"

    def some_method(self):
        currency = get_company_currency(self.env)
        name = safe_field_access(self, 'partner_id.name', 'Unknown')
```

## 🏗️ Method 3: Helper Classes

**Best for:** Complex utilities that need to maintain state or multiple related functions.

```python
# utils.py or models/utils.py
class MessageTemplateRenderer:
    def __init__(self, env):
        self.env = env

    def render(self, template, customer, products=None):
        # Complex rendering logic
        pass

    def _format_products_default(self, products):
        # Helper method
        pass
```

**Usage:**

```python
# In your model
def render_message(self):
    renderer = MessageTemplateRenderer(self.env)
    return renderer.render(self.template, self.customer)
```

## 🎨 Best Practices

### 1. **Import Organization**

```python
# ✅ Good - Specific imports
from ..utils import format_price_with_currency, validate_phone_number
from .utils import get_company_currency, RecordHelper

# ❌ Avoid - Wildcard imports
from ..utils import *
```

### 2. **Function Design**

```python
# ✅ Good - Pure function, testable
def format_price_with_currency(price, currency_code=None, company_currency=None):
    """
    Format price with currency.

    Args:
        price (float): Price to format
        currency_code (str, optional): Currency code
        company_currency (recordset, optional): Currency record

    Returns:
        str: Formatted price string
    """
    # Implementation

# ❌ Avoid - Depends on self, should be in model
def format_price_with_currency(self, price):
    currency = self.env.company.currency_id
    # ...
```

### 3. **Error Handling**

```python
# ✅ Good - Graceful error handling
def safe_operation(data):
    try:
        # Operation
        return result
    except Exception as e:
        _logger.warning(f"Error in safe_operation: {e}")
        return default_value

# ❌ Avoid - Let errors bubble up without context
def unsafe_operation(data):
    # This could crash without warning
    return complex_operation(data)
```

### 4. **Documentation**

```python
# ✅ Good - Clear docstrings with examples
def validate_phone_number(phone):
    """
    Validate and format a phone number for WhatsApp.

    Args:
        phone (str): Phone number to validate

    Returns:
        tuple: (is_valid: bool, formatted_phone: str)

    Example:
        >>> validate_phone_number("+1-234-567-8900")
        (True, "12345678900")
    """
```

## 🧪 Testing Utils

Create test files for your utilities:

```python
# tests/test_utils.py
from odoo.tests import TransactionCase
from ..utils import format_price_with_currency, validate_phone_number

class TestUtils(TransactionCase):
    def test_format_price_with_currency(self):
        result = format_price_with_currency(1000.50, "USD")
        self.assertEqual(result, "$1,000.50")

    def test_validate_phone_number(self):
        is_valid, formatted = validate_phone_number("+1234567890")
        self.assertTrue(is_valid)
        self.assertEqual(formatted, "1234567890")
```

## 🔄 Refactoring Existing Code

### Before (in model):

```python
class Campaign(models.Model):
    def _format_price_with_currency(self, product):
        # 50+ lines of complex formatting logic
        currency_symbol = "Rp"
        # ... lots of code ...
        return f"{currency_symbol}{formatted_number}"
```

### After (using utils):

```python
# utils.py
def format_price_with_currency(price, currency_code=None, company_currency=None):
    # 50+ lines moved here
    pass

# models/campaign.py
from ..utils import format_price_with_currency

class Campaign(models.Model):
    def _format_price_with_currency(self, product):
        return format_price_with_currency(
            product.list_price,
            company_currency=self.env.company.currency_id
        )
```

## 📊 Summary

| Approach             | Use Case                    | Import Path                 | Pros                       | Cons                   |
| -------------------- | --------------------------- | --------------------------- | -------------------------- | ---------------------- |
| **Addon Root Utils** | General functions           | `from ..utils import func`  | Clean separation, reusable | No direct model access |
| **Model Utils**      | Model-related helpers       | `from .utils import func`   | Has env/model access       | More coupled to Odoo   |
| **Helper Classes**   | Complex stateful operations | `from ..utils import Class` | Organized, maintainable    | More complex           |

Choose the approach that best fits your specific utility functions!
