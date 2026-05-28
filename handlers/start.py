from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import add_user, get_user
from keyboards import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start"""

    user_id = message.from_user.id
    username = message.from_user.username or "нет"
    full_name = message.from_user.full_name or "Пользователь"

    # Добавляем пользователя в базу
    add_user(user_id, username, full_name)

    # Проверяем, новый ли пользователь
    user = get_user(user_id)

    if not user.get("niche"):
        # Новый пользователь — показываем приветствие
        await message.answer(
            f"👋 Привет, {full_name}!\n\n"
            f"Я — **ContentForge AI** 🤖\n\n"
            f"Твой персональный AI контент-мейкер.\n\n"
            f"Я умею:\n"
            f"🎯 Генерировать идеи контента\n"
            f"📝 Писать посты для Telegram, VK, Instagram\n"
            f"🎬 Делать сценарии для Reels и Shorts\n"
            f"🔄 Адаптировать контент под 5 площадок\n"
            f"📅 Составлять контент-планы\n\n"
            f"💡 **Для начала настрой меня под себя:**\n"
            f"Нажми ⚙️ Настройки и заполни свою нишу и стиль.\n\n"
            f"Или сразу начни работать! 👇",
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            f"👋 С возвращением, {full_name}!\n\n"
            f"Готов создавать контент. Выбери, что нужно 👇",
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown"
        )