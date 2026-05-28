from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def main_menu_keyboard():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
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


def settings_keyboard():
    """Клавиатура настроек"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📌 Изменить нишу", callback_data="set_niche")],
            [InlineKeyboardButton(text="🎨 Изменить стиль", callback_data="set_style")],
            [InlineKeyboardButton(text="👥 Целевая аудитория", callback_data="set_audience")],
            [InlineKeyboardButton(text="🗣 Тон общения", callback_data="set_tone")],
            [InlineKeyboardButton(text="📊 Мой профиль", callback_data="my_profile")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ]
    )
    return keyboard


def cancel_keyboard():
    """Кнопка отмены"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )
    return keyboard


def admin_keyboard():
    """Админ-панель"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton(text="👥 Все пользователи", callback_data="admin_users")],
            [InlineKeyboardButton(text="📨 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ]
    )
    return keyboard


def content_plan_keyboard():
    """Выбор периода контент-плана"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 На неделю (7 дней)", callback_data="plan_week")],
            [InlineKeyboardButton(text="📅 На 2 недели (14 дней)", callback_data="plan_2weeks")],
            [InlineKeyboardButton(text="📅 На месяц (30 дней)", callback_data="plan_month")]
        ]
    )
    return keyboard