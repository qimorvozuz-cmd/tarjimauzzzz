import asyncio
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from config import config

if config.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = config.tesseract_cmd

async def extract_text(path: str, language: str = "eng+rus") -> str:
    def run():
        image = Image.open(path).convert("L")
        image = ImageEnhance.Contrast(image).enhance(1.8).filter(ImageFilter.SHARPEN)
        try:
            return pytesseract.image_to_string(image, lang=language).strip()
        except pytesseract.TesseractError:
            return pytesseract.image_to_string(image, lang="eng").strip()
    return await asyncio.to_thread(run)

