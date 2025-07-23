# Smart Engagement - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you set up and run your first WhatsApp marketing campaign in just 5 minutes.

### Prerequisites

- WhatsApp API endpoint
- API access token
- At least one customer with a valid phone number
- One or more products in your catalog

---

## Step 1: Configure WhatsApp API (1 minute)

1. **Navigate to Configuration**

   - Go to: **Smart Engagement → Configuration**

2. **Enter API Details**

   ```
   Base URL: https://your-whatsapp-api.com
   Access Token: your_access_token_here
   Send Path: /send-message
   Health Check Path: /health
   ```

3. **Select Test Customer**

   - Choose a customer for testing messages

4. **Test Connection**
   - Click "Test Connection" button
   - Verify you see "Connection successful" message

---

## Step 2: Create Customer Segment (1 minute)

1. **Navigate to Segmentation**

   - Go to: **Smart Engagement → Customer Segmentations**

2. **Create New Segment**
   - Click "Create"
   - Name: "Test Segment"
   - Type: "Manually"
   - Select 2-3 customers with valid phone numbers
   - Save

---

## Step 3: Create Your First Campaign (2 minutes)

1. **Navigate to Campaigns**

   - Go to: **Smart Engagement → Campaigns**

2. **Create Campaign**

   - Click "Create"
   - Fill in details:
     ```
     Name: My First Campaign
     Type: Time Based
     End Date: Tomorrow
     Customer Segmentation: Test Segment
     Product Recommendation: Fixed Products
     ```

3. **Select Products**

   - Choose 2-3 products from your catalog

4. **Create Message Template**

   ```
   Hi {customer_name}!

   Check out these amazing products:

   {products:product_item_format(🛍️ {product_name} - {product_price}
   📦 SKU: {product_code}

   )}

   Reply to this message to order!
   ```

5. **Set Timing**
   - Initial Send: "Now"
   - Recurring: Leave unchecked
   - Save the campaign

---

## Step 4: Test Your Campaign (1 minute)

1. **Preview Messages**

   - Click "Preview Messages" button
   - Review the generated messages
   - Verify customer names and product details appear correctly

2. **Send Test Message**
   - Click "Test" button
   - Check that test message is sent to your test customer
   - Verify the message appears in WhatsApp

---

## Step 5: Launch Your Campaign (30 seconds)

1. **Start Campaign**

   - Click "Run" button
   - Campaign status changes to "Running"

2. **Monitor Progress**
   - Go to: **Smart Engagement → WhatsApp API Logs**
   - Check for successful message deliveries
   - Monitor for any errors

---

## 🎉 Congratulations!

You've successfully created and launched your first WhatsApp marketing campaign!

### What's Next?

1. **Monitor Performance**

   - Check API logs regularly
   - Review success rates
   - Monitor customer responses

2. **Create More Segments**

   - Try rule-based segmentation
   - Target specific customer groups

3. **Advanced Templates**

   - Experiment with different template formats
   - Add more product information
   - Include promotional offers

4. **Recurring Campaigns**
   - Set up weekly newsletters
   - Create monthly promotions
   - Automate customer follow-ups

---

## 🆘 Need Help?

### Common Issues

**Cannot Create Campaign?**

- Check if you have created at least one customer segment
- Navigate to **Smart Engagement → Customer Segmentations**
- Create a segment before creating campaigns

**Connection Failed?**

- Check your API endpoint URL
- Verify your access token
- Ensure your API service is running

**Messages Not Sending?**

- Verify customer phone numbers
- Check API logs for errors
- Ensure customers have WhatsApp

**Template Not Working?**

- Use the Preview function
- Check placeholder syntax
- Verify customer/product data exists

### Get Support

- Check the comprehensive User Guide
- Review API logs for detailed errors
- Test with a single customer first
- Contact support if issues persist

---

## 📚 Additional Resources

- **Full User Guide**: Complete documentation with all features
- **Features Summary**: Overview of all capabilities
- **Templating Examples**: Advanced template examples
- **Utils Guide**: Technical implementation details

---

_Ready to scale your WhatsApp marketing? Explore the full User Guide for advanced features and best practices!_
