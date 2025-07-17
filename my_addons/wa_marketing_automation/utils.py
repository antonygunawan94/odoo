"""
Utility functions for WhatsApp Marketing Automation addon.

This module contains helper functions that can be reused across different models
within the wa_marketing_automation addon.
"""

import logging
import re

_logger = logging.getLogger(__name__)


def format_price_with_currency(price, currency_code=None, company_currency=None):
    """
    Format product price with proper currency formatting.

    Args:
        price (float): The price to format
        currency_code (str, optional): Currency code (e.g., 'USD', 'EUR')
        company_currency (recordset, optional): Company currency record

    Returns:
        str: Formatted price string with currency symbol, appropriate decimal places, and thousand separators
    """
    # Currency-specific formatting rules
    NO_DECIMAL_CURRENCIES = {
        "IDR": {"symbol": "Rp", "thousand_sep": "."},  # Indonesian Rupiah
        "JPY": {"symbol": "¥", "thousand_sep": ","},  # Japanese Yen
        "KRW": {"symbol": "₩", "thousand_sep": ","},  # Korean Won
        "VND": {"symbol": "₫", "thousand_sep": "."},  # Vietnamese Dong
        "CLP": {"symbol": "$", "thousand_sep": "."},  # Chilean Peso
        "TWD": {"symbol": "NT$", "thousand_sep": ","},  # Taiwan Dollar
        "HUF": {"symbol": "Ft", "thousand_sep": " "},  # Hungarian Forint
        "ISK": {"symbol": "kr", "thousand_sep": "."},  # Icelandic Krona
    }

    DECIMAL_CURRENCIES = {
        "USD": {"symbol": "$", "thousand_sep": ",", "decimal_sep": "."},
        "EUR": {"symbol": "€", "thousand_sep": ".", "decimal_sep": ","},
        "GBP": {"symbol": "£", "thousand_sep": ",", "decimal_sep": "."},
        "AUD": {"symbol": "A$", "thousand_sep": ",", "decimal_sep": "."},
        "CAD": {"symbol": "C$", "thousand_sep": ",", "decimal_sep": "."},
    }

    # Default values (Indonesian Rupiah)
    currency_symbol = "Rp"
    decimal_places = 0
    thousand_sep = "."
    decimal_sep = ","

    try:
        # Determine currency code
        if not currency_code and company_currency:
            currency_code = getattr(company_currency, "name", "")

        if currency_code:
            # Check if it's a no-decimal currency
            if currency_code in NO_DECIMAL_CURRENCIES:
                currency_info = NO_DECIMAL_CURRENCIES[currency_code]
                currency_symbol = currency_info["symbol"]
                thousand_sep = currency_info["thousand_sep"]
                decimal_places = 0
            # Check if it's a decimal currency
            elif currency_code in DECIMAL_CURRENCIES:
                currency_info = DECIMAL_CURRENCIES[currency_code]
                currency_symbol = currency_info["symbol"]
                thousand_sep = currency_info["thousand_sep"]
                decimal_sep = currency_info["decimal_sep"]
                decimal_places = 2

        # Format the number
        if decimal_places == 0:
            # No decimal places
            formatted_number = str(int(round(price)))
        else:
            # With decimal places
            formatted_number = f"{price:.{decimal_places}f}"
            if decimal_sep != ".":
                formatted_number = formatted_number.replace(".", decimal_sep)

        # Add thousand separators
        formatted_number = add_thousand_separators(
            formatted_number, thousand_sep, decimal_sep
        )

        return f"{currency_symbol}{formatted_number}"

    except Exception as e:
        _logger.warning(f"Error formatting price {price}: {e}")
        return f"Rp{int(round(price))}"


