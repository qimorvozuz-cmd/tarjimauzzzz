from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    deepl_api_key: str = os.getenv("DEEPL_API_KEY", "")
    database_path: str = os.getenv("DATABASE_PATH", "data/bot.db")
    tesseract_cmd: str = os.getenv("TESSERACT_CMD", "")
    max_file_mb: int = int(os.getenv("MAX_FILE_MB", "20"))

config = Config()

