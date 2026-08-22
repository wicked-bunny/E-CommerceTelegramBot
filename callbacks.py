
from aiogram.filters.callback_data import CallbackData


# A system for securely transmitting product IDs to a button
class BuyProductCallback(CallbackData, prefix="buy_prod"):
    action: str
    product_id: int
class MainTabsCallback(CallbackData, prefix="main_tabs"):
    target: str
class CategoriesCallback(CallbackData, prefix="categories_cb"):
    target: int