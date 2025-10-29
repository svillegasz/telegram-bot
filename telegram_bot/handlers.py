"""Telegram message and command handlers."""

from __future__ import annotations

import logging
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from agent import agent_manager
from config import TERMINATE_KEYWORD
from utils import (
    delete_session,
    extract_response_text,
    get_chat_id,
    get_user_id,
    handle_terminate_response,
    prepare_user_message,
    send_message,
    send_typing_action,
)

logger = logging.getLogger(__name__)


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Handle all user messages - starts, continues, and ends conversations.

    Args:
        update: Telegram update object.
        context: Telegram context.
    """
    # Validate update
    if not update.effective_chat or not update.message or not update.message.text:
        logger.error("No chat ID or message text found in update")
        return

    # Check agent initialization
    if not agent_manager.is_initialized:
        chat_id = get_chat_id(update)
        await send_message(
            context,
            chat_id,
            "Sorry, the AI agent is not initialized. "
            "Please contact the administrator.",
        )
        return

    user_id = get_user_id(update)
    chat_id = get_chat_id(update)

    # Initialize user_data if needed
    if context.user_data is None:
        context.user_data = {}

    # Check if session exists, create if not (start conversation)
    session = context.user_data.get('session')
    is_first_message = False

    if not session:
        logger.info(f"Starting new conversation for user {user_id}")
        try:
            session = agent_manager.agent.create_session(user_id=str(user_id))
            context.user_data['session'] = session
            is_first_message = True
            logger.info(
                f"Created new session for user {user_id}: {session['id']}"
            )
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            await send_message(
                context,
                chat_id,
                "Sorry, I couldn't start a conversation. Please try again later.",
            )
            return

    # Prepare the message - add greeting for first message
    user_message = prepare_user_message(
        update.message.text,
        is_first_message,
        update.effective_user.first_name if update.effective_user else None,
    )

    if is_first_message:
        logger.info(f"First message with greeting for user {user_id}")

    try:
        # Send typing indicator
        await send_typing_action(context, chat_id)

        logger.info(f"User {user_id} sent: {update.message.text}")

        # Stream query the agent with session
        events = agent_manager.agent.stream_query(
            user_id=str(user_id),
            session_id=session['id'],
            message=user_message,
        )
        response_text = extract_response_text(events)

        logger.info(f"Agent response to user {user_id}: {response_text[:100]}...")

        # Check if we got a response
        if not response_text:
            logger.warning(
                f"No response text received from agent for user {user_id}"
            )
            await send_message(
                context,
                chat_id,
                "Sorry, I didn't receive a response. Please try again.",
            )
            return

        # Check if response contains TERMINATE (end conversation)
        if TERMINATE_KEYWORD in response_text:
            await handle_terminate_response(
                response_text,
                context,
                chat_id,
                str(user_id),
                session['id'],
            )
            return

        # Send response to user (continue conversation)
        await send_message(context, chat_id, response_text)

    except Exception as e:
        logger.error(f"Error querying agent: {e}", exc_info=True)
        await send_message(
            context,
            chat_id,
            "Sorry, I encountered an error processing your message. "
            "Please try again.",
        )


async def handle_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Handle commands - clean up session if exists.

    Args:
        update: Telegram update object.
        context: Telegram context.
    """
    if not update.effective_chat:
        return

    user_id = get_user_id(update)
    chat_id = get_chat_id(update)

    # Clean up session from context if exists
    session_exists = (
        context.user_data is not None
        and 'session' in context.user_data
        and context.user_data.get('session')
    )

    if session_exists and context.user_data is not None:
        session = context.user_data['session']
        await delete_session(str(user_id), session['id'])
        context.user_data.pop('session', None)

        await send_message(
            context,
            chat_id,
            "Conversation ended. Send me a message anytime to start a new "
            "conversation!",
        )
    else:
        await send_message(
            context,
            chat_id,
            "No active conversation. Send me a message to start chatting!",
        )


def setup_handlers(application: Any) -> None:
    """Configure bot handlers.

    Args:
        application: Telegram application instance.
    """
    # Handle all text messages
    message_handler = MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message,
    )
    application.add_handler(message_handler)

    # Handle commands (to end conversation)
    command_handler = MessageHandler(filters.COMMAND, handle_command)
    application.add_handler(command_handler)

