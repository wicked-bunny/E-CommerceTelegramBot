import lexicon
from Keyboards import inline_catalog_kb
from callbacks import CategoriesCallback, BuyProductCallback
from aiogram import Router, types, F

from repositories.unit_of_work import IUnitOfWork
from enum import Enum, auto


class Categories(Enum):
    CLOTHING        = auto()      #[1]
    SHOES           = auto()      #[2]
    ACCESSORIES     = auto()      #[3]
    ELECTRONICS     = auto()      #[...]
    BEAUTY          = auto()
    ALL_PRODUCTS    = auto()


router = Router()

# Dynamically retrieve a list of all numeric IDs from our enum: [1, 2, 3, 4, 5, 6]
VALID_CATEGORY_IDS = [cat.value for cat in Categories]

@router.callback_query(CategoriesCallback.filter())
async def process_category_callback(
        callback: types.CallbackQuery,
        callback_data: CategoriesCallback,
        unit_of_work: IUnitOfWork
):
    await callback.answer()

    # Convert target to a number
    category_id = callback_data.target



    await send_category_products(callback, callback.message.chat.id, category_id, unit_of_work)

async def send_category_products(
        event: types.Message | types.CallbackQuery,
        chat_id: int,
        category_id: int,
        unit_of_work: IUnitOfWork
):
    if category_id == 6:
        # If the user selected "All products", send all products
        products = await unit_of_work.items.get_all()
    else:
        products = await unit_of_work.items.get_all_by_category(category_id)

    if not products:
        await event.bot.send_message(
            chat_id=chat_id,
            text=lexicon.ErrorEN.no_items_available_for_this_category()
        )
        return

    for item in products:
        text = lexicon.LexiconEN.item_description_text(
            name=item.name,
            price=item.price,
            description=item.description
        )

        #create callback for "Buy" button
        buy_callback = BuyProductCallback(action="buy", product_id=item.id)

        await event.bot.send_photo(
            chat_id=chat_id,
            photo=item.file_id,
            caption=text,
            parse_mode="HTML",
            # passing callback on
            reply_markup=inline_catalog_kb.generate_catalog_kb(buy_callback))

