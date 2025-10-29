"""Utility functions for Telegram bot operations."""

from __future__ import annotations

import logging
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from agent import agent_manager
from config import TERMINATE_KEYWORD, TYPING_ACTION

logger = logging.getLogger(__name__)


def get_user_id(update: Update) -> int:
    """Extract user ID from update.

    Args:
        update: Telegram update object.

    Returns:
        User ID or 0 if not available.
    """
    return update.effective_user.id if update.effective_user else 0


def get_chat_id(update: Update) -> int:
    """Extract chat ID from update.

    Args:
        update: Telegram update object.

    Returns:
        Chat ID.

    Raises:
        ValueError: If chat ID is not available.
    """
    if not update.effective_chat:
        raise ValueError("No chat ID available in update")
    return update.effective_chat.id


async def send_message(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
) -> None:
    """Send a message to a chat.

    Args:
        context: Telegram context.
        chat_id: Chat ID to send message to.
        text: Message text.
    """
    await context.bot.send_message(chat_id=chat_id, text=text)


async def send_typing_action(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
) -> None:
    """Send typing action to a chat.

    Args:
        context: Telegram context.
        chat_id: Chat ID to send action to.
    """
    await context.bot.send_chat_action(chat_id=chat_id, action=TYPING_ACTION)


def prepare_user_message(
    message_text: str,
    is_first_message: bool,
    user_first_name: str | None,
) -> str:
    """Prepare user message with greeting if first message.

    Args:
        message_text: Original message text.
        is_first_message: Whether this is the first message in session.
        user_first_name: User's first name.

    Returns:
        Prepared message text.
    """
    if not is_first_message:
        return message_text

    full_name = user_first_name or "there"
    return f"Hello, my name is {full_name}. {message_text}"


def extract_response_text(events: Any) -> str:
    """Extract text from agent response events.

    Args:
        events: Stream of events from agent.

    Returns:
        Concatenated response text.
    """
    response_text = ""
    for event in events:
        if "content" in event and "parts" in event["content"]:
            for part in event["content"]["parts"]:
                if "text" in part:
                    response_text += part["text"]
    return response_text


async def delete_session(
    user_id: str,
    session_id: str,
) -> None:
    """Delete a user session.

    Args:
        user_id: User ID.
        session_id: Session ID to delete.
    """
    try:
        agent_manager.agent.delete_session(
            user_id=user_id,
            session_id=session_id,
        )
        logger.info(f"Deleted session for user {user_id}")
    except Exception as e:
        logger.warning(f"Error deleting session: {e}")


async def handle_terminate_response(
    response_text: str,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    user_id: str,
    session_id: str,
) -> None:
    """Handle TERMINATE keyword in response.

    Args:
        response_text: Agent response text.
        context: Telegram context.
        chat_id: Chat ID.
        user_id: User ID.
        session_id: Session ID.
    """
    logger.info(f"TERMINATE detected - ending conversation for user {user_id}")

    # Remove TERMINATE from the response before sending
    clean_response = response_text.replace(TERMINATE_KEYWORD, "").strip()

    if clean_response:
        await send_message(context, chat_id, clean_response)

    # Clean up session
    await delete_session(user_id, session_id)

    # Remove session from context
    if context.user_data:
        context.user_data.pop('session', None)

