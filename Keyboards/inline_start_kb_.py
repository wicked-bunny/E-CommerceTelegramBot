from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks import MainTabsCallback


def generate_start_kb() -> InlineKeyboardMarkup:
    """Inline Keyboard vor start generieren """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛍️ Catalog", callback_data=MainTabsCallback(target="catalog").pack())],
            [InlineKeyboardButton(text="📦 My Orders", callback_data=MainTabsCallback(target="orders").pack())],
            [InlineKeyboardButton(text="ℹ️ About Bot", callback_data=MainTabsCallback(target="bot_info").pack())]
        ]
    )
