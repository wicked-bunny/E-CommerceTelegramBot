from aiogram import Router, F, types
from Keyboards.inline_invoice_kb import invoice_kb

import lexicon
from callbacks import BuyProductCallback

from services.stripe_service import StripeService
from repositories.implementations.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork

router = Router()


@router.callback_query(BuyProductCallback.filter(F.action == "buy"))
async def process_buy_product(callback: types.CallbackQuery, callback_data: BuyProductCallback):
    """
    Handles the user clicking the 'Buy' button.
    Fetches the item from the database layer, verifies its existence,
    and requests a secure Stripe Checkout URL via StripeService.
    """

    await callback.answer()  # Removes the loading clock icon from the Telegram button

    product_id = callback_data.product_id
    user_id = callback.from_user.id

    # 1. DATABASE LAYER: Query the item properties via Unit of Work
    async with SqlAlchemyUnitOfWork() as uow:
        item = await uow.items.get_by_id(product_id)

        if not item:
            await callback.message.answer(lexicon.ErrorEN.item_not_found())
            return

        quantity = item.quantity_in_stock
        if quantity is None or quantity <= 0:
            await callback.message.answer(lexicon.ErrorEN.out_of_stock())
            return

        product_name = getattr(item, "name", f"Product #{product_id}")
        product_price_cents = item.price

    # 2. BUSINESS LOGIC LAYER: Generate a secure external Stripe payment session
    try:
        payment_url = await StripeService.create_checkout_session(
            user_id=user_id,
            product_id=product_id,
            product_name=product_name,
            price_cents=product_price_cents
        )

        # 3. UI NOTIFICATION LAYER: Provide the secure checkout URL link to the client
        await callback.message.answer(
            text=lexicon.LexiconEN.invoice_message(product_name,item.price),
            reply_markup=invoice_kb(product_price_cents, payment_url),
            parse_mode="HTML"
        )

    except Exception as e:
        import logging
        await callback.message.answer(lexicon.ErrorEN.payment_unreachable())
        logging.error(f"Stripe Service invocation crashed: {e}")
