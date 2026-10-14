import stripe
from aiohttp import web
from aiogram import Bot
from os import getenv

from lexicon import LexiconEN
from repositories.implementations.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork


class StripeWebhookController:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.webhook_secret = getenv("STRIPE_WEBHOOK_SECRET")

    async def handle_webhook(self, request: web.Request) -> web.Response:
        """
        Asynchronously handles incoming POST requests from Stripe Webhooks.
        Constructs and verifies the event payload using the webhook signature.
        """
        payload = await request.text()
        sig_header = request.headers.get('Stripe-Signature')

        try:
            # Verify that the request genuinely originated from Stripe
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            # Return HTTP 400 Bad Request if verification fails
            return web.Response(status=400, text=str(e))

        # Handle the specific event type for a completed checkout session
        if event['type'] == 'checkout.session.completed':
            await self._process_successful_payment(event['data']['object'])

        return web.Response(status=200, text="OK")

    async def _process_successful_payment(self, session: dict):
        """
        Processes the business logic for a verified, successful payment session.
        Updates the database inventory and dispatches a Telegram notification.
        """
        # Extract custom properties passed during session creation from metadata
        user_id = session.get('metadata', {}).get('user_id')
        product_id = session.get('metadata', {}).get('product_id')

        if not user_id or not product_id:
            return

        # Stripe metadata properties are strictly strings; enforce explicit type casting
        user_id = int(user_id)
        product_id = int(product_id)

        # 1. DATABASE TRANSACTION MANAGEMENT VIA UNIT OF WORK
        # Initialize an isolated UoW context manager for this specific request thread
        async with SqlAlchemyUnitOfWork() as uow:
            try:
                # Invoke the specialized single-unit purchase method from the repository
                purchased_item = await uow.items.buy_one_item(item_id=product_id)

                if purchased_item is None:
                    print(f"⚠️ Payment webhook failed: Item #{product_id} no longer exists or out of stock.")
                    # Exiting the block without a commit triggers an automatic rollback
                    return

                # 2. TODO: Record a new entry in your orders table via OrderRepository
                # await uow.orders.create_order(user_id=user_id, item_id=product_id, status="paid")

                # Persist all entity modifications securely to the permanent database store
                await uow.commit()
                print(f"💰 Database updated successfully. Item #{product_id} quantity decremented.")

            except Exception as e:
                print(f"❌ Transaction failed, rolling back automatically. Error: {e}")
                # Any unhandled database layer exceptions will trigger an automatic uow rollback
                return

        # 3. TELEGRAM USER NOTIFICATION LAYER (Executed solely post-successful DB commit)
        try:
            # Extract localized ui notification string from the active lexicon module
            success_text = LexiconEN.paid_successful(product_id=product_id).format()

            # If the digital good includes a file payload, deliver it directly to the customer
            if purchased_item and purchased_item.file_id:
                await self.bot.send_document(
                    chat_id=user_id,
                    document=purchased_item.file_id,
                    caption=success_text
                )
            else:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=success_text
                )
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")