def add_thousand_separators(number_str, separator=",", decimal_sep="."):
    """
    Add thousand separators to a number string.

    Args:
        number_str (str): String representation of the number
        separator (str): Thousand separator character
        decimal_sep (str): Decimal separator character

    Returns:
        str: Number string with thousand separators
    """
    try:
        # Split by decimal separator
        parts = str(number_str).split(decimal_sep)
        integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else ""

        # Add thousand separators to integer part
        if len(integer_part) > 3:
            # Reverse, add separators every 3 digits, then reverse back
            reversed_int = integer_part[::-1]
            separated = separator.join(
                [reversed_int[i : i + 3] for i in range(0, len(reversed_int), 3)]
            )
            integer_part = separated[::-1]

        # Reconstruct the number
        if decimal_part:
            return f"{integer_part}{decimal_sep}{decimal_part}"
        else:
            return integer_part

    except Exception as e:
        _logger.warning(f"Error adding thousand separators to {number_str}: {e}")
        return str(number_str)


def parse_template_expression(expression):
    """
    Parse a template expression to extract function name and parameters.

    Args:
        expression (str): Complete template expression like "{products:product_item_format(custom format)}"

    Returns:
        dict: Parsed expression with 'variable', 'function', and 'params'
    """
    try:
        _logger.debug(f"Parsing template expression: {expression}")

        # Remove outer braces if present
        inner_expression = expression
        if expression.startswith("{") and expression.endswith("}"):
            inner_expression = expression[1:-1]

        _logger.debug(f"Inner expression after removing braces: {inner_expression}")

        # Pattern to match: variable:function(params) - improved to handle nested braces
        # First, check if it contains a colon and parentheses
        if (
            ":" in inner_expression
            and "(" in inner_expression
            and ")" in inner_expression
        ):
            # Split on the first colon
            parts = inner_expression.split(":", 1)
            if len(parts) == 2:
                variable = parts[0].strip()
                func_part = parts[1].strip()

                # Find the function name (everything before the first opening parenthesis)
                paren_index = func_part.find("(")
                if paren_index != -1:
                    function = func_part[:paren_index].strip()
                    # Get everything between the first ( and last )
                    params_part = func_part[paren_index + 1 :]
                    if params_part.endswith(")"):
                        params = params_part[:-1]  # Remove the last )

                        result = {
                            "variable": variable,
                            "function": function,
                            "params": params,
                        }
                        _logger.debug(f"Parsed result: {result}")
                        return result

        # Simple variable without function
        result = {
            "variable": inner_expression.strip(),
            "function": None,
            "params": None,
        }
        _logger.debug(f"Simple variable result: {result}")
        return result

    except Exception as e:
        _logger.warning(f"Error parsing template expression {expression}: {e}")
        return {"variable": expression, "function": None, "params": None}


def find_template_expressions(template):
    """
    Find all template expressions in a message template, handling nested braces properly.

    Args:
        template (str): Message template with placeholders

    Returns:
        list: List of complete expressions found in the template (including outer braces)
    """
    try:
        expressions = []
        i = 0
        while i < len(template):
            if template[i] == "{":
                # Found start of expression, find the matching closing brace
                brace_count = 1
                start = i
                i += 1

                while i < len(template) and brace_count > 0:
                    if template[i] == "{":
                        brace_count += 1
                    elif template[i] == "}":
                        brace_count -= 1
                    i += 1

                if brace_count == 0:
                    # Found complete expression
                    complete_expression = template[start:i]
                    expressions.append(complete_expression)
                    _logger.debug(f"Found complete expression: {complete_expression}")
                else:
                    # Unclosed brace, skip
                    _logger.warning(
                        f"Unclosed brace found starting at position {start}"
                    )
                    break
            else:
                i += 1

        _logger.debug(f"Total expressions found: {len(expressions)}")
        return expressions
    except Exception as e:
        _logger.warning(f"Error finding template expressions in template: {e}")
        return []


