import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import stripe
from config import TELEGRAM_TOKEN, STRIPE_SECRET_KEY, DOMAIN
from database import init_db, set_user_active, is_user_active

stripe.api_key = STRIPE_SECRET_KEY
init_db()

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if is_user_active(telegram_id):
        await update.message.reply_text("Ya tienes acceso activo. ¡Gracias!")
    else:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Suscripción mensual al bot"},
                    "unit_amount": 500,
                    "recurring": {"interval": "month"}
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{DOMAIN}/success?user_id={telegram_id}",
            cancel_url=f"{DOMAIN}/cancel",
            metadata={"telegram_id": telegram_id}
        )
        keyboard = [[InlineKeyboardButton("Pagar suscripción", url=session.url)]]
        await update.message.reply_text("Haz clic para suscribirte:", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
