from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, update_user_field
from keyboards import settings_keyboard, main_menu_keyboard, cancel_keyboard

router = Router()


class SettingsStates(StatesGroup):
    waiting_niche = State()
    waiting_style = State()
    waiting_audience = State()
    waiting_tone = State()


@router.message(F.text == "⚙️ Настройки")
async def settings_menu(message: Message):
    await message.answer(
        "⚙️ **Настройки профиля**\n\n"
        "Чем больше я знаю о тебе — тем лучше контент создаю.\n\n"
        "Выбери, что хочешь настроить 👇",
        reply_markup=settings_keyboard(),
        parse_mode="Markdown"
    )


# === Настройка ниши ===
@router.callback_query(F.data == "set_niche")
async def set_niche_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.waiting_niche)
    await callback.message.answer(
        "📌 **Твоя ниша**\n\n"
        "Напиши свою нишу или сферу деятельности.\n\n"
        "Примеры:\n"
        "• Психология и коучинг\n"
        "• Фитнес и здоровый образ жизни\n"
        "• Маркетинг и SMM\n"
        "• Кулинария\n"
        "• IT и программирование\n\n"
        "Напиши свою нишу 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(SettingsStates.waiting_niche)
async def set_niche_save(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    update_user_field(message.from_user.id, "niche", message.text)
    await state.clear()
    await message.answer(
        f"✅ Ниша сохранена: **{message.text}**\n\n"
        f"Теперь я буду создавать контент с учётом твоей ниши!",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


# === Настройка стиля ===
@router.callback_query(F.data == "set_style")
async def set_style_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.waiting_style)
    await callback.message.answer(
        "🎨 **Стиль контента**\n\n"
        "Опиши, какой стиль контента тебе нужен.\n\n"
        "Примеры:\n"
        "• Экспертный, с кейсами и цифрами\n"
        "• Лёгкий, с юмором и историями\n"
        "• Провокационный и дерзкий\n"
        "• Тёплый и душевный\n\n"
        "Опиши свой стиль 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(SettingsStates.waiting_style)
async def set_style_save(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    update_user_field(message.from_user.id, "style", message.text)
    await state.clear()
    await message.answer(
        f"✅ Стиль сохранён: **{message.text}**",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


# === Настройка целевой аудитории ===
@router.callback_query(F.data == "set_audience")
async def set_audience_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.waiting_audience)
    await callback.message.answer(
        "👥 **Целевая аудитория**\n\n"
        "Опиши свою целевую аудиторию.\n\n"
        "Примеры:\n"
        "• Женщины 25-40 лет, мамы в декрете\n"
        "• Предприниматели с доходом от 300к\n"
        "• Студенты и начинающие специалисты\n\n"
        "Опиши свою ЦА 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(SettingsStates.waiting_audience)
async def set_audience_save(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    update_user_field(message.from_user.id, "target_audience", message.text)
    await state.clear()
    await message.answer(
        f"✅ Целевая аудитория сохранена: **{message.text}**",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


# === Настройка тона ===
@router.callback_query(F.data == "set_tone")
async def set_tone_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.waiting_tone)
    await callback.message.answer(
        "🗣 **Тон общения**\n\n"
        "Как бот должен общаться?\n\n"
        "Примеры:\n"
        "• Дружелюбный и экспертный\n"
        "• Строгий и деловой\n"
        "• Весёлый и неформальный\n"
        "• Вдохновляющий и мотивирующий\n\n"
        "Напиши желаемый тон 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(SettingsStates.waiting_tone)
async def set_tone_save(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    update_user_field(message.from_user.id, "tone", message.text)
    await state.clear()
    await message.answer(
        f"✅ Тон сохранён: **{message.text}**",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


# === Профиль пользователя ===
@router.callback_query(F.data == "my_profile")
async def show_profile(callback: CallbackQuery):
    user = get_user(callback.from_user.id)
    if not user:
        await callback.message.answer("❌ Профиль не найден. Напишите /start")
        return

    niche = user["niche"] or "❌ Не указана"
    style = user["style"] or "❌ Не указан"
    audience = user["target_audience"] or "❌ Не указана"
    tone = user["tone"] or "❌ Не указан"

    await callback.message.answer(
        f"📊 **Твой профиль**\n\n"
        f"👤 Имя: {user['full_name']}\n"
        f"📌 Ниша: {niche}\n"
        f"🎨 Стиль: {style}\n"
        f"👥 ЦА: {audience}\n"
        f"🗣 Тон: {tone}\n"
        f"📈 Всего запросов: {user['total_requests']}\n"
        f"📅 Зарегистрирован: {user['created_at'][:10]}",
        parse_mode="Markdown"
    )
    await callback.answer()


# === Кнопка "Назад" ===
@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.answer(
        "Выбери, что нужно 👇",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()