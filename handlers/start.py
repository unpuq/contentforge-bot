from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from database import add_user, get_user
from keyboards import main_menu_keyboard

router = Router()

# Ссылка на твой WebApp
WEBAPP_URL = "https://unpuq.github.io/contentforge-bot/"


def webapp_keyboard():
    """Кнопка открытия WebApp"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ]
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
            f"💎 **Открой приложение** — там удобный интерфейс:",
            reply_markup=webapp_keyboard(),
            parse_mode="Markdown"
        )

        await message.answer(
            f"Или используй обычное меню 👇",
            reply_markup=main_menu_keyboard()
        )
    else:
        await message.answer(
            f"👋 С возвращением, {full_name}!\n\n"
            f"💎 Открой приложение для удобной работы:",
            reply_markup=webapp_keyboard(),
            parse_mode="Markdown"
        )

        await message.answer(
            f"Готов создавать контент 👇",
            reply_markup=main_menu_keyboard()
        )
