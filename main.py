import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import register_routers
from middlewares import register_middleware
from database.models import BaseModel
import logging
import sys

from utils.SetMainMenu import set_start_command

logging.basicConfig(
    level=logging.INFO,  # Показуватиме всі важливі події та оновлення
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Виводити лог прямо в консоль PyCharm
    ]
)


ENV_PATH = "BotToken.env"
load_dotenv(dotenv_path=ENV_PATH)

TOKEN = os.getenv("TOKEN")
async  def init_model(engine):
    async  with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.run_sync(BaseModel.metadata.create_all)



async def main():


    engine = create_async_engine(
        url="sqlite+aiosqlite:///DB.db",
        isolation_level="AUTOCOMMIT"
    )

    # create tables
    await init_model(engine)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    print("starting...")
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    #set default "/start" button
    await set_start_command(bot)

    # register handlers and middlewares
    register_routers(dp)
    register_middleware(dp, session_maker)

    print("bot has been started")
    await dp.start_polling(bot)




if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("The bot has been stopped")
