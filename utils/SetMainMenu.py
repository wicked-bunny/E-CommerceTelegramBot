import types
from email.policy import default

from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import BotCommand, Message, BotCommandScopeChat

from filters.is_admin import IsAdmin
from handlers.start import router
from lexicon import LexiconEN
from repositories.unit_of_work import IUnitOfWork
from utils import start_commands
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScope


async def set_command(bot: Bot, *bot_commands: BotCommand, scope: BotCommandScope = BotCommandScopeDefault()):
    await bot.set_my_commands(commands=list(bot_commands), scope=scope)

async def set_start_command(bot: Bot):
    bot_command = start_commands.UserStartCommand
    await set_command(bot, bot_command)

@router.message(Command("start"), IsAdmin())
async def set_admin_command(message: Message):
    admin_commands = start_commands.AdminStartCommand
    admin_scope = BotCommandScopeChat(chat_id=message.chat.id)
    await set_command(message.bot, admin_commands, scope=admin_scope)

