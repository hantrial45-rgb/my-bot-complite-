import asyncio
import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from config import BOT_TOKEN
from utils.logger import logger
from services.monitor import monitor_pending_verifications

# Import handlers
from handlers.start import start
from handlers.auth_flow import get_phone, get_code, cancel, PHONE, CODE
from handlers.withdraw import withdraw, handle_card_name, CARD_NAME
from handlers.delete_item_callback_handler import delete_item_callback_handler
from handlers.account import account, withdraw_button_callback
from utils.zipper import download_sessions
from handlers.callbacks import update_timer_callback
from handlers.cap import cap
from handlers.admin_balance import add_balance
from handlers.admin_panel import admin_panel
from handlers.admin_callbacks import (
    handle_admin_callback,
    set_support_id,
    set_channel_id,
    WAIT_SUPPORT,
    WAIT_CHANNEL
)
from handlers.admin_capacity_update import update_cap_handler, set_cap_handler, delete_cap_handler
from handlers.change_2fa import change_2fa_handler, set_2fa_handler
from handlers.help import help_command   # ✅ /help import

def main():
    """Main function to set up and run the bot."""

    async def post_init(app):
        asyncio.create_task(monitor_pending_verifications(app.bot))
        logger.info("✅ Background monitoring task started.")

    logging.basicConfig(level=logging.INFO)

    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # --- Conversation Handlers ---
    auth_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r"^\+\d{11,15}$"), get_phone)],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_code)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_chat=True,
        conversation_timeout=300,
    )

    withdraw_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("withdraw", withdraw),
            CallbackQueryHandler(withdraw_button_callback, pattern="^withdraw_request$")
        ],
        states={
            CARD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(r"^\+\d{11,15}$"), handle_card_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_chat=True,
        conversation_timeout=300,
    )

    # Admin conversation handler for updating Support/Channel ID
    admin_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_admin_callback, pattern="^change_.*|^admin_.*|bot_.*")],
        states={
            WAIT_SUPPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_support_id)],
            WAIT_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_channel_id)],
        },
        fallbacks=[],
        per_chat=True
    )

    # Register Handlers
    app.add_handler(auth_conv_handler)
    app.add_handler(withdraw_conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("account", account))
    app.add_handler(CommandHandler("download_sessions", download_sessions))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("cap", cap))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(admin_conv_handler)  # ✅ Admin conversation handler
    app.add_handler(CommandHandler("updatecap", update_cap_handler))
    app.add_handler(CommandHandler("setcap", set_cap_handler))
    app.add_handler(CommandHandler("change2fa", change_2fa_handler))
    app.add_handler(CommandHandler("set2fa", set_2fa_handler)) 
    app.add_handler(CommandHandler("addbalance", add_balance))
    app.add_handler(CommandHandler("help", help_command))   # ✅ /help command

    # CallbackQuery Handlers
    app.add_handler(CallbackQueryHandler(delete_item_callback_handler, pattern="^delete_capacity_"))
    app.add_handler(CallbackQueryHandler(handle_admin_callback))
    app.add_handler(CallbackQueryHandler(update_timer_callback))

    logger.info("🤖 Bot is starting...")
    app.run_polling()
    logger.info("Bot has stopped.")

if __name__ == "__main__":
    main()
