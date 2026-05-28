import os

# Токен бота от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "Сюда токен бота")

# Ключ Groq (бесплатный)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "Токен грока")

# Твой Telegram ID
ADMIN_ID = int(os.getenv("ADMIN_ID", "Админ айди"))

# Модель (бесплатная и мощная)
GROQ_MODEL = "llama-3.3-70b-versatile"

# База данных
DATABASE_PATH = "database.db"
