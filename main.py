import asyncio
import os
import logging
import sys
from infrastructure.ngrok_tunnel import NgrokTunnelManager
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiohttp import web

from handlers import register_routers
from middlewares import register_middleware
from database import init_model, session_maker
from utils.SetMainMenu import set_start_command
from api.stripe_webhook import StripeWebhookController

logging.basicConfig(
    level=logging.INFO,  # Shows all important events and tracking logs
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Outputs logs directly to the PyCharm console
    ]
)

ENV_PATH = "BotToken.env"
load_dotenv(dotenv_path=ENV_PATH)

TOKEN = os.getenv("TOKEN")
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

async def run_bot(bot: Bot, dp: Dispatcher):
    """
    Asynchronously runs the core Telegram bot engine via Long Polling.
    """
    await set_start_command(bot)
    register_routers(dp)
    register_middleware(dp, session_maker)

    print("🤖 Telegram Bot has been successfully started via Polling...")
    await dp.start_polling(bot)


async def run_stripe_api(bot: Bot):
    """
    Asynchronously starts an isolated web server to listen for Stripe Webhooks.
    """
    controller = StripeWebhookController(bot)

    app = web.Application()
    app.router.add_post('/stripe_webhook', controller.handle_webhook)

    # Automatically provision the external networking tunnel via infrastructure manager
    # (Only during active local development)
    NgrokTunnelManager.start_tunnel(port=5000)

    # Bind the webhook HTTP container to localhost port 5000
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 5000)
    await site.start()

    await asyncio.Event().wait()


async def main():
    # Database migration framework initialization
    await init_model()

    print("Initializing components...")
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Orchestrate concurrent background execution for both services in the master event loop
    await asyncio.gather(
        run_bot(bot, dp),
        run_stripe_api(bot)
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("The bot application has been forcefully stopped.")
