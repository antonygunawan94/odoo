import logging
from datetime import datetime, timedelta
from email.policy import default

import requests

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

from ..utils import MessageTemplateRenderer, show_notification, validate_phone_number

_logger = logging.getLogger(__name__)


class Campaign(models.Model):
    _name = "wa_marketing_automation.campaign"
    _description = "Campaign"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_names_search = ["name", "customer_segmentation_id", "state"]

    name = fields.Char(string="Name", required=True, tracking=True)

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("running", "Running"),
            ("finished", "Finished"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="draft",
        tracking=True,
    )

    customer_segmentation_id = fields.Many2one(
        "wa_marketing_automation.customer_segmentation",
        string="Who is the target audience?",
        required=True,
        tracking=True,
    )
    assigned_to = fields.Many2one(
        "res.users",
        string="Who is responsible for this campaign?",
        default=lambda self: self.env.user,
        tracking=True,
    )
    type = fields.Selection(
        [
            ("time_based", "Time Based"),
            ("forever", "Forever"),
        ],
        string="What type of campaign is this?",
        default="time_based",
        tracking=True,
    )
    end_date = fields.Datetime(string="End Date", tracking=True)

    # Product Recommendation
    product_recommendation_type = fields.Selection(
        [
            ("none", "None"),
            ("fixed_products", "Fixed Products"),
            ("rules", "Rules"),
        ],
        string="Recommend Products based on?",
        default="none",
        tracking=True,
    )
    product_recommendation_fixed_products = fields.Many2many(
        "product.product",
        string="Recommended Products",
        tracking=True,
    )
    product_recommendation_rules = fields.Char(
        string="Rules", default="[]", tracking=True
    )

    # Message Template
    message_template = fields.Text(
        string="Message Template",
        required=True,
        tracking=True,
        help="""Use placeholders to personalize your messages:

Basic placeholders:
• {customer_name} - Customer's name

Product placeholders:
• {products} - Default product format (Name - Price)
• {products:product_item_format(CUSTOM_FORMAT)} - Custom product format

Example templates:
1. Simple: "Hi {customer_name}! Check out these products: {products}"

2. Custom format with newlines:
"Hello {customer_name}! Here are our recommendations:

{products:product_item_format(🛍️ {product_name}
💰 Price: {product_price}
📦 Code: {product_code}
)}"

3. Numbered list format:
"{products:product_item_format({product_number}. {product_name} - {product_price})}"

Available product format variables:
• {product_name} - Product name
• {product_price} - Formatted price with currency
• {product_code} / {product_sku} - Product code/SKU
• {product_description} - Product description
• {product_number} / {product_index} - Product number in list (1, 2, 3...)

Formatting tips:
• Use \\n in format strings for explicit newlines
• Products with internal newlines are separated by double newlines
• Excessive whitespace is automatically cleaned up
""",
    )
    message_initial_send_type = fields.Selection(
        [
            ("now", "Now"),
            ("specific_date", "Specific Date"),
            ("after_x_minutes", "After X Minutes"),
            ("after_x_hours", "After X Hours"),
            ("after_x_days", "After X Days"),
        ],
        string="When should we send the first message?",
        default="now",
        tracking=True,
    )
    message_initial_send_specific_date = fields.Datetime(
        string="Specific Date", tracking=True
    )
    message_initial_send_after_x_minutes = fields.Integer(
        string="After X Minutes", tracking=True
    )
    message_initial_send_after_x_hours = fields.Integer(
        string="After X Hours", tracking=True
    )
    message_initial_send_after_x_days = fields.Integer(
        string="After X Days", tracking=True
    )

    message_should_send_repeat = fields.Boolean(
        string="Should we repeat sending the message?", default=False, tracking=True
    )

    # Repeat Send
    message_send_repeat_trigger_type = fields.Selection(
        [
            ("every_x_days", "Every X Days"),
            ("every_x_weeks", "Every X Weeks"),
        ],
        string="How often?",
        default="every_x_days",
        tracking=True,
    )
    message_send_repeat_trigger_days = fields.Integer(
        string="Every X Days", tracking=True
    )
    message_send_repeat_trigger_weeks = fields.Integer(
        string="Every X Weeks", tracking=True
    )
    message_send_repeat_trigger_time = fields.Float(
        string="At what time of day should we send messages?", tracking=True
    )

    def _format_datetime_for_user(self, utc_datetime):
        """Convert UTC datetime to user's timezone and format for display"""
        if not utc_datetime:
            return ""

        try:
            # Try to get user's timezone from multiple sources
            user_tz = None

            # Method 1: Get from current user
            if self.env.user and self.env.user.tz:
                user_tz = self.env.user.tz

            # Method 2: Get from context
            elif self.env.context.get("tz"):
                user_tz = self.env.context.get("tz")

            # Method 3: Use fields.Datetime.context_timestamp (preferred method)
            if user_tz or hasattr(self, "env"):
                try:
                    local_datetime = fields.Datetime.context_timestamp(
                        self, utc_datetime
                    )
                    return local_datetime.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    # Fallback if context_timestamp fails
                    pass

            # Method 4: Manual conversion using pytz if available
            if user_tz:
                try:
                    import pytz

                    utc_tz = pytz.UTC
                    user_timezone = pytz.timezone(user_tz)

                    # Ensure datetime is timezone-aware
                    if utc_datetime.tzinfo is None:
                        utc_datetime = utc_tz.localize(utc_datetime)

                    local_datetime = utc_datetime.astimezone(user_timezone)
                    return local_datetime.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass

            # Fallback: Return UTC time with timezone indicator
            return utc_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

        except Exception:
            # Last resort fallback
            return (
                utc_datetime.strftime("%Y-%m-%d %H:%M:%S UTC") if utc_datetime else ""
            )

    @api.constrains(
        "message_initial_send_after_x_minutes",
        "message_initial_send_after_x_hours",
        "message_initial_send_after_x_days",
        "message_send_repeat_trigger_days",
        "message_send_repeat_trigger_weeks",
        "message_send_repeat_trigger_time",
        "message_should_send_repeat",
        "message_initial_send_type",
        "message_send_repeat_trigger_type",
    )
    def _check_trigger_values(self):
        """Validate trigger values are positive and within reasonable ranges"""
        for record in self:
            # Check initial send trigger values with reasonable upper bounds
            if record.message_initial_send_type == "after_x_minutes":
                if not record.message_initial_send_after_x_minutes:
                    raise ValidationError(_("Trigger minutes must be specified"))
                if record.message_initial_send_after_x_minutes < 1:
                    raise ValidationError(_("Trigger minutes must be at least 1"))
                if record.message_initial_send_after_x_minutes > 1440:  # 24 hours
                    raise ValidationError(
                        _("Trigger minutes cannot exceed 1440 (24 hours)")
                    )

            if record.message_initial_send_type == "after_x_hours":
                if not record.message_initial_send_after_x_hours:
                    raise ValidationError(_("Trigger hours must be specified"))
                if record.message_initial_send_after_x_hours < 1:
                    raise ValidationError(_("Trigger hours must be at least 1"))
                if record.message_initial_send_after_x_hours > 8760:  # 1 year
                    raise ValidationError(
                        _("Trigger hours cannot exceed 8760 (1 year)")
                    )

            if record.message_initial_send_type == "after_x_days":
                if not record.message_initial_send_after_x_days:
                    raise ValidationError(_("Trigger days must be specified"))
                if record.message_initial_send_after_x_days < 1:
                    raise ValidationError(_("Trigger days must be at least 1"))
                if record.message_initial_send_after_x_days > 365:  # 1 year
                    raise ValidationError(_("Trigger days cannot exceed 365 (1 year)"))

            # Check repeat trigger values only when repeat is enabled
            if record.message_should_send_repeat:
                if record.message_send_repeat_trigger_type == "every_x_days":
                    if not record.message_send_repeat_trigger_days:
                        raise ValidationError(
                            _("Repeat days must be specified when repeat is enabled")
                        )
                    if record.message_send_repeat_trigger_days < 1:
                        raise ValidationError(_("Repeat days must be at least 1"))
                    if record.message_send_repeat_trigger_days > 365:  # 1 year
                        raise ValidationError(_("Repeat days cannot exceed 365"))

                if record.message_send_repeat_trigger_type == "every_x_weeks":
                    if not record.message_send_repeat_trigger_weeks:
                        raise ValidationError(
                            _("Repeat weeks must be specified when repeat is enabled")
                        )
                    if record.message_send_repeat_trigger_weeks < 1:
                        raise ValidationError(_("Repeat weeks must be at least 1"))
                    if record.message_send_repeat_trigger_weeks > 52:  # 1 year
                        raise ValidationError(_("Repeat weeks cannot exceed 52"))

                # Validate time of day format (float_time widget: HH.MM format)
                if record.message_send_repeat_trigger_time is not False:
                    time_val = record.message_send_repeat_trigger_time
                    if time_val < 0 or time_val >= 24:
                        raise ValidationError(
                            _("Time of day must be between 00:00 and 23:59")
                        )

                    # Check that decimal part represents valid minutes (0-59)
                    hours = int(time_val)
                    minutes = round((time_val - hours) * 100)
                    if minutes >= 60:
                        raise ValidationError(
                            _(
                                "Invalid time format. Minutes must be 0-59 (e.g., 14:30 = 14.30, not 14.60)"
                            )
                        )
                else:
                    raise ValidationError(
                        _("Time of day must be specified when repeat is enabled")
                    )

    @api.constrains("end_date", "type")
    def _check_end_date(self):
        """Validate that end date is in the future and reasonable for time-based campaigns"""
        for record in self:
            if record.type == "time_based" and record.end_date:
                now = fields.Datetime.now()
                if record.end_date <= now:
                    raise ValidationError(
                        _("End date must be in the future for time-based campaigns")
                    )

                # Check that end date is not too far in the future (max 10 years)
                max_future_date = now + timedelta(days=3650)  # 10 years
                if record.end_date > max_future_date:
                    raise ValidationError(
                        _("End date cannot be more than 10 years in the future")
                    )

                # Check that end date is at least 1 hour from now
                min_future_date = now + timedelta(hours=1)
                if record.end_date < min_future_date:
                    raise ValidationError(
                        _("End date must be at least 1 hour in the future")
                    )

    @api.constrains(
        "message_initial_send_specific_date",
        "message_initial_send_type",
        "end_date",
        "type",
    )
    def _check_trigger_date(self):
        """Validate that trigger date is in the future and reasonable"""
        for record in self:
            if (
                record.message_initial_send_type == "specific_date"
                and record.message_initial_send_specific_date
            ):
                now = fields.Datetime.now()
                trigger_date = record.message_initial_send_specific_date

                if trigger_date <= now:
                    raise ValidationError(_("Specific date must be in the future"))

                # Check that trigger date is at least 1 minute from now
                min_future_date = now + timedelta(minutes=1)
                if trigger_date < min_future_date:
                    raise ValidationError(
                        _("Specific date must be at least 1 minute in the future")
                    )

                # Check that trigger date is not too far in the future (max 10 years)
                max_future_date = now + timedelta(days=3650)  # 10 years
                if trigger_date > max_future_date:
                    raise ValidationError(
                        _("Specific date cannot be more than 10 years in the future")
                    )

                # Check that trigger date is before campaign end date for time-based campaigns
                if record.type == "time_based" and record.end_date:
                    if trigger_date >= record.end_date:
                        raise ValidationError(
                            _("Specific date must be before the campaign end date (%s)")
                            % record._format_datetime_for_user(record.end_date)
                        )

            elif record.message_initial_send_type == "specific_date":
                # Required field validation
                raise ValidationError(
                    _("Specific date must be set when 'Specific Date' is selected")
                )

    @api.constrains(
        "message_initial_send_after_x_minutes",
        "message_initial_send_after_x_hours",
        "message_initial_send_after_x_days",
        "message_initial_send_type",
        "end_date",
        "type",
    )
    def _check_calculated_trigger_vs_end_date(self):
        """Validate that calculated trigger dates don't exceed campaign end date"""
        for record in self:
            if record.type == "time_based" and record.end_date:
                now = fields.Datetime.now()
                calculated_trigger_date = None

                # Calculate the trigger date based on the selected type
                if (
                    record.message_initial_send_type == "after_x_minutes"
                    and record.message_initial_send_after_x_minutes
                ):
                    calculated_trigger_date = now + timedelta(
                        minutes=record.message_initial_send_after_x_minutes
                    )
                elif (
                    record.message_initial_send_type == "after_x_hours"
                    and record.message_initial_send_after_x_hours
                ):
                    calculated_trigger_date = now + timedelta(
                        hours=record.message_initial_send_after_x_hours
                    )
                elif (
                    record.message_initial_send_type == "after_x_days"
                    and record.message_initial_send_after_x_days
                ):
                    calculated_trigger_date = now + timedelta(
                        days=record.message_initial_send_after_x_days
                    )

                # Check if calculated trigger date exceeds campaign end date
                if (
                    calculated_trigger_date
                    and calculated_trigger_date >= record.end_date
                ):
                    trigger_type_labels = {
                        "after_x_minutes": _("minutes"),
                        "after_x_hours": _("hours"),
                        "after_x_days": _("days"),
                    }
                    trigger_label = trigger_type_labels.get(
                        record.message_initial_send_type or "", ""
                    )
                    raise ValidationError(
                        _(
                            "The calculated trigger date (%s) would be after the campaign end date (%s). "
                            "Please reduce the number of %s or extend the campaign end date."
                        )
                        % (
                            record._format_datetime_for_user(calculated_trigger_date),
                            record._format_datetime_for_user(record.end_date),
                            trigger_label,
                        )
                    )

    @api.constrains(
        "message_should_send_repeat",
        "message_send_repeat_trigger_days",
        "message_send_repeat_trigger_weeks",
        "message_send_repeat_trigger_type",
        "message_initial_send_specific_date",
        "message_initial_send_after_x_minutes",
        "message_initial_send_after_x_hours",
        "message_initial_send_after_x_days",
        "message_initial_send_type",
        "end_date",
        "type",
    )
    def _check_recurring_vs_end_date(self):
        """Validate that recurring messages can be scheduled before campaign end date"""
        for record in self:
            if (
                record.type == "time_based"
                and record.end_date
                and record.message_should_send_repeat
            ):

                # Calculate when the initial message will be sent
                now = fields.Datetime.now()
                initial_send_date = None

                if record.message_initial_send_type == "now":
                    initial_send_date = now
                elif (
                    record.message_initial_send_type == "specific_date"
                    and record.message_initial_send_specific_date
                ):
                    initial_send_date = record.message_initial_send_specific_date
                elif (
                    record.message_initial_send_type == "after_x_minutes"
                    and record.message_initial_send_after_x_minutes
                ):
                    initial_send_date = now + timedelta(
                        minutes=record.message_initial_send_after_x_minutes
                    )
                elif (
                    record.message_initial_send_type == "after_x_hours"
                    and record.message_initial_send_after_x_hours
                ):
                    initial_send_date = now + timedelta(
                        hours=record.message_initial_send_after_x_hours
                    )
                elif (
                    record.message_initial_send_type == "after_x_days"
                    and record.message_initial_send_after_x_days
                ):
                    initial_send_date = now + timedelta(
                        days=record.message_initial_send_after_x_days
                    )

                if initial_send_date:
                    # Calculate when the first recurring message would be sent
                    first_recurring_date = None
                    repeat_interval_days = 0

                    if (
                        record.message_send_repeat_trigger_type == "every_x_days"
                        and record.message_send_repeat_trigger_days
                    ):
                        repeat_interval_days = record.message_send_repeat_trigger_days
                    elif (
                        record.message_send_repeat_trigger_type == "every_x_weeks"
                        and record.message_send_repeat_trigger_weeks
                    ):
                        repeat_interval_days = (
                            record.message_send_repeat_trigger_weeks * 7
                        )

                    if repeat_interval_days > 0:
                        first_recurring_date = initial_send_date + timedelta(
                            days=repeat_interval_days
                        )

                        # Check if first recurring message would be after campaign end
                        if first_recurring_date >= record.end_date:
                            if (
                                record.message_send_repeat_trigger_type
                                == "every_x_days"
                            ):
                                interval_text = (
                                    _("%d days")
                                    % record.message_send_repeat_trigger_days
                                )
                            else:
                                interval_text = (
                                    _("%d weeks")
                                    % record.message_send_repeat_trigger_weeks
                                )

                            raise ValidationError(
                                _(
                                    "The first recurring message would be scheduled for %s, which is after the campaign end date (%s). "
                                    "Either disable recurring messages, reduce the repeat interval from every %s, "
                                    "schedule the initial message earlier, or extend the campaign end date."
                                )
                                % (
                                    record._format_datetime_for_user(
                                        first_recurring_date
                                    ),
                                    record._format_datetime_for_user(record.end_date),
                                    interval_text,
                                )
                            )

                        # Calculate how many recurring messages would fit before end date
                        time_until_end = record.end_date - initial_send_date
                        total_days_available = time_until_end.total_seconds() / (
                            24 * 3600
                        )
                        possible_recurring_messages = int(
                            total_days_available / repeat_interval_days
                        )

                        # Warn if only very few recurring messages would fit (1 or fewer)
                        if possible_recurring_messages <= 1:
                            if (
                                record.message_send_repeat_trigger_type
                                == "every_x_days"
                            ):
                                interval_text = (
                                    _("%d days")
                                    % record.message_send_repeat_trigger_days
                                )
                            else:
                                interval_text = (
                                    _("%d weeks")
                                    % record.message_send_repeat_trigger_weeks
                                )

                            raise ValidationError(
                                _(
                                    "With the current settings, only %d recurring message(s) would be sent before the campaign ends. "
                                    "Consider reducing the repeat interval from every %s or extending the campaign duration "
                                    "to make recurring messages more effective."
                                )
                                % (possible_recurring_messages, interval_text)
                            )

    @api.constrains("product_recommendation_rules")
    def _check_product_rules(self):
        """Validate that product recommendation rules are valid domain expressions"""
        for record in self:
            if (
                record.product_recommendation_type == "rules"
                and record.product_recommendation_rules
            ):
                try:
                    # Try to safely evaluate the rules to check if they're valid
                    safe_eval(record.product_recommendation_rules or "[]")
                except Exception as e:
                    raise ValidationError(
                        _("Product recommendation rules contain invalid syntax: %s")
                        % str(e)
                    )

    @api.constrains(
        "message_template",
        "product_recommendation_type",
        "product_recommendation_fixed_products",
        "product_recommendation_rules",
    )
    def _check_template_products_consistency(self):
        """Validate that message template and product recommendation are consistent"""
        for record in self:
            # Check if template needs products
            template_has_product_placeholders = record._template_needs_products(
                record.message_template
            )

            if template_has_product_placeholders:
                # Template has product placeholders, so we need products configured
                if record.product_recommendation_type == "none":
                    raise ValidationError(
                        _(
                            "The message template contains product placeholders, but product recommendation is set to 'None'. "
                            "Please either remove product placeholders from the template or configure product recommendations."
                        )
                    )

                elif record.product_recommendation_type == "fixed_products":
                    if not record.product_recommendation_fixed_products:
                        raise ValidationError(
                            _(
                                "The message template contains product placeholders, but no fixed products are selected. "
                                "Please select products or change the product recommendation type."
                            )
                        )

                elif record.product_recommendation_type == "rules":
                    # Additionally, try to validate that the rules actually return products
                    try:
                        domain = safe_eval(record.product_recommendation_rules or "[]")
                        product_count = self.env["product.product"].search_count(domain)
                        if product_count == 0:
                            raise ValidationError(
                                _(
                                    "The message template contains product placeholders, but the product recommendation rules "
                                    "do not match any products. Please check whether you have added the products in Odoo."
                                )
                            )
                    except Exception as e:
                        # Rule syntax error is already handled by _check_product_rules
                        # This is just for additional product count validation
                        pass

    def action_preview_messages(self):
        """
        Preview how messages will look with the current template and data.
        Useful for testing templates before sending.
        """
        # Ensure record is saved with any form changes before processing
        self.ensure_one()

        for rec in self:
            selected_customers = (
                rec.customer_segmentation_id.selected_customers
                if rec.customer_segmentation_id.type == "manual"
                else self.env["res.partner"].search(
                    safe_eval(rec.customer_segmentation_id.rules)
                )
            )

            if not selected_customers:
                return show_notification(
                    self.env,
                    "warning",
                    "No Customers",
                    "No customers found for the selected segmentation.",
                    direct_return=True,
                )

            # Get products to recommend
            products = []
            if rec.product_recommendation_type == "fixed_products":
                products = rec.product_recommendation_fixed_products
            elif rec.product_recommendation_type == "rules":
                products = self.env["product.product"].search(
                    safe_eval(rec.product_recommendation_rules)
                )

            # Note: Template-products consistency is now validated by field constraint
            # This ensures products are available when template needs them

            renderer = MessageTemplateRenderer(self.env)

            # Generate preview for first customer
            sample_customer = selected_customers[0]
            preview_message = renderer.render(
                rec.message_template, sample_customer, products
            )

            _logger.info(f"Preview lho")
            _logger.info(f"Message Preview for {sample_customer.name}:")
            _logger.info(preview_message)

            show_notification(
                self.env,
                "success",
                f"Message Preview for {sample_customer.name}",
                f"Preview:\n\n{preview_message}\n\nCheck server logs for full details.",
                sticky=True,
            )

    def action_test(self):
        # Ensure record is saved with any form changes before processing
        self.ensure_one()

        for rec in self:
            config = self.env["res.config.settings"].get_whatsapp_config()
            test_customer_id = config.get('test_customer_id', False)
            test_customers = [self.env['res.partner'].browse(test_customer_id)] if test_customer_id else []

            if not test_customers:
                # Get target customers with safe evaluation
                if rec.customer_segmentation_id.type == "manual":
                    test_customers = rec.customer_segmentation_id.selected_customers
                else:
                    try:
                        test_customers = self.env["res.partner"].search(
                            safe_eval(rec.customer_segmentation_id.rules or "[]")
                        )
                    except Exception as e:
                        return show_notification(
                            self.env,
                            "error",
                            "Invalid Customer Rules",
                            f"Error evaluating customer segmentation rules: {str(e)}",
                            direct_return=True,
                        )

            if not test_customers:
                return show_notification(
                    self.env,
                    "warning",
                    "No Test Customer",
                    "No test customer is set. Please set a test customer in the configuration.",
                    direct_return=True,
                )

            # Get products to recommend
            products = []
            if rec.product_recommendation_type == "fixed_products":
                products = rec.product_recommendation_fixed_products
            elif rec.product_recommendation_type == "rules":
                try:
                    products = self.env["product.product"].search(
                        safe_eval(rec.product_recommendation_rules or "[]")
                    )
                except Exception as e:
                    return show_notification(
                        self.env,
                        "error",
                        "Invalid Product Rules",
                        f"Error evaluating product recommendation rules: {str(e)}",
                        direct_return=True,
                    )

            # Note: Template-products consistency is now validated by field constraint
            # This ensures products are available when template needs them

            return self._action_send_messages(test_customers, products, "test")

    def action_run(self):
        """
        Execute the campaign based on its configuration.
        Creates opportunities for customers and schedules message sending.
        """
        # Ensure record is saved with any form changes before processing
        self.ensure_one()

        for rec in self:
            # Get target customers with safe evaluation
            if rec.customer_segmentation_id.type == "manual":
                selected_customers = rec.customer_segmentation_id.selected_customers
            else:
                try:
                    selected_customers = self.env["res.partner"].search(
                        safe_eval(rec.customer_segmentation_id.rules or "[]")
                    )
                except Exception as e:
                    return show_notification(
                        self.env,
                        "error",
                        "Invalid Customer Rules",
                        f"Error evaluating customer segmentation rules: {str(e)}",
                        direct_return=True,
                    )

            if not selected_customers:
                return show_notification(
                    self.env,
                    "warning",
                    "No Customers",
                    "No customers found for the selected segmentation.",
                    direct_return=True,
                )

            # Get products to recommend
            products = []
            if rec.product_recommendation_type == "fixed_products":
                products = rec.product_recommendation_fixed_products
            elif rec.product_recommendation_type == "rules":
                try:
                    products = self.env["product.product"].search(
                        safe_eval(rec.product_recommendation_rules or "[]")
                    )
                except Exception as e:
                    return show_notification(
                        self.env,
                        "error",
                        "Invalid Product Rules",
                        f"Error evaluating product recommendation rules: {str(e)}",
                        direct_return=True,
                    )

            # Note: Template-products consistency is now validated by field constraint
            # This ensures products are available when template needs them

            # Create opportunities for each customer
            rec._create_opportunities(selected_customers)

            # Handle initial message sending
            rec._handle_initial_send(selected_customers, products)

            # Handle recurring messages if enabled (regardless of campaign type)
            if rec.message_should_send_repeat:
                rec._handle_recurring_messages(selected_customers, products)

            # Update campaign state
            rec.state = "running"

            show_notification(
                self.env,
                "success",
                "Campaign Started",
                f"Campaign '{rec.name}' has been started successfully with {len(selected_customers)} customers.",
            )

    def action_finish(self):
        """
        Finish the campaign and handle cleanup.
        """
        for rec in self:
            # Stop all scheduled actions for this campaign
            rec._stop_scheduled_actions()

            # Handle opportunities - mark as lost if not won
            rec._handle_opportunities_on_finish()

            # Update state
            rec.state = "finished"

            show_notification(
                self.env,
                "success",
                "Campaign Finished",
                f"Campaign '{rec.name}' has been finished successfully. All scheduled actions have been stopped.",
            )

    def action_cancel(self):
        """
        Cancel the campaign and handle cleanup.
        """
        for rec in self:
            # Stop all scheduled actions for this campaign
            rec._stop_scheduled_actions()

            # Handle opportunities - mark as lost for both campaign types.
            rec._handle_opportunities_on_cancel()

            # Update state
            rec.state = "cancelled"

            show_notification(
                self.env,
                "info",
                "Campaign Cancelled",
                f"Campaign '{rec.name}' has been cancelled. All scheduled actions have been stopped.",
            )

    def action_reset(self):
        """
        Reset the campaign to draft state and handle cleanup.
        """
        for rec in self:
            # Stop all scheduled actions for this campaign
            rec._stop_scheduled_actions()

            # Update state
            rec.state = "draft"

            show_notification(
                self.env,
                "info",
                "Campaign Reset",
                f"Campaign '{rec.name}' has been reset to draft state. All scheduled actions have been stopped.",
            )

    def _template_needs_products(self, template):
        """
        Check if the template contains any product-related placeholders.
        Handles both simple {products} and complex {products:function(...)} formats.
        """
        try:
            from ..utils import find_template_expressions, parse_template_expression

            # Find all template expressions in the message
            expressions = find_template_expressions(template)

            # Check if any expression references products
            for expression in expressions:
                parsed = parse_template_expression(expression)
                if parsed.get("variable") == "products":
                    return True

            return False
        except Exception as e:
            _logger.warning(f"Error checking template for product placeholders: {e}")
            # Fallback to simple check
            return "{products}" in template or "{products:" in template

    def _create_opportunities(self, customers):
        """
        Create opportunities for each customer in the campaign.
        """
        for rec in self:
            for customer in customers:
                # Create opportunity for each customer
                try:
                    # Get and validate the user assignment
                    assigned_user = (
                        rec.assigned_to if rec.assigned_to else self.env.user
                    )

                    # Verify user exists and is active
                    if (
                        not assigned_user
                        or not assigned_user.exists()
                        or not assigned_user.active
                    ):
                        # Fallback to current user or admin
                        assigned_user = (
                            self.env.user
                            if self.env.user.active
                            else self.env.ref("base.user_admin")
                        )
                        _logger.warning(
                            f"Invalid assigned user, falling back to: {assigned_user.name}"
                        )

                    _logger.info(
                        f"Creating opportunity with user ID: {assigned_user.id} ({assigned_user.name})"
                    )

                    opportunity = self.env["crm.lead"].create(
                        {
                            "name": f"{rec.name} - {customer.name}",
                            "partner_id": customer.id,
                            "user_id": assigned_user.id,
                            "team_id": False,  # Can be set to a specific sales team if needed
                            "stage_id": self._get_default_stage_id(),
                            "description": f"Opportunity created from marketing campaign: {rec.name}",
                            "source_id": self._get_or_create_campaign_source(rec.name),
                        }
                    )

                    _logger.info(
                        f"Created opportunity {opportunity.id} for customer {customer.name} with salesperson {assigned_user.name}"
                    )
                except Exception as e:
                    _logger.error(
                        f"Error creating opportunity for customer {customer.name}: {e}"
                    )
                    show_notification(
                        self.env,
                        "error",
                        "Error Creating Opportunity",
                        f"Error creating opportunity for customer {customer.name}: {e}",
                    )

    def _get_default_stage_id(self):
        """
        Get the default stage for new opportunities.
        """
        default_stage = self.env["crm.stage"].search([("is_won", "=", False)], limit=1)
        _logger.info(f"Default crm stage: {default_stage}")
        return default_stage.id if default_stage else False

    def _get_or_create_campaign_source(self, campaign_name):
        """
        Get or create a lead source for the campaign.
        """
        source_name = f"WhatsApp Campaign: {campaign_name}"
        source = self.env["utm.source"].search([("name", "=", source_name)], limit=1)

        if not source:
            source = self.env["utm.source"].create(
                {
                    "name": source_name,
                }
            )

        return source.id

    def _handle_initial_send(self, customers, products):
        """
        Handle initial message sending based on trigger settings.
        """
        for rec in self:
            if rec.message_initial_send_type == "now":
                # Send immediately
                return rec._action_send_messages(customers, products, "initial")
            elif rec.message_initial_send_type == "specific_date":
                # Schedule for specific date
                if rec.message_initial_send_specific_date:
                    rec._schedule_initial_message_sending(
                        customers, products, rec.message_initial_send_specific_date
                    )
            elif rec.message_initial_send_type == "after_x_minutes":
                # Schedule after X minutes
                if rec.message_initial_send_after_x_minutes:
                    trigger_date = datetime.now() + timedelta(
                        minutes=rec.message_initial_send_after_x_minutes
                    )
                    _logger.info(
                        f"Scheduling initial message sending for {trigger_date}"
                    )
                    rec._schedule_initial_message_sending(
                        customers, products, trigger_date
                    )
            elif rec.message_initial_send_type == "after_x_hours":
                # Schedule after X hours
                if rec.message_initial_send_after_x_hours:
                    trigger_date = datetime.now() + timedelta(
                        hours=rec.message_initial_send_after_x_hours
                    )
                    _logger.info(
                        f"Scheduling initial message sending for {trigger_date}"
                    )
                    rec._schedule_initial_message_sending(
                        customers, products, trigger_date
                    )
            elif rec.message_initial_send_type == "after_x_days":
                # Schedule after X days
                if rec.message_initial_send_after_x_days:
                    trigger_date = datetime.now() + timedelta(
                        days=rec.message_initial_send_after_x_days
                    )
                    _logger.info(
                        f"Scheduling initial message sending for {trigger_date}"
                    )
                    rec._schedule_initial_message_sending(
                        customers, products, trigger_date
                    )

    def _handle_recurring_messages(self, customers, products):
        """
        Handle recurring message scheduling. End date is determined by campaign type:
        - time_based: requires end_date to be set, recurring stops at end_date
        - forever: no end_date, recurring continues until manually stopped
        """
        for rec in self:
            end_date = None

            if rec.type == "time_based":
                if not rec.end_date:
                    return show_notification(
                        self.env,
                        "warning",
                        "End Date Required",
                        "Time-based campaigns require an end date to be set.",
                        direct_return=True,
                    )
                end_date = rec.end_date
            # For forever campaigns, end_date remains None

            # Schedule recurring messages
            rec._schedule_recurring_messages(customers, products, end_date)

            # For time-based campaigns, also schedule automatic finish at end date
            if rec.type == "time_based" and end_date:
                rec._schedule_campaign_finish(end_date)

    def _schedule_initial_message_sending(self, customers, products, execution_date):
        """
        Schedule initial message sending for a specific date using Odoo's cron system.
        """
        for rec in self:
            # Create a scheduled action (cron job) for this campaign
            cron_vals = {
                "name": f"Campaign Initial Message: {rec.name}",
                "model_id": self.env.ref(
                    "wa_marketing_automation.model_wa_marketing_automation_campaign"
                ).id,
                "state": "code",
                "code": f"model.browse({rec.id})._execute_initial_send({[c.id for c in customers]}, {[p.id for p in products]})",
                "nextcall": execution_date,
                "active": True,
            }

            cron = self.env["ir.cron"].create(cron_vals)
            _logger.info(
                f"Scheduled campaign execution for {execution_date} with cron job {cron.id}"
            )

    def _schedule_recurring_messages(self, customers, products, end_date):
        """
        Schedule recurring message sending.
        """
        for rec in self:
            # Calculate interval based on trigger settings
            interval_type = ""
            interval_number = 1
            if rec.message_send_repeat_trigger_type == "every_x_days":
                interval_type = "days"
                interval_number = rec.message_send_repeat_trigger_days or 1
            elif rec.message_send_repeat_trigger_type == "every_x_weeks":
                interval_type = "weeks"
                interval_number = rec.message_send_repeat_trigger_weeks or 1
            else:
                interval_type = "days"
                interval_number = 1

            # Calculate next execution time
            next_call = datetime.now()
            if rec.message_send_repeat_trigger_time:
                # Set specific time of day
                hour = int(rec.message_send_repeat_trigger_time)
                minute = int((rec.message_send_repeat_trigger_time % 1) * 60)
                next_call = next_call.replace(
                    hour=hour, minute=minute, second=0, microsecond=0
                )
                # If time has passed for today, schedule for next interval
                if next_call <= datetime.now():
                    if interval_type == "days":
                        next_call += timedelta(days=interval_number)
                    elif interval_type == "weeks":
                        next_call += timedelta(weeks=interval_number)

            # Create recurring scheduled action
            cron_vals = {
                "name": f"Campaign Recurring Messages: {rec.name}",
                "model_id": self.env.ref(
                    "wa_marketing_automation.model_wa_marketing_automation_campaign"
                ).id,
                "state": "code",
                "code": f"model.browse({rec.id})._execute_recurring_messages({[c.id for c in customers]}, {[p.id for p in products]}, end_date='{end_date}' if end_date else None)",
                "interval_number": interval_number,
                "interval_type": interval_type,
                "nextcall": next_call,
                "active": True,
            }

            cron = self.env["ir.cron"].create(cron_vals)
            _logger.info(f"Scheduled recurring campaign with cron job {cron.id}")

    def _schedule_campaign_finish(self, end_date):
        """
        Schedule automatic campaign finishing at end date for time-based campaigns.
        """
        for rec in self:
            # Create a scheduled action to finish the campaign at end date
            cron_vals = {
                "name": f"Campaign Auto-Finish: {rec.name}",
                "model_id": self.env.ref(
                    "wa_marketing_automation.model_wa_marketing_automation_campaign"
                ).id,
                "state": "code",
                "code": f"model.browse({rec.id})._auto_finish_campaign()",
                "nextcall": end_date,
                "active": True,
            }

            cron = self.env["ir.cron"].create(cron_vals)
            _logger.info(
                f"Scheduled auto-finish for campaign {rec.name} at {end_date} with cron job {cron.id}"
            )

    def _execute_initial_send(self, customer_ids, product_ids):
        """
        Execute initial message send - called by cron jobs for scheduled execution.
        Deactivates the cron job after execution.
        """
        customers = self.env["res.partner"].browse(customer_ids)
        products = self.env["product.product"].browse(product_ids)

        for rec in self:
            # Check if campaign is still active
            if rec.state != "running":
                return

            _logger.info(
                f"Executing one-time campaign {rec.name} for {len(customers)} customers"
            )

            # Send messages
            result = rec._action_send_messages(customers, products, "initial")

            # Mark execution as completed - cleanup cron will deactivate this job
            _logger.info(
                f"One-time campaign {rec.name} execution completed. Cleanup cron will deactivate the scheduled action."
            )

            return result

    def _auto_finish_campaign(self):
        """
        Automatically finish a time-based campaign when it reaches its end date.
        Called by scheduled cron jobs.
        """
        for rec in self:
            if rec.state == "running" and rec.type == "time_based":
                _logger.info(
                    f"Auto-finishing time-based campaign {rec.name} at end date"
                )

                # Stop all scheduled actions
                rec._stop_scheduled_actions()

                # Handle opportunities
                rec._handle_opportunities_on_time_end()

                # Update state to finished
                rec.state = "finished"

                _logger.info(f"Campaign {rec.name} auto-finished successfully")

    @api.model
    def _cleanup_completed_campaign_jobs(self):
        """
        Cleanup cron job method: Deactivate completed campaign cron jobs.
        This includes initial message sending, auto-finish jobs, and recurring campaigns for finished campaigns.
        This runs separately to avoid database lock conflicts.
        """
        try:
            # Find all active campaign-related cron jobs
            campaign_crons = self.env["ir.cron"].search(
                [
                    "|",
                    "|",
                    ("name", "ilike", "Campaign Initial Message:"),
                    ("name", "ilike", "Campaign Auto-Finish:"),
                    ("name", "ilike", "Campaign Recurring Messages:"),
                    ("active", "=", True),
                    ("state", "=", "code"),  # Only code-based crons
                ]
            )

            deactivated_count = 0
            for cron in campaign_crons:
                try:
                    should_deactivate = False

                    # For one-time jobs (initial messages and auto-finish), deactivate if they've executed
                    if (
                        "Campaign Initial Message:" in cron.name
                        or "Campaign Auto-Finish:" in cron.name
                    ):
                        if cron.lastcall:
                            should_deactivate = True

                    # For recurring jobs, check if the associated campaign is no longer running
                    elif "Campaign Recurring Messages:" in cron.name:
                        # Extract campaign name from cron job name
                        campaign_name = cron.name.replace(
                            "Campaign Recurring Messages: ", ""
                        )
                        campaign = self.env["wa_marketing_automation.campaign"].search(
                            [("name", "=", campaign_name)], limit=1
                        )
                        if campaign and campaign.state != "running":
                            should_deactivate = True

                    if should_deactivate:
                        cron.write({"active": False})
                        deactivated_count += 1
                        _logger.info(
                            f"Cleanup: Deactivated campaign cron job: {cron.name}"
                        )
                except Exception as e:
                    _logger.warning(
                        f"Cleanup: Could not deactivate cron {cron.name}: {e}"
                    )
                    continue

            if deactivated_count > 0:
                _logger.info(
                    f"Cleanup: Successfully deactivated {deactivated_count} campaign cron jobs"
                )

        except Exception as e:
            _logger.error(f"Cleanup cron failed: {e}")

    def _execute_recurring_messages(self, customer_ids, product_ids, end_date=None):
        """
        Execute recurring message sending - called by cron jobs.
        Checks end date and deactivates if needed.
        """
        customers = self.env["res.partner"].browse(customer_ids)
        products = self.env["product.product"].browse(product_ids)

        for rec in self:
            # Check if campaign is still active
            if rec.state != "running":
                return

            # Check if we've passed the end date - if so, skip execution (auto-finish will handle cleanup)
            if end_date and end_date != "None":
                try:
                    # Safely parse the end date string
                    end_date_str = str(end_date).replace("'", "").strip()
                    if end_date_str:
                        end_datetime = datetime.fromisoformat(end_date_str)
                        if datetime.now() > end_datetime:
                            # Campaign has reached its end date - skip execution
                            # The auto-finish cron job will handle cleanup and opportunity management
                            _logger.info(
                                f"Time-based campaign {rec.name} has reached its end date - skipping execution (auto-finish will handle cleanup)"
                            )
                            return
                except (ValueError, TypeError) as e:
                    _logger.error(
                        f"Invalid end_date format for campaign {rec.name}: {end_date}. Error: {e}"
                    )
                    # Continue execution if date parsing fails - don't stop the campaign
                    pass

            _logger.info(
                f"Executing recurring campaign {rec.name} for {len(customers)} customers"
            )

            # Send messages
            return rec._action_send_messages(customers, products, "scheduled")

    def _stop_scheduled_actions(self):
        """
        Stop all scheduled actions (cron jobs) related to this campaign.
        """
        for rec in self:
            # Find all cron jobs created for this campaign
            campaign_crons = self.env["ir.cron"].search(
                [
                    "|",
                    "|",
                    ("name", "=", f"Campaign Initial Message: {rec.name}"),
                    ("name", "=", f"Campaign Recurring Messages: {rec.name}"),
                    ("name", "=", f"Campaign Auto-Finish: {rec.name}"),
                    ("active", "=", True),
                ]
            )

            if campaign_crons:
                # Deactivate the cron jobs
                campaign_crons.write({"active": False})
                _logger.info(
                    f"Stopped {len(campaign_crons)} scheduled actions for campaign {rec.name}"
                )

    def _handle_opportunities_on_finish(self):
        """
        Handle opportunities when campaign is manually finished.
        Applies to both time_based and forever campaigns - mark as lost if not won.
        """
        for rec in self:
            # Find opportunities created by this campaign
            opportunities = rec._get_campaign_opportunities()

            # Get lost stage
            lost_stage = rec._get_lost_stage()

            if opportunities and lost_stage:
                # Only update opportunities that are not already won
                won_stages = self.env["crm.stage"].search([("is_won", "=", True)])
                opportunities_to_update = opportunities.filtered(
                    lambda opp: opp.stage_id.id not in won_stages.ids
                )

                if opportunities_to_update:
                    opportunities_to_update.write({"stage_id": lost_stage.id})
                    _logger.info(
                        f"Marked {len(opportunities_to_update)} opportunities as lost for finished campaign {rec.name}"
                    )

    def _handle_opportunities_on_cancel(self):
        """
        Handle opportunities when campaign is cancelled - mark as lost for both campaign types.
        """
        for rec in self:
            # Find opportunities created by this campaign
            opportunities = rec._get_campaign_opportunities()

            # Get lost stage
            lost_stage = rec._get_lost_stage()

            if opportunities and lost_stage:
                # Update all opportunities to lost stage (regardless of current stage)
                opportunities.write({"stage_id": lost_stage.id})
                _logger.info(
                    f"Marked {len(opportunities)} opportunities as lost for cancelled campaign {rec.name}"
                )

    def _handle_opportunities_on_time_end(self):
        """
        Handle opportunities when time-based campaign reaches its end date.
        Only applies to time-based campaigns. Forever campaigns don't have natural end dates.
        """
        for rec in self:
            if rec.type != "time_based":
                # Only time-based campaigns should mark opportunities as lost on end date
                return

            # Find opportunities created by this campaign
            opportunities = rec._get_campaign_opportunities()

            # Get lost stage
            lost_stage = rec._get_lost_stage()

            if opportunities and lost_stage:
                # Only update opportunities that are not already won
                won_stages = self.env["crm.stage"].search([("is_won", "=", True)])
                opportunities_to_update = opportunities.filtered(
                    lambda opp: opp.stage_id.id not in won_stages.ids
                )

                if opportunities_to_update:
                    opportunities_to_update.write({"stage_id": lost_stage.id})
                    _logger.info(
                        f"Marked {len(opportunities_to_update)} opportunities as lost for time-based campaign {rec.name} that reached its end date"
                    )

    def _get_campaign_opportunities(self):
        """
        Get all opportunities created by this campaign.
        """
        for rec in self:
            # Find opportunities with the campaign's UTM source
            campaign_source = self.env["utm.source"].search(
                [("name", "=", f"WhatsApp Campaign: {rec.name}")], limit=1
            )

            if campaign_source:
                return self.env["crm.lead"].search(
                    [("source_id", "=", campaign_source.id)]
                )

            return self.env["crm.lead"]

    def _get_lost_stage(self):
        """
        Get the lost stage for opportunities.
        """
        # Try to find a stage that indicates lost/cancelled
        lost_stage = self.env["crm.stage"].search(
            ["|", ("name", "ilike", "lost"), ("name", "ilike", "cancelled")], limit=1
        )

        # If no specific lost stage found, get a stage that is not won
        if not lost_stage:
            lost_stage = self.env["crm.stage"].search(
                [("is_won", "=", False)], limit=1, order="sequence desc"
            )  # Get the last non-won stage

        return lost_stage

    def _action_send_messages(self, customers, products, execution_type="manual"):
        """
        Send WhatsApp messages to customers and log the results.
        """
        for rec in self:
            recipients: list[dict[str, str]] = []
            invalid_phone_customers: list[str] = []
            renderer = MessageTemplateRenderer(self.env)

            # Prepare recipients list with phone validation
            for customer in customers:
                phone = customer.mobile if customer.mobile else customer.phone

                # Validate phone number
                is_valid, formatted_phone = validate_phone_number(phone)

                if not is_valid:
                    invalid_phone_customers.append(customer.name)
                    _logger.warning(
                        f"Customer {customer.name} has invalid/missing phone number: {phone}"
                    )
                    continue

                # Use the new templating system
                message = renderer.render(rec.message_template, customer, products)

                _logger.info(
                    f"Prepared message for {customer.name} ({formatted_phone}): {message}"
                )

                recipients.append({"to": formatted_phone, "message": message})

            # Check if we have any valid recipients
            if not recipients:
                return show_notification(
                    self.env,
                    "error",
                    "No Valid Phone Numbers",
                    "No customers have valid phone numbers for WhatsApp messaging. Please check customer phone number formats.",
                    direct_return=True,
                )

            # Notify about invalid phone numbers if any
            if invalid_phone_customers:
                _logger.warning(
                    f"Campaign {rec.name}: {len(invalid_phone_customers)} customers have invalid phone numbers"
                )
                show_notification(
                    self.env,
                    "warning",
                    f"Invalid Phone Numbers ({len(invalid_phone_customers)} customers)",
                    f"Some customers were skipped due to invalid/missing phone numbers: {', '.join(invalid_phone_customers[:5])}"
                    + (
                        f" and {len(invalid_phone_customers) - 5} more..."
                        if len(invalid_phone_customers) > 5
                        else ""
                    ),
                )

            # Prepare API request data
            config = self.env["res.config.settings"].get_whatsapp_config()
            api_url = f"{config['base_url']}{config['send_path_url']}"
            request_data = {"recipients": recipients}

            # Track execution start time
            execution_start = datetime.now()

            try:
                # Make API request
                response = requests.post(api_url, json=request_data, timeout=30)

                # Log successful execution
                log_message = f"Campaign '{rec.name}' - Sent messages to {len(recipients)} recipients"

                if response.status_code == 200:
                    # Success case
                    rec._create_api_log(
                        message=f"{log_message}\nResponse: {response.text}",
                        status="success",
                        execution_time=execution_start,
                        recipients_count=len(recipients),
                        execution_type=execution_type,
                    )
                    _logger.info(f"Successfully sent messages for campaign {rec.name}")
                    show_notification(
                        self.env,
                        "success",
                        _("Success"),
                        _(f"Successfully sent messages for campaign {rec.name}"),
                    )
                else:
                    # HTTP error case
                    error_msg = (
                        f"[{response.status_code}] - {log_message}\n{response.text}"
                    )
                    rec._create_api_log(
                        message=error_msg,
                        status="error",
                        execution_time=execution_start,
                        recipients_count=len(recipients),
                        execution_type=execution_type,
                    )
                    _logger.error(
                        f"API request failed for campaign {rec.name}: {error_msg}"
                    )
                    show_notification(
                        self.env,
                        "error",
                        _("API Request Failed"),
                        _("API request failed for campaign {rec.name}: {error_msg}"),
                    )

            except requests.exceptions.Timeout:
                # Timeout error
                error_msg = f"Campaign '{rec.name}' - Timeout error when sending messages to {len(recipients)} recipients"
                rec._create_api_log(
                    message=error_msg,
                    status="error",
                    execution_time=execution_start,
                    recipients_count=len(recipients),
                    execution_type=execution_type,
                )
                _logger.error(f"Timeout error for campaign {rec.name}")
                show_notification(
                    self.env,
                    "error",
                    _("Timeout Error"),
                    _(
                        "Timeout error when sending messages to {len(recipients)} recipients"
                    ),
                )

            except requests.exceptions.ConnectionError:
                # Connection error
                error_msg = f"Campaign '{rec.name}' - Connection error when sending messages to {len(recipients)} recipients"
                rec._create_api_log(
                    message=error_msg,
                    status="error",
                    execution_time=execution_start,
                    recipients_count=len(recipients),
                    execution_type=execution_type,
                )
                _logger.error(f"Connection error for campaign {rec.name}")
                show_notification(
                    self.env,
                    "error",
                    _("Connection Error"),
                    _(
                        "Connection error when sending messages to {len(recipients)} recipients"
                    ),
                )

            except Exception as e:
                # General error
                error_msg = f"Campaign '{rec.name}' - Unexpected error when sending messages to {len(recipients)} recipients: {str(e)}"
                rec._create_api_log(
                    message=error_msg,
                    status="error",
                    execution_time=execution_start,
                    recipients_count=len(recipients),
                    execution_type=execution_type,
                )
                _logger.error(f"Unexpected error for campaign {rec.name}: {str(e)}")
                show_notification(
                    self.env,
                    "error",
                    _("Unexpected Error"),
                    _(
                        "Unexpected error when sending messages to {len(recipients)} recipients"
                    ),
                )

    def _create_api_log(
        self,
        message,
        status,
        execution_time,
        recipients_count=0,
        execution_type="manual",
    ):
        """
        Create a log entry in the WhatsApp API log.
        """
        try:
            self.env["wa_marketing_automation.whatsapp_api_log"].create(
                {
                    "message": message,
                    "status": status,
                    "at": execution_time,
                    "campaign_id": self.id,
                    "recipients_count": recipients_count,
                    "execution_type": execution_type,
                }
            )
        except Exception as e:
            _logger.error(f"Failed to create API log entry: {str(e)}")
