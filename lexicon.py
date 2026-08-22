STORE_NAME = "E-commerceBot"


class LexiconEN:
    @staticmethod
    def start_message() -> str:
        return f"""<b>👋 WELCOME TO {STORE_NAME.upper()}!</b>
_____________________________________

    Your personal shopping assistant right in Telegram.
    
    🛒 Browse products by categories
    🔍 View details and prices
    🛍 Place orders easily
    📦 Fast and simple!
    
    Use the buttons below to get started 👇
                """
    @staticmethod
    def item_description_text(name: str, price: int, description: str):
        return (
            f"🛍 <b>{name}</b>\n\n"
            f"💰 Price: {price} €\n"
            f"📝 Description:\n\n{description}"
        )
    @staticmethod
    def info_text() -> str:
        return """<b>ℹ️ ABOUT THIS PROJECT</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🤖 <b>E-Commerce Bot</b> is a portfolio project built to demonstrate modern backend development practices for Telegram.

🚀 <b>Tech Stack Used:</b>
• <b>Language:</b> Python 3.11+
• <b>Framework:</b> Aiogram 3.x (Async)
• <b>Database:</b> SQLite
• <b>ORM:</b> SQLAlchemy 2.0 (Async)
• <b>Architecture:</b> Repository & Unit of Work (UoW) patterns

💻 <b>Key Features:</b>
• Dynamic catalog browsing
• Async database transactions
• Secure session & state management (FSM)
• Scalable & clean code structure

👨‍💻 <b>Developer:</b> WickedBunny
🌐 <b>GitHub:</b> <a href="https://github.com/wicked-bunny/E-CommerceTelegramBot">://https://github.com/wicked-bunny/E-CommerceTelegramBot</a>

<i>Thank you for testing my bot! Feel free to check out the source code on GitHub.</i>"""
    @staticmethod
    def set_main_menu_button() -> str :
        return "start"
    @staticmethod
    def choose_category()-> str:
        return "🗂️Choose a category:"

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

