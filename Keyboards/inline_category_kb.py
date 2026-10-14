from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callbacks import CategoriesCallback

def main_category_kb()-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👔Clothing", callback_data=CategoriesCallback(target=1).pack()), InlineKeyboardButton(text="📱Electronics", callback_data=CategoriesCallback(target=4).pack())],
            [InlineKeyboardButton(text="👟Shoes",callback_data=CategoriesCallback(target=2).pack()), InlineKeyboardButton(text="💄Beauty",callback_data=CategoriesCallback(target=5).pack())],
            [InlineKeyboardButton(text="🎧Accessories",callback_data=CategoriesCallback(target=3).pack()), InlineKeyboardButton(text="✅Show all Products",callback_data=CategoriesCallback(target=6).pack())]
        ],
    )
