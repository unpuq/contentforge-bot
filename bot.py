import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import init_db
from handlers import start, content, settings, admin

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Запуск бота"""

    # Инициализируем базу данных
    init_db()
    logger.info("✅ База данных инициализирована")

    # Создаём бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрируем роутеры (обработчики)
    dp.include_router(start.router)
    dp.include_router(content.router)
    dp.include_router(settings.router)
    dp.include_router(admin.router)

    logger.info("✅ ContentForge AI запущен!")

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())