def validate_phone_number(phone):
    """
    Validate and format a phone number for WhatsApp.

    Args:
        phone (str): Phone number to validate

    Returns:
        tuple: (is_valid: bool, formatted_phone: str)
    """
    if not phone:
        return False, ""

    # Remove all non-digit characters
    clean_phone = re.sub(r"\D", "", str(phone))

    # Deny phone that doesn't have explicit country code
    if clean_phone.startswith("0"):
        return False, ""

    # Check if it's a valid length (typically 10-15 digits)
    if len(clean_phone) < 10 or len(clean_phone) > 15:
        return False, clean_phone

    return True, clean_phone


def sanitize_message_content(message):
    """
    Sanitize message content for WhatsApp API.
    Preserves intentional newlines while cleaning up excessive whitespace.

    Args:
        message (str): Message content to sanitize

    Returns:
        str: Sanitized message content
    """
    if not message:
        return ""

    # Remove or replace invalid characters
    # WhatsApp has specific character limitations
    sanitized = str(message)

    # Preserve newlines but clean up other excessive whitespace
    # First, replace multiple consecutive newlines with double newlines (max)
    sanitized = re.sub(r"\n{3,}", "\n\n", sanitized)

    # Clean up whitespace on each line while preserving newlines
    lines = sanitized.split("\n")
    cleaned_lines = []

    for line in lines:
        # Remove excessive spaces/tabs on each line
        cleaned_line = re.sub(r"[ \t]+", " ", line)
        # Trim leading/trailing whitespace from each line
        cleaned_line = cleaned_line.strip()
        cleaned_lines.append(cleaned_line)

    # Rejoin with newlines
    sanitized = "\n".join(cleaned_lines)

    # Remove leading/trailing newlines from the entire message
    sanitized = sanitized.strip("\n")

    return sanitized


def show_notification(
    env, type: str, title: str, message: str, sticky=False, direct_return=False
):
    if direct_return:
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": type,
                "title": title,
                "message": message,
                "sticky": sticky,
            },
        }

    env.user._bus_send(
        "simple_notification",
        {"type": type, "title": title, "message": message, "sticky": sticky},
    )


