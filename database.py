import aiosqlite
from pathlib import Path
from config import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
 user_id INTEGER PRIMARY KEY, source_lang TEXT NOT NULL DEFAULT 'auto',
 target_lang TEXT NOT NULL DEFAULT 'uz', created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS history (
 id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
 source_text TEXT NOT NULL, translated_text TEXT NOT NULL,
 source_lang TEXT, target_lang TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS favorites (
 id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
 source_text TEXT NOT NULL, translated_text TEXT NOT NULL,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

class Database:
    def __init__(self, path: str = config.database_path):
        self.path = path

    async def init(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.path) as db:
            await db.executescript(SCHEMA)
            await db.commit()

    async def ensure_user(self, user_id: int):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
            await db.commit()

    async def set_languages(self, user_id: int, source: str, target: str):
        await self.ensure_user(user_id)
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE users SET source_lang=?, target_lang=? WHERE user_id=?", (source, target, user_id))
            await db.commit()

    async def get_languages(self, user_id: int):
        await self.ensure_user(user_id)
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT source_lang,target_lang FROM users WHERE user_id=?", (user_id,))
            return await cur.fetchone()

    async def add_history(self, user_id, source_text, translated_text, source_lang, target_lang):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("INSERT INTO history(user_id,source_text,translated_text,source_lang,target_lang) VALUES(?,?,?,?,?)", (user_id, source_text[:5000], translated_text[:5000], source_lang, target_lang))
            await db.commit()

    async def get_history(self, user_id, limit=10):
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT source_text,translated_text,created_at FROM history WHERE user_id=? ORDER BY id DESC LIMIT ?", (user_id, limit))
            return await cur.fetchall()

    async def add_favorite(self, user_id, source_text, translated_text):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("INSERT INTO favorites(user_id,source_text,translated_text) VALUES(?,?,?)", (user_id, source_text, translated_text))
            await db.commit()

    async def get_favorites(self, user_id, limit=20):
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT source_text,translated_text FROM favorites WHERE user_id=? ORDER BY id DESC LIMIT ?", (user_id, limit))
            return await cur.fetchall()

    async def stats(self, user_id):
        async with aiosqlite.connect(self.path) as db:
            h = await (await db.execute("SELECT COUNT(*) FROM history WHERE user_id=?", (user_id,))).fetchone()
            f = await (await db.execute("SELECT COUNT(*) FROM favorites WHERE user_id=?", (user_id,))).fetchone()
            return h[0], f[0]

db = Database()

