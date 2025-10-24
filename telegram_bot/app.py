import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.effective_user:
        user = update.effective_user
        # Use first name, and add last name if available
        full_name = user.first_name
        if user.last_name:
            full_name += f" {user.last_name}"
        
        greeting = f"Hello {full_name}! 👋 I'm a bot, please talk to me!"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=greeting)
    else:
        logging.error("No chat ID or user info found in update")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.message and update.message.text:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    else:
        logging.error("No chat ID or message text found in update")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
    else:
        logging.error("No chat ID found in update")


if __name__ == '__main__':
    # Get token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables. Please create a .env file with your token.")
    
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(echo_handler)
    
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.run_polling()