class MessageTemplateRenderer:
    """
    Helper class for rendering message templates with various placeholders.
    """

    def __init__(self, env):
        """
        Initialize the renderer with Odoo environment.

        Args:
            env: Odoo environment object
        """
        self.env = env

    def render(self, template, customer=None, products=None, **kwargs):
        """
        Render a message template with customer and product data.

        Args:
            template (str): Message template with placeholders
            customer (recordset, optional): Customer record
            products (recordset, optional): Product records
            **kwargs: Additional context variables

        Returns:
            str: Rendered message
        """
        try:
            _logger.debug(f"Starting template rendering with template: {template}")

            context = {
                "customer_name": customer.name if customer else "",
                **kwargs,
            }
            _logger.debug(f"Rendering context: {context}")

            # Process template expressions (now returns complete expressions with braces)
            expression_strings = find_template_expressions(template)
            _logger.debug(f"Found expression strings: {expression_strings}")
            rendered_template = template

            for expression_string in expression_strings:
                _logger.debug(f"Processing expression string: {expression_string}")

                # Parse the expression
                expr = parse_template_expression(expression_string)
                _logger.debug(f"Parsed expression: {expr}")

                # The placeholder is the complete expression string (already includes braces)
                placeholder = expression_string
                _logger.debug(f"Using placeholder: {placeholder}")

                # Replace with actual content
                if expr["variable"] == "products" and products:
                    _logger.debug(f"Processing products with {len(products)} items")
                    if expr["function"] == "product_item_format" and expr["params"]:
                        formatted_products = self._format_products_custom(
                            products, expr["params"]
                        )
                    else:
                        formatted_products = self._format_products_default(products)

                    _logger.debug(f"Formatted products: {formatted_products}")
                    _logger.debug(f"Replacing '{placeholder}' with formatted products")

                    rendered_template = rendered_template.replace(
                        placeholder, formatted_products
                    )
                    _logger.debug(f"Template after replacement: {rendered_template}")

                elif expr["variable"] in context:
                    _logger.debug(
                        f"Replacing '{placeholder}' with context value: {context[expr['variable']]}"
                    )
                    rendered_template = rendered_template.replace(
                        placeholder, str(context[expr["variable"]])
                    )

            _logger.debug(f"Final rendered template: {rendered_template}")
            return sanitize_message_content(rendered_template)

        except Exception as e:
            _logger.error(f"Error rendering template: {e}")
            return template

    def _format_products_default(self, products):
        """Format products with default format."""
        formatted_items = []
        for product in products:
            price_formatted = format_price_with_currency(
                product.lst_price, company_currency=self.env.company.currency_id
            )
            formatted_items.append(f"{product.name} - {price_formatted}")
        return "\n".join(formatted_items)

    def _format_products_custom(self, products, format_template):
        """
        Format products with custom format template.
        Supports newlines and multiple formatting options.
        """
        _logger.debug(
            f"Formatting {len(products)} products with template: {format_template}"
        )

        # Decode common escape sequences in format template
        decoded_template = format_template
        # Handle common escape sequences that might be in the template
        decoded_template = decoded_template.replace("\\n", "\n")
        decoded_template = decoded_template.replace("\\t", "\t")

        _logger.debug(f"Decoded template: {repr(decoded_template)}")

        formatted_items = []
        for i, product in enumerate(products, 1):
            _logger.debug(
                f"Processing product {i}: {product.name} (price: {product.lst_price})"
            )

            item_text = decoded_template

            # Replace product-specific placeholders
            item_text = item_text.replace("{product_name}", product.name or "")
            _logger.debug(f"After product_name replacement: {repr(item_text)}")

            price_formatted = format_price_with_currency(
                product.lst_price, company_currency=self.env.company.currency_id
            )
            _logger.debug(f"Formatted price: {price_formatted}")

            item_text = item_text.replace("{product_price}", price_formatted)

            # Add additional placeholders for more flexibility
            item_text = item_text.replace("{product_index}", str(i))
            item_text = item_text.replace("{product_number}", str(i))

            # Handle product description if available
            description = (
                getattr(product, "description_sale", "")
                or getattr(product, "description", "")
                or ""
            )
            item_text = item_text.replace("{product_description}", description)

            # Handle product code/SKU if available
            default_code = getattr(product, "default_code", "") or ""
            item_text = item_text.replace("{product_code}", default_code)
            item_text = item_text.replace("{product_sku}", default_code)

            _logger.debug(f"After all replacements: {repr(item_text)}")
            formatted_items.append(item_text)

        # Join items - if template already contains newlines, use double newline as separator
        # Otherwise use single newline
        if "\n" in decoded_template:
            separator = "\n\n"  # Extra space between products when template has internal newlines
        else:
            separator = "\n"  # Single newline for simple single-line templates

        result = separator.join(formatted_items)
        _logger.debug(f"Final formatted products result: {repr(result)}")
        return result


# def _format_price_with_currency(self, product):
#     """
#     Format product price with proper currency formatting.

#     Args:
#         product: product.product record

#     Returns:
#         Formatted price string with currency symbol, appropriate decimal places, and thousand separators
#     """
#     # Currency-specific formatting rules
#     # Currencies that typically don't use decimal places
#     NO_DECIMAL_CURRENCIES = {
#         "IDR": {"symbol": "Rp", "thousand_sep": "."},  # Indonesian Rupiah
#         "JPY": {"symbol": "¥", "thousand_sep": ","},  # Japanese Yen
#         "KRW": {"symbol": "₩", "thousand_sep": ","},  # Korean Won
#         "VND": {"symbol": "₫", "thousand_sep": "."},  # Vietnamese Dong
#         "CLP": {"symbol": "$", "thousand_sep": "."},  # Chilean Peso
#         "TWD": {"symbol": "NT$", "thousand_sep": ","},  # Taiwan Dollar
#         "HUF": {"symbol": "Ft", "thousand_sep": " "},  # Hungarian Forint
#         "ISK": {"symbol": "kr", "thousand_sep": "."},  # Icelandic Krona
#     }

