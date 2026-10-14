import os
import stripe
import asyncio
from functools import partial


class StripeService:
    @staticmethod
    async def create_checkout_session(user_id: int, product_id: int, product_name: str, price_cents: int) -> str:
        """
        Asynchronously creates a Stripe Hosted Checkout Session.
        Loads credentials dynamically to ensure seamless environment setup.
        """
        api_key = os.getenv("STRIPE_SECRET_KEY") or os.getenv("STRIPE_API_KEY")
        bot_username = os.getenv("BOT_USERNAME")

        if not api_key:
            raise ValueError("❌ Stripe API Key is missing inside environment variables.")
        if not bot_username:
            raise ValueError("❌ BOT_USERNAME is missing inside environment variables.")

        clean_username = bot_username.lstrip('@')

        stripe.api_key = api_key

        try:
            loop = asyncio.get_running_loop()
            create_session_func = partial(
                stripe.checkout.Session.create,
                payment_method_types=['card'],
                metadata={
                    "user_id": str(user_id),
                    "product_id": str(product_id)
                },
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': price_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',

                success_url=f"tg://resolve?domain={clean_username}&start=success_{product_id}",
                cancel_url=f"tg://resolve?domain={clean_username}&start=cancel",
            )

            session = await loop.run_in_executor(None, create_session_func)
            return session.url

        except Exception as e:
            print(f"[STRIPE SERVICE CRASH] Core API Exception caught: {e}")
            raise e
