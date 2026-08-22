from aiogram.types import BotCommand

from lexicon import LexiconEN

UserStartCommand = BotCommand(
    command='/start',
    description=LexiconEN.set_main_menu_button()
)
AdminStartCommand = [
    UserStartCommand,
    BotCommand(
        command='/admin',
        description="admin")
]