#     # Currencies with 2 decimal places and their thousand separators
#     DECIMAL_CURRENCIES = {
#         "USD": {"symbol": "$", "thousand_sep": ",", "decimal_sep": "."},
#         "EUR": {"symbol": "€", "thousand_sep": ".", "decimal_sep": ","},
#         "GBP": {"symbol": "£", "thousand_sep": ",", "decimal_sep": "."},
#         "AUD": {"symbol": "A$", "thousand_sep": ",", "decimal_sep": "."},
#         "CAD": {"symbol": "C$", "thousand_sep": ",", "decimal_sep": "."},
#     }

#     # Default values (Indonesian Rupiah)
#     currency_symbol = "Rp"
#     decimal_places = 0
#     thousand_sep = "."
#     decimal_sep = ","

#     try:
#         # Try to get company currency if available
#         if hasattr(self.env, "company"):
#             company = self.env.company
#             if hasattr(company, "currency_id") and company.currency_id:
#                 currency = company.currency_id

#                 # Get currency code
#                 currency_code = getattr(currency, "name", "")

#                 # Check if it's a no-decimal currency
#                 if currency_code in NO_DECIMAL_CURRENCIES:
#                     currency_info = NO_DECIMAL_CURRENCIES[currency_code]
#                     currency_symbol = currency_info["symbol"]
#                     thousand_sep = currency_info["thousand_sep"]
#                     decimal_places = 0
#                 # Check if it's a decimal currency
#                 elif currency_code in DECIMAL_CURRENCIES:
#                     currency_info = DECIMAL_CURRENCIES[currency_code]
#                     currency_symbol = currency_info["symbol"]
#                     thousand_sep = currency_info["thousand_sep"]
#                     decimal_sep = currency_info["decimal_sep"]
#                     decimal_places = 2
#                 # Fallback to Odoo's currency symbol with default formatting
#                 elif hasattr(currency, "symbol") and currency.symbol:
#                     currency_symbol = currency.symbol
#                     decimal_places = 2
#                     thousand_sep = ","
#                     decimal_sep = "."
#     except:
#         # Use default values if anything fails
#         pass

#     # Format the number with proper separators
#     price = product.lst_price

#     if decimal_places == 0:
#         # No decimal places - round to nearest whole number
#         price_int = int(round(price))
#         # Add thousand separators
#         formatted_price = self._add_thousand_separators(price_int, thousand_sep)
#     else:
#         # With decimal places
#         # Split into integer and decimal parts
#         price_int = int(price)
#         price_decimal = round((price - price_int), decimal_places)

#         # Format integer part with thousand separators
#         formatted_int = self._add_thousand_separators(price_int, thousand_sep)

#         # Format decimal part
#         decimal_str = f"{price_decimal:.{decimal_places}f}".split(".")[1]

#         formatted_price = f"{formatted_int}{decimal_sep}{decimal_str}"

#     return f"{currency_symbol} {formatted_price}"

# def _add_thousand_separators(self, number, separator):
#     """
#     Add thousand separators to a number.

#     Args:
#         number: Integer number
#         separator: Separator character (e.g., '.', ',', ' ')

#     Returns:
#         Formatted number string with thousand separators
#     """
#     # Convert to string and reverse for easier processing
#     num_str = str(abs(number))
#     result = ""

#     for i, digit in enumerate(reversed(num_str)):
#         if i > 0 and i % 3 == 0:
#             result = separator + result
#         result = digit + result

#     # Handle negative numbers
#     if number < 0:
#         result = "-" + result

#     return result

# def _format_products(self, products, format_string=None):
#     """
#     Format products according to the specified format string.

