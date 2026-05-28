from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
from database import get_stats, get_all_users, get_all_user_ids
from keyboards import admin_keyboard, main_menu_keyboard

router = Router()


class AdminStates(StatesGroup):
    waiting_broadcast = State()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    """Открытие админ-панели"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У тебя нет доступа к админ-панели.")
        return

    await message.answer(
        "🔐 **Админ-панель ContentForge AI**\n\n"
        "Выбери действие 👇",
        reply_markup=admin_keyboard(),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    """Статистика"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа")
        return

    stats = get_stats()

    await callback.message.answer(
        f"📊 **Статистика бота**\n\n"
        f"👥 Всего пользователей: {stats['total_users']}\n"
        f"📝 Всего запросов: {stats['total_requests']}\n"
        f"🗂 Всего генераций: {stats['total_generations']}",
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery):
    """Список пользователей"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа")
        return

    users = get_all_users()

    if not users:
        await callback.message.answer("Пользователей пока нет.")
        await callback.answer()
        return

    text = "👥 **Все пользователи:**\n\n"
    for i, user in enumerate(users[:50], 1):  # Максимум 50
        user_id, username, full_name, niche, total_requests, created_at = user
        text += (
            f"{i}. {full_name} (@{username})\n"
            f"   📌 Ниша: {niche or 'не указана'}\n"
            f"   📈 Запросов: {total_requests}\n\n"
        )

    if len(text) > 4000:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            await callback.message.answer(part, parse_mode="Markdown")
    else:
        await callback.message.answer(text, parse_mode="Markdown")

    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_start(callback: CallbackQuery, state: FSMContext):
    """Начало рассылки"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа")
        return

    await state.set_state(AdminStates.waiting_broadcast)
    await callback.message.answer(
        "📨 **Рассылка**\n\n"
        "Напиши текст сообщения для рассылки всем пользователям.\n\n"
        "Для отмены напиши: отмена",
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(AdminStates.waiting_broadcast)
async def admin_broadcast_send(message: Message, state: FSMContext):
    """Отправка рассылки"""
    if message.from_user.id != ADMIN_ID:
        return

    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("Рассылка отменена ✅", reply_markup=main_menu_keyboard())
        return

    user_ids = get_all_user_ids()
    success = 0
    failed = 0

    await message.answer(f"📨 Начинаю рассылку для {len(user_ids)} пользователей...")

    bot: Bot = message.bot

    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message.text)
            success += 1
        except Exception:
            failed += 1

    await state.clear()
    await message.answer(
        f"✅ **Рассылка завершена!**\n\n"
        f"📨 Отправлено: {success}\n"
        f"❌ Ошибок: {failed}",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )