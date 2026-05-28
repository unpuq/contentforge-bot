from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)
from database import add_user, get_user
from keyboards import main_menu_keyboard

router = Router()

# Ссылка на WebApp
WEBAPP_URL = "https://unpuq.github.io/contentforge-bot/"


def webapp_main_keyboard():
    """Главное меню с кнопкой WebApp"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )],
            [
                KeyboardButton(text="🎯 Идеи контента"),
                KeyboardButton(text="📝 Написать пост")
            ],
            [
                KeyboardButton(text="🎬 Сценарий Reels"),
                KeyboardButton(text="🔄 Адаптировать контент")
            ],
            [
                KeyboardButton(text="📅 Контент-план"),
                KeyboardButton(text="⚙️ Настройки")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start"""

    user_id = message.from_user.id
    username = message.from_user.username or "нет"
    full_name = message.from_user.full_name or "Пользователь"

    add_user(user_id, username, full_name)
    user = get_user(user_id)

    if not user.get("niche"):
        await message.answer(
            f"👋 Привет, {full_name}!\n\n"
            f"Я — **ContentForge AI** ✨\n\n"
            f"Твой персональный AI контент-мейкер.\n\n"
            f"💎 Нажми **🚀 Открыть приложение** для удобного интерфейса\n"
            f"Или используй кнопки меню 👇",
            reply_markup=webapp_main_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            f"👋 С возвращением, {full_name}!\n\n"
            f"Готов создавать контент 👇",
            reply_markup=webapp_main_keyboard(),
            parse_mode="Markdown"
        )
