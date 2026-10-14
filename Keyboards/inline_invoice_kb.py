from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callbacks import MainTabsCallback

def invoice_kb(product_price_cents: int, payment_url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text=f"ℹ️ Project Info", callback_data=MainTabsCallback(target="bot_info").pack()),
         InlineKeyboardButton(text=f"💳 Pay ${(product_price_cents / 100):.2f}", url=payment_url)]
    ])