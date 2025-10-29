"""Telegram bot integration with Google Vertex AI Agent Engine.

This is the main entry point for the bot application.
"""

from __future__ import annotations

import os
import logging
from typing import Any

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from agent import agent_manager
from config import BotConfig, load_bot_config, load_vertex_ai_config
from handlers import setup_handlers

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def run_webhook_mode(
    application: Any,
    config: BotConfig,
) -> None:
    """
    Start the built-in webhook server provided by python-telegram-bot.
    Application.run_webhook will create an aiohttp/tornado server (depending on extras).
    """
    port = int(os.environ.get("PORT", "8080"))
    listen = "0.0.0.0"
    # run_webhook will start the HTTP server and set the webhook with Telegram API if webhook_url provided.
    application.run_webhook(
        listen=listen,
        port=port,
        webhook_url=config.webhook_url,
    )


def run_polling_mode(application: Any) -> None:
    """Run bot in polling mode.

    Args:
        application: Telegram application instance.
    """
    logger.info("Starting bot in POLLING mode (development)")
    application.run_polling()


def main() -> None:
    """Main entry point for the bot."""
    # Load configurations
    bot_config = load_bot_config()
    vertex_ai_config = load_vertex_ai_config()

    # Initialize Vertex AI agent
    try:
        agent_manager.initialize(vertex_ai_config)
    except Exception as e:
        logger.error(f"Failed to initialize Vertex AI: {e}")
        raise

    # Build application
    application = ApplicationBuilder().token(bot_config.token).build()

    # Setup handlers
    setup_handlers(application)

    # Run in selected mode
    if bot_config.mode == 'webhook':
        run_webhook_mode(application, bot_config)
    else:
        run_polling_mode(application)


if __name__ == '__main__':
    main()