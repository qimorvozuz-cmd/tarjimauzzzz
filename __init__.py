import html
import tempfile
from pathlib import Path
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, Message
from database import db
from keyboards.main import LANGUAGES, favorite_keyboard, main_menu, source_keyboard, target_keyboard
from services.audio import transcribe
from services.documents import translate_document
from services.ocr import extract_text
from services.translator import translator

router = Router()
MENU_TEXTS = {"📝 Text tarjima", "🖼️ Rasm tarjima", "📄 Hujjat tarjima", "🎙 Voice tarjima"}

async def do_translate(message: Message, text: str):
    source, target = await db.get_languages(message.from_user.id)
    status = await message.answer("⏳ Tarjima qilinmoqda…")
    try:
        result = await translator.translate(text, source, target)
        await db.add_history(message.from_user.id, text, result, source, target)
        await status.edit_text(f"🌐 <b>{LANGUAGES.get(target,target)}</b>\n\n{html.escape(result)}", reply_markup=favorite_keyboard(), parse_mode="HTML")
    except Exception as e:
        await status.edit_text(f"❌ Tarjima amalga oshmadi: {html.escape(str(e))}", parse_mode="HTML")

@router.message(CommandStart())
async def start(message: Message):
    await db.ensure_user(message.from_user.id)
    await message.answer("👋 Professional tarjimon botga xush kelibsiz!\n\nAvval 🌍 tilni tanlang, keyin matn, rasm, audio yoki hujjat yuboring.", reply_markup=main_menu())

@router.message(F.text == "🌍 Tilni tanlash")
async def choose_language(message: Message):
    await message.answer("Matnning asl tilini tanlang:", reply_markup=source_keyboard())

@router.callback_query(F.data.startswith("src:"))
async def source_chosen(call: CallbackQuery):
    source = call.data.split(":", 1)[1]
    await call.message.edit_text("Qaysi tilga tarjima qilay?", reply_markup=target_keyboard(source))
    await call.answer()

@router.callback_query(F.data.startswith("dst:"))
async def target_chosen(call: CallbackQuery):
    _, source, target = call.data.split(":")
    await db.set_languages(call.from_user.id, source, target)
    await call.message.edit_text(f"✅ Saqlandi: {LANGUAGES.get(source,'Avtomatik')} → {LANGUAGES.get(target,target)}\nEndi istalgan matn yoki faylni yuboring.")
    await call.answer("Til saqlandi")

@router.message(F.text == "📝 History")
async def history(message: Message):
    rows = await db.get_history(message.from_user.id)
    text = "\n\n".join(f"• {html.escape(a[:120])}\n→ {html.escape(b[:180])}" for a,b,_ in rows) or "Tarjimalar tarixi bo‘sh."
    await message.answer(f"📝 <b>Oxirgi tarjimalar</b>\n\n{text}", parse_mode="HTML")

@router.message(F.text == "⭐ Favorites")
async def favorites(message: Message):
    rows = await db.get_favorites(message.from_user.id)
    text = "\n\n".join(f"⭐ {html.escape(a[:120])}\n→ {html.escape(b[:180])}" for a,b in rows) or "Sevimlilar bo‘sh."
    await message.answer(text, parse_mode="HTML")

@router.callback_query(F.data.startswith("fav:"))
async def save_favorite(call: CallbackQuery):
    rows = await db.get_history(call.from_user.id, 1)
    if rows:
        await db.add_favorite(call.from_user.id, rows[0][0], rows[0][1])
    await call.answer("⭐ Sevimlilarga saqlandi")

@router.message(F.text == "👤 Profil")
async def profile(message: Message):
    source,target = await db.get_languages(message.from_user.id)
    histories,favorites_count = await db.stats(message.from_user.id)
    await message.answer(f"👤 <b>Profil</b>\nID: <code>{message.from_user.id}</code>\nTil: {LANGUAGES.get(source,'Avtomatik')} → {LANGUAGES.get(target,target)}\nTarjimalar: {histories}\nSevimlilar: {favorites_count}", parse_mode="HTML")

@router.message(F.text.in_(MENU_TEXTS))
async def menu_hint(message: Message):
    hints = {"📝 Text tarjima":"Tarjima qilish uchun matn yuboring.", "🖼️ Rasm tarjima":"Rasmni foto sifatida yuboring.", "📄 Hujjat tarjima":"PDF, DOCX yoki TXT fayl yuboring.", "🎙 Voice tarjima":"Voice yoki audio yuboring."}
    await message.answer(hints[message.text])

@router.message(F.photo)
async def photo(message: Message, bot):
    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "image.jpg")
        await bot.download(message.photo[-1], destination=path)
        try:
            text = await extract_text(path)
            if not text: raise ValueError("Rasmdan matn topilmadi")
            await do_translate(message, text)
        except Exception as e: await message.answer(f"❌ OCR xatosi: {e}")

@router.message(F.document)
async def document(message: Message, bot):
    suffix = Path(message.document.file_name or "file").suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt"}:
        return await message.answer("❌ Faqat PDF, DOCX yoki TXT yuboring.")
    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / (message.document.file_name or f"file{suffix}"))
        await bot.download(message.document, destination=path)
        status = await message.answer("⏳ Hujjat tarjima qilinmoqda…")
        try:
            source,target = await db.get_languages(message.from_user.id)
            output = await translate_document(path, tmp, source, target)
            await message.answer_document(FSInputFile(output), caption="✅ Tarjima tayyor")
            await status.delete()
        except Exception as e: await status.edit_text(f"❌ {e}")

@router.message(F.voice | F.audio)
async def voice(message: Message, bot):
    with tempfile.TemporaryDirectory() as tmp:
        media = message.voice or message.audio
        path = str(Path(tmp) / "audio.ogg")
        await bot.download(media, destination=path)
        status = await message.answer("🎧 Audio tinglanmoqda…")
        try:
            source,_ = await db.get_languages(message.from_user.id)
            text = await transcribe(path, None if source == "auto" else source)
            await status.delete()
            await do_translate(message, text)
        except Exception as e: await status.edit_text(f"❌ Audio xatosi: {e}")

@router.message(F.text)
async def text_translation(message: Message):
    await do_translate(message, message.text)

