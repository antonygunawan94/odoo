# Smart Engagement - Message Templating Guide

## Overview

The new templating system supports advanced formatting for personalized WhatsApp messages.

## Basic Usage

### Simple Templates

```
Hi {customer_name}! We have new products for you.
```

### With Basic Product List

```
Hello {customer_name}!

Check out these products:
{products}
```

**Output:**

```
Hello John Doe!

Check out these products:
iPhone 15 - 999.0
Samsung Galaxy - 799.0
Google Pixel - 699.0
```

## Advanced Formatting

### Custom Product Format

```
Dear {customer_name},

Here are our top recommendations:
{products:product_item_format(🛍️ {product_name} - Only ${product_price}!)}

Happy shopping!
```

**Output:**

```
Dear John Doe,

Here are our top recommendations:
🛍️ iPhone 15 - Only $999.0!
🛍️ Samsung Galaxy - Only $799.0!
🛍️ Google Pixel - Only $699.0!

Happy shopping!
```

### Detailed Product Information

```
Hi {customer_name}!

Based on your preferences in {customer_email}, we suggest:

{products:product_item_format(✅ {product_name}
   Category: {product_category}
   Price: ${product_price}
   Product Code: {product_code}

)}

Questions? Call us at {customer_phone}
```

**Output:**

```
Hi John Doe!

Based on your preferences in john@example.com, we suggest:

✅ iPhone 15
   Category: Smartphones
   Price: $999.0
   Product Code: IPH15

✅ Samsung Galaxy
   Category: Smartphones
   Price: $799.0
   Product Code: SAM001

Questions? Call us at +1234567890
```

## Available Placeholders

### Customer Information

- `{customer_name}` - Customer's full name
- `{customer_email}` - Customer's email address
- `{customer_phone}` - Customer's phone number
- `{customer_mobile}` - Customer's mobile number

### Product Information (within product_item_format)

- `{product_name}` - Product name
- `{product_price}` - Product price
- `{product_code}` - Product internal reference/SKU
- `{product_category}` - Product category name

### Product List Formats

- `{products}` - Default format (Name - Price)
- `{products:product_item_format(CUSTOM_FORMAT)}` - Custom format

## Real-World Examples

### E-commerce Promotion

```
🎉 Special offer for {customer_name}!

Limited time deals:
{products:product_item_format(📱 {product_name}
💰 Was: ${product_price} → Now: Special Price!
📦 Code: {product_code})}

Order now by replying to {customer_mobile}!
```

### Service Business

```
Hello {customer_name},

We recommend these services:
{products:product_item_format(⭐ {product_name} - {product_category}
   Starting at ${product_price})}

Contact us for booking!
```

### Inventory Update

```
Hi {customer_name}!

New arrivals in stock:
{products:product_item_format(🆕 {product_name} ({product_code})
Price: ${product_price} | Category: {product_category}
)}

Visit our store or call {customer_phone}
```

## Technical Implementation

The templating system uses regex parsing to:

1. Identify template expressions like `{field}` or `{field:format_type(format_string)}`
2. Parse complex nested formats within product listings
3. Replace placeholders with actual data
4. Support multiple customer and product variables

This allows for highly personalized and flexible message templates while maintaining clean, readable syntax.