#     Args:
#         products: List/recordset of product.product records
#         format_string: Custom format string (e.g., "- {product_name} just {product_price}")

#     Returns:
#         Formatted string with all products
#     """
#     if not products:
#         return ""

#     if not format_string:
#         # Default format with currency formatting
#         return "\n".join(
#             f"{product.name} - {self._format_price_with_currency(product)}"
#             for product in products
#         )

#     formatted_products = []
#     for product in products:
#         # Replace product placeholders in the format string
#         formatted_item = format_string
#         formatted_item = formatted_item.replace(
#             "{product_name}", product.name or ""
#         )

#         # Format price with currency
#         formatted_price = self._format_price_with_currency(product)
#         formatted_item = formatted_item.replace("{product_price}", formatted_price)

#         formatted_products.append(formatted_item)

#     return "\n".join(formatted_products)

# def _parse_template_expression(self, expression):
#     """
#     Parse complex template expressions like {products:product_item_format(- {product_name} just {product_price})}

#     Args:
#         expression: The full expression string

#     Returns:
#         dict with 'field', 'format_type', and 'format_string'
#     """
#     # Pattern to match: {field:format_type(format_string)}
#     pattern = r"\{(\w+):(\w+)\(([^)]+)\)\}"
#     match = re.match(pattern, expression)

#     if match:
#         return {
#             "field": match.group(1),
#             "format_type": match.group(2),
#             "format_string": match.group(3),
#         }

#     # Simple pattern: {field}
#     simple_pattern = r"\{(\w+)\}"
#     simple_match = re.match(simple_pattern, expression)
#     if simple_match:
#         return {
#             "field": simple_match.group(1),
#             "format_type": None,
#             "format_string": None,
#         }

#     return None

# def _find_template_expressions(self, template):
#     """
#     Find all template expressions in the message, handling nested braces properly.

#     Args:
#         template: The template string

#     Returns:
#         List of complete template expressions
#     """
#     expressions = []
#     i = 0
#     while i < len(template):
#         if template[i] == "{":
#             # Found start of expression, find the matching closing brace
#             brace_count = 1
#             start = i
#             i += 1

#             while i < len(template) and brace_count > 0:
#                 if template[i] == "{":
#                     brace_count += 1
#                 elif template[i] == "}":
#                     brace_count -= 1
#                 i += 1

#             if brace_count == 0:
#                 # Found complete expression
#                 expressions.append(template[start:i])
#             else:
#                 # Unclosed brace, skip
#                 break
#         else:
#             i += 1

#     return expressions

# def _render_message_template(self, template, customer, products):
#     """
#     Render the message template with customer and product data.

#     Args:
#         template: Message template string
#         customer: res.partner record
#         products: product.product recordset

#     Returns:
#         Rendered message string
#     """
#     message = template

#     # Find all template expressions using improved method
#     expressions = self._find_template_expressions(message)

#     _logger.info(f"Found template expressions: {expressions}")

#     for expression in expressions:
#         parsed = self._parse_template_expression(expression)
#         if not parsed:
#             _logger.warning(f"Could not parse expression: {expression}")
#             continue

#         field = parsed["field"]
#         format_type = parsed["format_type"]
#         format_string = parsed["format_string"]

#         _logger.info(
#             f"Parsed expression - Field: {field}, Format: {format_type}, Format String: {format_string}"
#         )

#         replacement = ""

#         if field == "customer_name":
#             replacement = customer.name or ""
#         elif field == "products":
#             if format_type == "product_item_format" and format_string:
#                 replacement = self._format_products(products, format_string)
#                 _logger.info(f"Generated product replacement: {replacement}")
#             else:
#                 replacement = self._format_products(products)

#         # Replace the expression with the computed value
#         message = message.replace(expression, replacement)
#         _logger.info(f"Replaced '{expression}' with: {replacement}")

#     return message
