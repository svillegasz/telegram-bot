"""Configuration management for the Telegram bot."""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass

# Constants
DEFAULT_LOCATION = 'us-central1'
DEFAULT_PORT = 8080
DEFAULT_MODE = 'polling'
TERMINATE_KEYWORD = 'TERMINATE'
TYPING_ACTION = 'typing'


@dataclass
class BotConfig:
    """Configuration for the Telegram bot."""

    token: str
    mode: str
    webhook_url: str
    port: int
    webhook_path: str


@dataclass
class VertexAIConfig:
    """Configuration for Vertex AI."""

    project_id: str
    location: str
    agent_id: str


def load_bot_config() -> BotConfig:
    """Load bot configuration from environment variables.

    Returns:
        Bot configuration.

    Raises:
        ValueError: If required configuration is missing.
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN not found in environment variables. "
            "Please create a .env file with your token."
        )

    mode = os.getenv('BOT_MODE', DEFAULT_MODE).lower()
    webhook_url = os.getenv('WEBHOOK_URL', '')
    port = int(os.getenv('PORT', str(DEFAULT_PORT)))
    webhook_path = os.getenv('WEBHOOK_PATH', str(uuid.uuid4()))

    return BotConfig(
        token=token,
        mode=mode,
        webhook_url=webhook_url,
        port=port,
        webhook_path=webhook_path,
    )


def load_vertex_ai_config() -> VertexAIConfig:
    """Load Vertex AI configuration from environment variables.

    Returns:
        Vertex AI configuration.

    Raises:
        ValueError: If required configuration is missing.
    """
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT not found in environment variables"
        )

    agent_id = os.getenv('GOOGLE_AGENT_ENGINE')
    if not agent_id:
        raise ValueError(
            "GOOGLE_AGENT_ENGINE not found in environment variables"
        )

    location = os.getenv('GOOGLE_CLOUD_LOCATION', DEFAULT_LOCATION)

    return VertexAIConfig(
        project_id=project_id,
        location=location,
        agent_id=agent_id,
    )

