from html import escape

STORE_NAME = "E-commerceBot"


class LexiconEN:
    @staticmethod
    def start_message() -> str:
        return f"""<b>👋 WELCOME TO {STORE_NAME.upper()}!</b>
_________________________________

Your personal shopping assistant right in Telegram.

🛒 Browse products by categories
🔍 View details and prices
🛍 Place orders easily
📦 Fast and simple!

Use the buttons below to get started 👇
            """
    @staticmethod
    def item_description_text(name: str, price: int,quantity:int, description: str):
        formatted_price = f"{price / 100.0:.2f}"

        return (
            f"🛍 <b>{name}</b>\n\n"
            f"💰 Price: {formatted_price} €\n"
            f"📦 In Stock: {quantity} pcs\n\n"
            f"📝 Description:\n{description}"
        )
    @staticmethod
    def info_text() -> str:
        return """<b>ℹ️ ABOUT THIS PROJECT</b>
━━━━━━━━━━━━━━━ 
🤖 <b>E-Commerce Bot</b> is a portfolio project built to demonstrate modern backend development practices for Telegram.

🚀 <b>Tech Stack Used:</b>
• <b>Language:</b> Python 3.11+
• <b>Framework:</b> Aiogram 3.x (Async)
• <b>Database:</b> SQLite (aiosqlite)
• <b>ORM:</b> SQLAlchemy 2.0 (Async)
• <b>Payments:</b> Stripe API Integration
• <b>Architecture:</b> Repository & Unit of Work (UoW) patterns

💳 <b>Stripe Test Card Details:</b>
• <b>Card Number:</b> <code>4242 4242 4242 4242</code>
• <b>Valid Thru:</b> Any future date (e.g., <code>12/29</code>)
• <b>CVC:</b> Any 3 digits (e.g., <code>123</code>)

💻 <b>Key Features:</b>
• Dynamic catalog browsing
• Async database transactions
• Secure Hosted Checkout (Stripe Sandbox)
• Secure session & state management (FSM)
• Scalable & clean code structure

👨‍💻 <b>Developer:</b> WickedBunny
🌐 <b>GitHub:</b> <a href="https://github.com">://github.com</a>

<i>Thank you for testing my bot! Feel free to check out the source code on GitHub.</i>"""
    @staticmethod
    def set_main_menu_button() -> str :
        return "start"
    @staticmethod
    def choose_category()-> str:
        return "🗂️Choose a category:"
    @staticmethod
    def paid_successful(product_id):
        return f"Your payment for the goods #{product_id} has been successfully processed! Access has been granted."
    @staticmethod
    def invoice_message(product_name: str, price: int) -> str:
        formatted_price = f"{price / 100.0:.2f}"

        safe_name = escape(product_name)

        return (
            f"🛒 <b>Invoice Generated Successfully</b>\n\n"
            f"Product: <b>{safe_name}</b>\n\n"
            f"💰 Price: {formatted_price} €\n\n"
            f"⚠️ <b>TEST MODE NOTICE:</b>\n"
            f"This is a testing environment, so you won't be charged. "
            f"Please do NOT enter your real personal data or real credit card numbers!\n\n"
        )


class ErrorEN:
    @staticmethod
    def currently_unavailable() -> str:
        return "We're sorry, but this is currently unavailable."
    @staticmethod
    def empty_catalog() -> str:
        return "The catalog is currently empty."
    @staticmethod
    def no_items_available_for_this_category() -> str:
        return "no items for this category is current available"
    @staticmethod
    def payment_unreachable() -> str:
        return "❌ Payment processor is temporarily unreachable. Please try again later."
    @staticmethod
    def item_not_found() -> str:
        return "❌ Sorry, this item was not found in our catalog."
    @staticmethod
    def out_of_stock() -> str:
        return "❌ Out of stock! This item is temporarily unavailable."


