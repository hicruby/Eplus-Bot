from loguru import logger
import sys, os

os.makedirs("logs", exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("logs/eplus-bot.log", rotation="5 MB", retention="7 days", level="INFO")
