# Webhook Integration Guide

This guide explains how to use the Smart Engagement webhook integration with **enhanced weighted duplicate detection** to sync contact, product, category, and sales order data from external systems.

## Overview

The Smart Engagement module provides REST API webhook endpoints with advanced smart synchronization:
- **Contact Data**: Create/update contact records with weighted duplicate detection (90% confidence threshold)
- **Product Categories**: Manage product category hierarchy  
- **Product Data**: Create/update products/services
- **Sales Orders**: Create confirmed sales orders with automatic invoicing

## ✨ Key Features

- **🎯 Weighted Duplicate Detection**: Advanced scoring system (Name 40%, Phone 25%, Mobile 25%, Email 10%)
- **🔍 All Contact Search**: Checks ALL contacts, not just customers with orders
- **📊 Built-in Logging**: Uses Odoo's native webhook logging with detailed tracking
- **🚀 Smart Sync**: Intelligent data normalization and processing
- **💎 High Confidence Matching**: 90% confidence threshold for auto-merge decisions

## Authentication

Webhooks require Odoo API authentication. You can use either:
- API Keys (recommended)
- Username/Password authentication

## Webhook Endpoints

### Base URL
```
https://your-odoo-instance.com/web/dataset/call_kw
```

### 1. Contact Data Webhook

**Server Action ID**: `smart_engagement.action_webhook_contact_smart_sync`

**Payload Format**:
```json
{
  "external_id": "CONTACT001",   // required - external system ID
  "patient_id": "PAT001",        // backward compatibility - same as external_id
  "name": "John Doe",            // required - full name
  "phone": "628123456789",       // Phone format (auto-normalized)
  "mobile": "628987654321",      // Mobile format (auto-normalized)
  "email": "john@example.com",
  "street": "Jl. Sudirman No. 123",
  "city": "Jakarta",
  "state_name": "DKI Jakarta",
  "date_of_birth": "1990-01-15"  // YYYY-MM-DD format
}
```

**🚀 Enhanced Features**:
- **Weighted Duplicate Detection**: Advanced scoring system with 90% confidence threshold
- **All Contact Search**: Searches ALL contacts (leads, prospects, customers)
- **Smart Phone Normalization**: Handles multiple formats (08xxx → 628xxx, +62xxx → 628xxx)
- **Intelligent Name Matching**: Title case conversion and fuzzy matching
- **Duplicate Score Logging**: Returns confidence score for transparency

**Example cURL**:
```bash
curl -X POST https://your-odoo-instance.com/web/dataset/call_kw \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "model": "ir.actions.server",
      "method": "run",
      "args": [["smart_engagement.action_webhook_contact_smart_sync"]],
      "kwargs": {
        "context": {
          "payload": {
            "external_id": "CONTACT001",
            "name": "John Doe",
            "phone": "08123456789",
            "email": "john@example.com"
          }
        }
      }
    }
  }'
```

### 2. Product Category Webhook

**Server Action ID**: `smart_engagement.action_webhook_category_smart_sync`

**Payload Format**:
```json
{
  "name": "Services",                    // required - category name
  "parent_name": "Main Categories"       // optional - creates parent if not exists
}
```

**Example**:
```json
{
  "name": "Premium Services",
  "parent_name": "Services"
}
```

### 3. Product Data Webhook

**Server Action ID**: `smart_engagement.action_webhook_product_smart_sync`

**Payload Format**:
```json
{
  "name": "Professional Service",    // required - product name
  "default_code": "SRV-001",         // SKU/internal reference
  "barcode": "1234567890123",         // barcode (optional)
  "list_price": 1500000,             // price
  "type": "service",                  // product type (service, consu, product)
  "categ_name": "Premium Services"    // category name
}
```

**🚀 Smart Features**:
- **Auto Service Type**: Defaults to service type for business services
- **Category Auto-Creation**: Creates category hierarchy if not exists
- **Smart Updates**: Updates existing products by SKU or barcode
- **Price Management**: Handles pricing and product configuration

### 4. Sales Order Webhook

**Server Action ID**: `smart_engagement.action_webhook_sale_order_smart_sync`

**Payload Format**:
```json
{
  "external_id": "CONTACT001",      // required - customer external ID
  "patient_id": "PAT001",           // backward compatibility - same as external_id
  "name": "ORDER-2024-001",         // order reference
  "customer_name": "John Doe",      // fallback for smart contact matching
  "date_order": "2024-01-15 10:30:00",  // order datetime
  "amount_total": 3500000,          // total amount
  "source": "AGR-123",              // required - source/agreement ID
  "order_line": [
    {
      "product_code": "SRV-001",    // product SKU
      "product_name": "Professional Service",  // fallback name
      "product_uom_qty": 1,         // quantity
      "price_unit": 1500000,        // unit price
      "price_subtotal": 1500000     // line total
    },
    {
      "product_code": "SRV-002",
      "product_name": "Premium Service",
      "product_uom_qty": 2,
      "price_unit": 1000000,
      "price_subtotal": 2000000
    }
  ]
}
```

**🚀 Smart Features**:
- **Smart Customer Lookup**: Uses weighted scoring if external_id not found
- **Auto Order Confirmation**: Automatically confirms and processes orders
- **Invoice & Payment**: Creates invoice and registers payment automatically
- **Product Fallback**: Finds products by SKU or name with intelligent matching

## Webhook Response Format

### Success Response
```json
{
  "success": true,
  "action": "created",      // or "updated"
  "contact_id": 123,        // record ID
  "contact_name": "John Doe",
  "duplicate_score": 0.95   // confidence score (0.0-1.0)
}
```

