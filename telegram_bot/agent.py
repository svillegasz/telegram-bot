"""Vertex AI agent management."""

from __future__ import annotations

import logging
from typing import Any

import vertexai
from vertexai import agent_engines

from config import VertexAIConfig

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages the Vertex AI agent instance."""

    def __init__(self) -> None:
        """Initialize the agent manager."""
        self._agent: Any | None = None

    @property
    def agent(self) -> Any:
        """Get the agent instance.

        Returns:
            The initialized agent.

        Raises:
            RuntimeError: If agent is not initialized.
        """
        if self._agent is None:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        return self._agent

    @property
    def is_initialized(self) -> bool:
        """Check if agent is initialized.

        Returns:
            True if agent is initialized, False otherwise.
        """
        return self._agent is not None

    def initialize(self, config: VertexAIConfig) -> None:
        """Initialize Vertex AI and get agent engine.

        Args:
            config: Vertex AI configuration.

        Raises:
            ValueError: If required configuration is missing.
            Exception: If agent initialization fails.
        """
        vertexai.init(project=config.project_id, location=config.location)
        logger.info(
            f"Initialized Vertex AI with project: {config.project_id}, "
            f"location: {config.location}"
        )

        try:
            self._agent = agent_engines.get(config.agent_id)
            logger.info(f"Successfully loaded agent: {config.agent_id}")
        except Exception as e:
            logger.error(f"Failed to load agent: {e}")
            raise


# Global agent manager instance
agent_manager = AgentManager()

