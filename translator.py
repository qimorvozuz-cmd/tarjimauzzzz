import asyncio
from deep_translator import GoogleTranslator, DeeplTranslator
from config import config

class TranslationService:
    async def translate(self, text: str, source: str, target: str) -> str:
        if not text.strip():
            return ""
        return await asyncio.to_thread(self._sync_translate, text, source, target)

    def _sync_translate(self, text, source, target):
        if config.deepl_api_key and target.lower() in {"bg","cs","da","de","el","en","es","et","fi","fr","hu","id","it","ja","ko","lt","lv","nb","nl","pl","pt","ro","ru","sk","sl","sv","tr","uk","zh"}:
            src = "auto" if source == "auto" else source
            return DeeplTranslator(api_key=config.deepl_api_key, source=src, target=target).translate(text)
        return GoogleTranslator(source=source, target=target).translate(text)

translator = TranslationService()