### Error Response
```json
{
  "success": false,
  "error": "external_id or patient_id is required"
}
```

## 🎯 Advanced Weighted Duplicate Detection

The contact webhook uses **sophisticated weighted scoring** for intelligent duplicate detection:

### Scoring System
- **Name Similarity**: 40% weight (most important for identity)
- **Phone Match**: 25% weight (very reliable identifier)
- **Mobile Match**: 25% weight (very reliable identifier)  
- **Email Match**: 10% weight (can change, less reliable)

### Confidence Thresholds
- **≥90% Score**: Auto-merge (high confidence)
- **70-89% Score**: Could add manual review (future feature)
- **<70% Score**: Create new contact

### Smart Matching Examples
```javascript
// Scenario 1: Perfect match (95% confidence)
"John Doe" + "628123456789" → Auto-merge ✅

// Scenario 2: Similar name + exact phone (92% confidence)  
"Jon Doe" vs "John Doe" + same phone → Auto-merge ✅

// Scenario 3: Just name similarity (40% confidence)
"John Doe" + no phone/email → Create new contact ✅

// Scenario 4: Different name + same phone (85% confidence)
"John" vs "Jonathan" + exact phone → Auto-merge ✅
```

### Key Improvements
- **🔍 All Contact Search**: Checks ALL contacts (leads, prospects, customers)
- **📊 Transparent Scoring**: Returns exact confidence score in response
- **🎯 Higher Accuracy**: Weighted approach vs simple threshold
- **🚀 Better Performance**: Optimized search and scoring algorithms

## Data Processing Order

For initial data import, process in this order:

1. **Product Categories** (parent categories first)
2. **Products** (services/items)
3. **Contacts** (customers/leads)
4. **Sales Orders** (requires contacts and products)

## 📊 Monitoring & Built-in Logging

**Enhanced logging with Odoo's native webhook system:**

### Webhook Logs Location
- **Settings → Technical → Automation → Base Automation**
- **Smart Engagement → Campaigns → WhatsApp API Logs** (application logs)

### Built-in Log Features
- ✅ **Automatic Logging**: Enabled via `log_webhook_calls: True`
- ✅ **Detailed Tracking**: Full request/response data
- ✅ **Error Capture**: Complete error traces and stack traces
- ✅ **Performance Metrics**: Execution time and resource usage
- ✅ **Success/Failure Status**: Clear status indicators

### Log Information Includes
- 🕐 **Timestamp**: Precise execution time
- 🎯 **Webhook Type**: Contact, Product, Category, Sales Order
- 📝 **Full Payload**: Complete JSON request data
- ✅ **Success/Error Status**: Clear result indicators
- 📊 **Duplicate Score**: Confidence score for contact matching
- 🔍 **Execution Details**: Processing time and resource usage

## 🚀 Best Practices

1. **🔄 Batch Processing**: Send multiple records in separate API calls for optimal performance
2. **🛡️ Error Handling**: Implement retry logic with exponential backoff for failed webhooks
3. **✅ Data Validation**: Validate required fields (`external_id`, `name`) before sending
4. **📱 Phone Format**: Use any format - system auto-normalizes (08xxx, +62xxx, 628xxx)
5. **🎯 Consistent IDs**: Use consistent `external_id` across systems for best duplicate detection
6. **📊 Monitor Scores**: Track `duplicate_score` in responses to tune confidence thresholds
7. **🏗️ Process Order**: Follow data processing order (categories → products → contacts → orders)

## 🧪 Testing Webhooks

### Using cURL
Use the provided cURL examples with your authentication:

```bash
# Test authentication first
curl -X POST https://your-odoo-instance.com/web/session/authenticate \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","params":{"db":"your-db","login":"admin","password":"admin"}}'
```

### Testing Checklist
1. ✅ Set proper authentication headers
2. ✅ Use correct server action IDs (`*_smart_sync`)
3. ✅ Include payload in context object
4. ✅ Check built-in webhook logs for results
5. ✅ Verify `duplicate_score` in response for contacts

## 🔧 Common Issues & Solutions

### Contact Not Found in Sales Orders
**Problem**: `Customer not found with external_id: CONTACT001`
**Solutions**:
- ✅ Ensure contact webhook was called first with same `external_id`
- ✅ Check `external_id` matches exactly (case-sensitive)
- ✅ Verify contact creation was successful via logs
- ✅ Use `customer_name` as fallback for smart matching

### Product Not Found in Orders
**Problem**: `Product not found: SRV-001`
**Solutions**:
- ✅ Create product via product webhook first
- ✅ Verify `product_code` (SKU) matches exactly
- ✅ Ensure product category exists
- ✅ Use `product_name` as fallback for smart matching

### Low Duplicate Detection Scores
**Problem**: Contacts creating duplicates with low confidence scores
**Solutions**:
- ✅ Ensure phone numbers are consistently formatted
- ✅ Use full names instead of abbreviations
- ✅ Include email addresses when available
- ✅ Monitor duplicate scores and adjust data quality

### Authentication Issues
**Problem**: Webhook calls return authentication errors
**Solutions**:
- ✅ Verify API key or credentials are correct
- ✅ Check user has proper permissions for webhook execution
- ✅ Ensure database name is correct in requests
- ✅ Test authentication separately before webhook calls

## 🎯 Performance Tips

- **Parallel Processing**: Send different webhook types concurrently
- **Smart Batching**: Group related records (same customer, same category)
- **Error Recovery**: Implement idempotent operations for retry safety
- **Monitoring**: Track response times and success rates
- **Caching**: Cache authentication tokens to reduce overhead