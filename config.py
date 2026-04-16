"""Configuration management for MiroFish.

Loads and validates environment variables, providing a central
configuration object used throughout the application.
"""

import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    # Telegram
    telegram_bot_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    telegram_chat_id: str = field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID", ""))

    # Bilibili credentials
    bilibili_sessdata: str = field(default_factory=lambda: os.getenv("BILIBILI_SESSDATA", ""))
    bilibili_bili_jct: str = field(default_factory=lambda: os.getenv("BILIBILI_BILI_JCT", ""))
    bilibili_buvid3: str = field(default_factory=lambda: os.getenv("BILIBILI_BUVID3", ""))

    # Proxy settings
    proxy_url: Optional[str] = field(default_factory=lambda: os.getenv("PROXY_URL"))

    # Polling / fetch interval in seconds
    fetch_interval: int = field(
        default_factory=lambda: int(os.getenv("FETCH_INTERVAL", "300"))
    )

    # Maximum number of items to process per cycle
    max_items_per_cycle: int = field(
        default_factory=lambda: int(os.getenv("MAX_ITEMS_PER_CYCLE", "10"))
    )

    # Storage path for tracking sent items
    data_dir: str = field(default_factory=lambda: os.getenv("DATA_DIR", "./data"))

    # Log level
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper())

    def validate(self) -> list[str]:
        """Validate required configuration values.

        Returns:
            A list of error messages. Empty list means configuration is valid.
        """
        errors: list[str] = []

        if not self.telegram_bot_token:
            errors.append("TELEGRAM_BOT_TOKEN is not set")
        if not self.telegram_chat_id:
            errors.append("TELEGRAM_CHAT_ID is not set")
        if not self.bilibili_sessdata:
            errors.append("BILIBILI_SESSDATA is not set")
        if not self.bilibili_bili_jct:
            errors.append("BILIBILI_BILI_JCT is not set")
        if not self.bilibili_buvid3:
            errors.append("BILIBILI_BUVID3 is not set")
        if self.fetch_interval < 60:
            errors.append("FETCH_INTERVAL must be at least 60 seconds")

        return errors

    def is_valid(self) -> bool:
        """Return True if configuration passes validation."""
        return len(self.validate()) == 0

    def __repr__(self) -> str:  # pragma: no cover
        """Redact sensitive fields in string representation."""
        return (
            f"Config("
            f"telegram_chat_id={self.telegram_chat_id!r}, "
            f"fetch_interval={self.fetch_interval}, "
            f"max_items_per_cycle={self.max_items_per_cycle}, "
            f"data_dir={self.data_dir!r}, "
            f"log_level={self.log_level!r}, "
            f"proxy_url={self.proxy_url!r})"
        )


# Module-level singleton
config = Config()
