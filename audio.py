from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

LANGUAGES = {"uz":"O‘zbek", "ru":"Rus", "en":"Ingliz", "tr":"Turk", "kk":"Qozoq", "tg":"Tojik", "de":"Nemis", "fr":"Fransuz", "es":"Ispan", "it":"Italyan", "ar":"Arab", "zh-CN":"Xitoy", "ja":"Yapon", "ko":"Koreys"}

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📝 Text tarjima"), KeyboardButton(text="🖼️ Rasm tarjima")],
        [KeyboardButton(text="📄 Hujjat tarjima"), KeyboardButton(text="🎙 Voice tarjima")],
        [KeyboardButton(text="📝 History"), KeyboardButton(text="⭐ Favorites")],
        [KeyboardButton(text="🌍 Tilni tanlash"), KeyboardButton(text="👤 Profil")],
    ], resize_keyboard=True)

def source_keyboard():
    rows = [[InlineKeyboardButton(text="✨ Avtomatik aniqlash", callback_data="src:auto")]]
    items = list(LANGUAGES.items())
    rows += [[InlineKeyboardButton(text=n, callback_data=f"src:{c}") for c,n in items[i:i+2]] for i in range(0,len(items),2)]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def target_keyboard(source):
    items = [(c,n) for c,n in LANGUAGES.items() if c != source]
    rows = [[InlineKeyboardButton(text=n, callback_data=f"dst:{source}:{c}") for c,n in items[i:i+2]] for i in range(0,len(items),2)]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def favorite_keyboard(history_id: int = 0):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⭐ Saqlash", callback_data=f"fav:{history_id}")]])

