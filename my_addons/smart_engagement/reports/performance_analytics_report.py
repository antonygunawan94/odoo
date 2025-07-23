# -*- coding: utf-8 -*-

import logging
from collections import defaultdict

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PerformanceAnalyticsReport(models.Model):
    _name = "smart_engagement.performance_analytics_report"
    _description = "Performance Analytics Report"
    _rec_name = "display_name"
    _order = "order_date desc"

    # Display name for record identification
    display_name = fields.Char(
        "Display Name", compute="_compute_display_name", store=True
    )

    # === PRIMARY KEYS & IDENTIFIERS ===
    order_id = fields.Many2one("sale.order", "Order", readonly=True, required=True)

    # === SPENDING ANALYSIS ===
    spending_tier_id = fields.Many2one(
        "smart_engagement.customer_spending_tier_config",
        "Spending Tier Config",
        readonly=True,
    )
    spending_tier_code = fields.Char("Spending Tier Code", readonly=True)
    spending_tier_name = fields.Char("Spending Tier Name", readonly=True)
    spending_tier_display = fields.Char(
        "Spending Tier", readonly=True, help="Tier name with spending range"
    )

    # === PRODUCT DIMENSIONS ===
    product_id = fields.Many2one("product.product", "Product", readonly=True)
    product_name = fields.Char("Product Name", readonly=True)
    product_category_id = fields.Many2one(
        "product.category", "Product Category", readonly=True
    )
    category_name = fields.Char("Category Name", readonly=True)

    # === CUSTOMER DIMENSIONS ===
    partner_id = fields.Many2one(
        "res.partner", "Customer", readonly=True, required=True
    )
    customer_name = fields.Char("Customer Name", readonly=True)
    customer_age_group = fields.Char("Customer Age Group", readonly=True)
    customer_country_id = fields.Many2one(
        "res.country", "Customer Country", readonly=True
    )
    customer_state_id = fields.Many2one(
        "res.country.state", "Customer State", readonly=True
    )

    # === CUSTOMER ACQUISITION SOURCE ===
    customer_acquisition_source_id = fields.Many2one(
        "smart_engagement.customer_acquisition_source_config",
        "Customer Acquisition Source",
        readonly=True,
    )
    customer_acquisition_source_name = fields.Char(
        "Acquisition Source Name",
        readonly=True,
        help="IG, TIKTOK, LEWAT DEPAN ELLA, TEMAN/KELUARGA",
    )

    # === CUSTOMER SEGMENTATION ===
    is_new_customer = fields.Boolean("Is New Customer", readonly=True)
    customer_type = fields.Selection(
        [("new", "New Customer"), ("existing", "Existing Customer")],
        "Customer Type",
        readonly=True,
    )

    # === SALES DIMENSIONS ===
    salesperson_id = fields.Many2one("res.users", "Salesperson", readonly=True)
    sales_team_id = fields.Many2one("crm.team", "Sales Team", readonly=True)
    order_date = fields.Date("Order Date", readonly=True, required=True)
    order_month = fields.Char("Order Month", readonly=True)
    order_quarter = fields.Char("Order Quarter", readonly=True)
    order_year = fields.Integer("Order Year", readonly=True, aggregator=None)

    # === SALES SOURCE ===
    sales_source_id = fields.Many2one("utm.source", "Sales Source", readonly=True)
    sales_source_name = fields.Char(
        "Sales Source Name", readonly=True, help="PRODUK, TREATMENT CLINIC, REDEEM"
    )

    # === RAW MEASURES (from database) ===
    units_sold = fields.Integer("Units Sold", readonly=True)
    revenue = fields.Float("Revenue", readonly=True)

    # === AGGREGATION FIELDS ===
    # Each field has separate compute method for better debugging and control
    avg_order_value = fields.Float(
        "Avg Order Value",
        readonly=True,
        help="Average Order Value - calculated via read_group override",
        aggregator="avg",
    )
    order_count = fields.Float(
        "# Orders",
        compute="_compute_order_count",
        store=True,
        help="Fractional order count - each order contributes 1.0 total across all its lines",
        aggregator="sum",
    )
    customer_count = fields.Integer(
        "# Customers",
        readonly=True,
        help="Unique customer count - calculated via read_group override",
        aggregator="sum",
    )


    @api.depends("order_id")
    def _compute_order_count(self):
        """Compute fractional order count - each order line gets 1/total_lines of the order"""
        for record in self:
            if not record.order_id:
                record.order_count = 0.0
                continue
                
            # Count ALL lines for this order (across all categories)
            total_order_lines = self.search_count([
                ('order_id', '=', record.order_id.id)
            ])
            
            if total_order_lines > 0:
                # Fractional order count: 1 order divided by total lines
                # This ensures each order contributes exactly 1.0 total
                record.order_count = 1.0 / total_order_lines
            else:
                record.order_count = 1.0


    @api.model
    def init(self):
        """Initialize report data on module install/upgrade or when manually called"""
        self.refresh_data()

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        _logger.info(f"READ_GROUP called with fields: {fields}, groupby: {groupby}")
        """Override read_group to handle unique customer counting"""
        # Get the standard read_group result first
        result = super().read_group(
            domain, fields, groupby, offset, limit, orderby, lazy
        )

        # Process customer_count if requested
        customer_count_requested = any('customer_count' in field for field in fields)
        if customer_count_requested:
            _logger.info("Processing customer_count in read_group")
            
            # Check if we're grouping by customer_name - if so, customer_count should be 1 per group
            is_customer_level = 'customer_name' in str(groupby) if groupby else False
            _logger.info(f"Is customer level grouping: {is_customer_level}")
            
            for i, group in enumerate(result):
                if "__domain" in group:
                    if is_customer_level:
                        # At customer level, each group represents 1 customer
                        group["customer_count"] = 1
                        _logger.info(f"Group {i} (customer level): customer_count = 1")
                    else:
                        # At higher levels, count unique customers
                        group_domain = group["__domain"]
                        records_in_group = self.search(group_domain)
                        unique_customers = records_in_group.mapped("partner_id")
                        unique_count = len(unique_customers)
                        group["customer_count"] = unique_count
                        _logger.info(f"Group {i} (higher level): {unique_count} unique customers")
                else:
                    group["customer_count"] = 0

        # Process avg_order_value if requested  
        aov_requested = any('avg_order_value' in field for field in fields)
        if aov_requested:
            _logger.info("Processing avg_order_value in read_group")
            
            for i, group in enumerate(result):
                if "__domain" in group:
                    revenue = group.get('revenue', 0)
                    order_count = group.get('order_count', 0)
                    
                    if order_count and order_count > 0:
                        group["avg_order_value"] = revenue / order_count
                        _logger.info(f"Group {i}: AOV = {revenue} / {order_count} = {group['avg_order_value']}")
                    else:
                        group["avg_order_value"] = 0
                        _logger.info(f"Group {i}: AOV = 0 (no orders)")
                else:
                    group["avg_order_value"] = 0

        return result

    @api.depends("order_id", "customer_name", "category_name")
    def _compute_display_name(self):
        """Compute display name for better record identification"""
        for record in self:
            parts = []
            if record.order_id:
                parts.append(f"Order {record.order_id.name}")
            if record.customer_name:
                parts.append(record.customer_name)
            if record.category_name:
                parts.append(record.category_name)
            record.display_name = " - ".join(parts) or f"Record {record.id}"

    @api.model
    def get_spending_tier_for_amount(self, amount):
        """Helper method to get spending tier for a given amount"""
        tiers = self.env[
            "smart_engagement.customer_spending_tier_config"
        ].search([("active", "=", True)], order="min_spending_amount desc")

        for tier in tiers:
            if amount >= tier.min_spending_amount:
                if not tier.max_spending_amount or amount <= tier.max_spending_amount:
                    return {
                        "id": tier.id,
                        "code": tier.tier_code,
                        "name": tier.display_name,
                        "display": self._format_tier_display(tier),
                    }

        return {
            "id": False,
            "code": "UNCLASSIFIED",
            "name": "Unclassified",
            "display": "Unclassified",
        }

    def _format_tier_display(self, tier):
        """Format tier display with spending range"""
        if not tier.max_spending_amount:
            return f"{tier.display_name} (> Rp {tier.min_spending_amount:,.0f})"
        else:
            return f"{tier.display_name} (Rp {tier.min_spending_amount:,.0f} - {tier.max_spending_amount:,.0f})"

    @api.model
    def get_business_category(self, category):
        """Get business-level category (PRODUK/JASA) for a product category"""
        if not category:
            return "UNCATEGORIZED"

        # Direct children of "All" (id=1) are business-level categories
        if category.parent_id and category.parent_id.id == 1:
            return category.name

        # Categories without parent map to themselves
        if not category.parent_id:
            return category.name

        # Deep nested categories - find business-level parent
        parent_path_parts = category.parent_path.strip("/").split("/")
        if len(parent_path_parts) >= 2:
            business_category_id = int(parent_path_parts[1])
            business_category = self.env["product.category"].browse(
                business_category_id
            )
            return (
                business_category.name
                if business_category.exists()
                else "UNCATEGORIZED"
            )

        return "UNCATEGORIZED"

    @api.model
    def refresh_data(self):
        """
        Refresh report data by rebuilding from source tables
        This method fetches data using standard ORM queries
        """
        # Clear existing data
        self.search([]).unlink()

        # Get all confirmed/done orders with revenue (V2 Enhanced: matches V1 filtering)
        orders = self.env["sale.order"].search([
            ("state", "in", ["sale", "done"]),
            ("amount_total", ">", 0),  # Only revenue-generating orders
            ("partner_id.customer_rank", ">", 0),  # Only customers
            ("partner_id.is_company", "=", False),  # No companies
        ])

        # Calculate customer lifetime spending for correct tier assignment
        # (Already filtered to revenue-generating orders only)
        customer_spending = {}
        for order in orders:
            partner_id = order.partner_id.id
            if partner_id not in customer_spending:
                customer_spending[partner_id] = 0
            customer_spending[partner_id] += order.amount_total

        records_to_create = []

        for order in orders:
            # Get spending tier based on customer's TOTAL lifetime spending (not individual order)
            customer_total_spending = customer_spending[order.partner_id.id]
            tier_info = self.get_spending_tier_for_amount(customer_total_spending)

            # Get customer info
            partner = order.partner_id

            # Get acquisition source
            acq_source = partner.acquisition_source_id
            acq_source_name = acq_source.display_name if acq_source else "Unknown"

            # Create one record per order line for full product flexibility
            for line in order.order_line:
                if not line.product_id:
                    continue
                
                # Get product info
                product = line.product_id
                product_template = product.product_tmpl_id
                product_category = product_template.categ_id
                business_category = self.get_business_category(product_category)

                # Line-level metrics
                total_qty = line.product_uom_qty
                total_revenue = line.price_subtotal

                record_data = {
                    # IDs
                    "order_id": order.id,
                    # Spending Analysis
                    "spending_tier_id": tier_info["id"],
                    "spending_tier_code": tier_info["code"],
                    "spending_tier_name": tier_info["name"],
                    "spending_tier_display": tier_info["display"],
                    # Product Dimensions
                    "product_id": product.id,
                    "product_name": product_template.name,
                    "product_category_id": product_category.id if product_category else False,
                    "category_name": business_category,
                    # Customer Dimensions
                    "partner_id": partner.id,
                    "customer_name": partner.name,
                    "customer_age_group": getattr(partner, "customer_age_group", False)
                    or "Unknown",
                    "customer_country_id": (
                        partner.country_id.id if partner.country_id else False
                    ),
                    "customer_state_id": (
                        partner.state_id.id if partner.state_id else False
                    ),
                    # Customer Acquisition
                    "customer_acquisition_source_id": (
                        acq_source.id if acq_source else False
                    ),
                    "customer_acquisition_source_name": acq_source_name,
                    # Customer Segmentation
                    "is_new_customer": getattr(partner, "is_new_customer", False),
                    "customer_type": (
                        "new"
                        if getattr(partner, "is_new_customer", False)
                        else "existing"
                    ),
                    # Sales Dimensions
                    "salesperson_id": order.user_id.id if order.user_id else False,
                    "sales_team_id": order.team_id.id if order.team_id else False,
                    "order_date": order.date_order.date(),
                    "order_month": order.date_order.strftime("%Y-%m"),
                    "order_quarter": f"Q{(order.date_order.month - 1) // 3 + 1}-{order.date_order.year}",
                    "order_year": order.date_order.year,
                    # Sales Source
                    "sales_source_id": order.source_id.id if order.source_id else False,
                    "sales_source_name": (
                        order.source_id.name if order.source_id else "Unclassified"
                    ),
                    # Raw Measures
                    "units_sold": int(total_qty),
                    "revenue": total_revenue,  # Category-specific revenue
                    # === AGGREGATION FIELDS ===
                    # order_count: computed via _compute_order_count (fractional within same category)
                    # customer_count: handled via read_group override for unique counting
                    # avg_order_value: calculated via read_group override (revenue / order_count)
                    "customer_count": 1,  # Default to 1, read_group will correct for unique counting
                }

                records_to_create.append(record_data)

        # Batch create all records
        if records_to_create:
            created_records = self.create(records_to_create)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Performance Analytics Report V2 refreshed successfully! Created {len(records_to_create)} records.",
                "type": "success",
                "sticky": False,
            },
        }
