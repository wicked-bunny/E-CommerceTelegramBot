from aiogram import Router,F,types

import lexicon
from callbacks import MainTabsCallback

router = Router()

@router.message(F.text == "Information")
@router.callback_query(MainTabsCallback.filter(F.target == "bot_info"))
async def info(event: types.Message | types.CallbackQuery):

        await event.answer()

        await event.message.answer(
            text=lexicon.LexiconEN.info_text(),
            parse_mode="HTML"
        )
