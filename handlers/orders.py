from aiogram import Router, types, F
from callbacks import MainTabsCallback
from lexicon import ErrorEN

router = Router()



@router.message(F.text == "orders")
@router.callback_query(MainTabsCallback.filter(F.target == "orders"))
async def orders(event: types.Message | types.CallbackQuery):
        #TODO: implement logik
        await event.answer(text=ErrorEN.currently_unavailable())
