from loguru import logger

# Configure logging
logger.add("instagram_downloader.log", level="ERROR", format="{time} - {level} - {message}")

