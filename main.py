#!/usr/bin/env python3
"""
MiroFish - A fishing bot/automation tool
Main entry point for the application.
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()  # changed default from INFO to DEBUG for easier local dev
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/mirofish.log", encoding="utf-8"),  # fixed: log file should go in logs/ dir
    ],
)
logger = logging.getLogger("mirofish")


def check_environment() -> bool:
    """Validate required environment variables are set."""
    required_vars = [
        "BOT_TOKEN",
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        logger.error("Please copy .env.example to .env and fill in the values.")
        return False
    return True


async def main() -> None:
    """Main async entry point for MiroFish."""
    logger.info("Starting MiroFish...")

    if not check_environment():
        sys.exit(1)

    # Import bot module after environment validation
    try:
        from bot import MiroFishBot
    except ImportError as e:
        logger.critical("Failed to import bot module: %s", e)
        sys.exit(1)

    bot_token = os.getenv("BOT_TOKEN")
    bot = MiroFishBot(token=bot_token)

    try:
        logger.info("Bot initialized. Starting polling...")
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal. Shutting down...")
    except Exception as e:
        logger.exception("Unexpected error occurred: %s", e)
        sys.exit(1)
    finally:
        await bot.stop()
        logger.info("MiroFish stopped.")


if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated by user.")
