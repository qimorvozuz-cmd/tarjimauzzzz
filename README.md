# TranslatorBot

Aiogram 3.22 asosidagi professional Telegram tarjimon: matn, rasm OCR, PDF/DOCX/TXT va voice/audio tarjimasi, tarix, sevimlilar va profil.

## Lokal ishga tushirish

1. Python 3.12, Tesseract OCR va FFmpeg o‘rnating.
2. `.env.example` nusxasini `.env` nomi bilan saqlang.
3. BotFather bergan tokenni `BOT_TOKEN` qatoriga yozing.
4. Quyidagilarni bajaring:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

DeepL ixtiyoriy: `DEEPL_API_KEY` bo‘sh bo‘lsa Google Translate ishlaydi. `deep-translator` Google’ning norasmiy veb interfeysidan foydalanadi; katta tijoriy yuklama uchun rasmiy Google Cloud Translation yoki DeepL tavsiya etiladi.

## Railway

GitHub’ga yuklang, Railway’da repozitoriyni tanlang va Variables bo‘limiga `BOT_TOKEN` (ixtiyoriy `DEEPL_API_KEY`) kiriting. Doimiy tarix uchun Railway Volume yarating va `DATABASE_PATH=/data/bot.db` belgilang.

## Eslatma

- Telegram botlarida “Dark UI” alohida sozlanmaydi: interfeys Telegram’ning foydalanuvchi tanlagan mavzusiga moslashadi.
- Matnli PDF tarjima qilinadi; skaner PDF uchun OCR pipeline’ni alohida kengaytirish mumkin.
- Telegram va provayder cheklovlari sabab juda katta hujjatlarni bo‘lib yuborish kerak bo‘lishi mumkin.

