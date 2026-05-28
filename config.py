import os

# Токен бота от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "8747374879:AAEdsbS4zAWMqLPf38Lu3uWdQDFKaO3bgSs")

# Ключ Groq (бесплатный)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

# Твой Telegram ID
ADMIN_ID = int(os.getenv("ADMIN_ID", "1936209847"))

# Модель (бесплатная и мощная)
GROQ_MODEL = "llama-3.3-70b-versatile"

# База данных
DATABASE_PATH = "database.db"