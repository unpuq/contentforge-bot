from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, increment_requests, save_history
from services.openai_service import generate_content
from keyboards import main_menu_keyboard, cancel_keyboard, content_plan_keyboard

router = Router()


# === Состояния (FSM) ===
class ContentStates(StatesGroup):
    waiting_ideas_topic = State()
    waiting_post_topic = State()
    waiting_reels_topic = State()
    waiting_adapt_text = State()
    waiting_plan_topic = State()


# === ГЕНЕРАЦИЯ ИДЕЙ ===
@router.message(F.text == "🎯 Идеи контента")
async def ideas_start(message: Message, state: FSMContext):
    await state.set_state(ContentStates.waiting_ideas_topic)
    await message.answer(
        "🎯 **Генерация идей контента**\n\n"
        "Напиши тему или нишу, для которой нужны идеи.\n\n"
        "Примеры:\n"
        "• «идеи для психолога про тревожность»\n"
        "• «контент для фитнес-тренера»\n"
        "• «посты для кофейни»\n\n"
        "Или просто напиши свою тему 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )


@router.message(ContentStates.waiting_ideas_topic)
async def ideas_generate(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    await message.answer("⏳ Генерирую идеи... Подожди 10-20 секунд")

    result = await generate_content(
        user_id=message.from_user.id,
        content_type="ideas",
        user_message=f"Сгенерируй 10 идей контента на тему: {message.text}"
    )

    # Сохраняем в историю
    increment_requests(message.from_user.id)
    save_history(message.from_user.id, "ideas", message.text, result)

    await state.clear()
    await message.answer(result, reply_markup=main_menu_keyboard(), parse_mode="Markdown")


# === НАПИСАТЬ ПОСТ ===
@router.message(F.text == "📝 Написать пост")
async def post_start(message: Message, state: FSMContext):
    await state.set_state(ContentStates.waiting_post_topic)
    await message.answer(
        "📝 **Написание поста**\n\n"
        "Напиши тему поста или о чём он должен быть.\n\n"
        "Примеры:\n"
        "• «пост о том, почему клиенты уходят»\n"
        "• «мотивационный пост для предпринимателей»\n"
        "• «пост-знакомство для нового блога»\n\n"
        "Чем подробнее опишешь — тем лучше результат 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )


@router.message(ContentStates.waiting_post_topic)
async def post_generate(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    await message.answer("⏳ Пишу пост... Подожди 15-25 секунд")

    result = await generate_content(
        user_id=message.from_user.id,
        content_type="post",
        user_message=f"Напиши продающий/экспертный пост на тему: {message.text}"
    )

    increment_requests(message.from_user.id)
    save_history(message.from_user.id, "post", message.text, result)

    await state.clear()
    await message.answer(result, reply_markup=main_menu_keyboard(), parse_mode="Markdown")


# === СЦЕНАРИЙ REELS ===
@router.message(F.text == "🎬 Сценарий Reels")
async def reels_start(message: Message, state: FSMContext):
    await state.set_state(ContentStates.waiting_reels_topic)
    await message.answer(
        "🎬 **Сценарий для Reels / Shorts**\n\n"
        "Напиши тему для видео.\n\n"
        "Примеры:\n"
        "• «3 ошибки в продажах»\n"
        "• «утренняя рутина предпринимателя»\n"
        "• «как я заработал первые 100к»\n\n"
        "Опиши тему 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )


@router.message(ContentStates.waiting_reels_topic)
async def reels_generate(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    await message.answer("⏳ Пишу сценарий... Подожди 15-25 секунд")

    result = await generate_content(
        user_id=message.from_user.id,
        content_type="reels",
        user_message=f"Напиши сценарий Reels/Shorts на тему: {message.text}"
    )

    increment_requests(message.from_user.id)
    save_history(message.from_user.id, "reels", message.text, result)

    await state.clear()
    await message.answer(result, reply_markup=main_menu_keyboard(), parse_mode="Markdown")


# === АДАПТАЦИЯ КОНТЕНТА ===
@router.message(F.text == "🔄 Адаптировать контент")
async def adapt_start(message: Message, state: FSMContext):
    await state.set_state(ContentStates.waiting_adapt_text)
    await message.answer(
        "🔄 **Адаптация контента под 5 площадок**\n\n"
        "Отправь мне готовый текст (пост, статью, заметку),\n"
        "и я адаптирую его под:\n\n"
        "1. Telegram\n"
        "2. ВКонтакте\n"
        "3. Instagram\n"
        "4. YouTube\n"
        "5. TikTok\n\n"
        "Вставь текст 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )


@router.message(ContentStates.waiting_adapt_text)
async def adapt_generate(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    await message.answer("⏳ Адаптирую под 5 площадок... Подожди 20-30 секунд")

    result = await generate_content(
        user_id=message.from_user.id,
        content_type="adapt",
        user_message=f"Адаптируй этот контент под 5 площадок:\n\n{message.text}"
    )

    increment_requests(message.from_user.id)
    save_history(message.from_user.id, "adapt", message.text[:100], result)

    await state.clear()
    await message.answer(result, reply_markup=main_menu_keyboard(), parse_mode="Markdown")


# === КОНТЕНТ-ПЛАН ===
@router.message(F.text == "📅 Контент-план")
async def plan_start(message: Message, state: FSMContext):
    await message.answer(
        "📅 **Контент-план**\n\n"
        "Выбери период:",
        reply_markup=content_plan_keyboard(),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith("plan_"))
async def plan_period_selected(callback: CallbackQuery, state: FSMContext):
    period_map = {
        "plan_week": "на 7 дней",
        "plan_2weeks": "на 14 дней",
        "plan_month": "на 30 дней"
    }
    period = period_map.get(callback.data, "на 7 дней")

    await state.update_data(plan_period=period)
    await state.set_state(ContentStates.waiting_plan_topic)

    await callback.message.answer(
        f"📅 Контент-план **{period}**\n\n"
        f"Напиши тему/нишу для контент-плана 👇",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(ContentStates.waiting_plan_topic)
async def plan_generate(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Отменено ✅", reply_markup=main_menu_keyboard())
        return

    data = await state.get_data()
    period = data.get("plan_period", "на 7 дней")

    await message.answer(f"⏳ Составляю контент-план {period}... Подожди 20-40 секунд")

    result = await generate_content(
        user_id=message.from_user.id,
        content_type="plan",
        user_message=f"Составь подробный контент-план {period} на тему: {message.text}"
    )

    increment_requests(message.from_user.id)
    save_history(message.from_user.id, "plan", message.text, result)

    await state.clear()

    # Если текст длинный — разбиваем на части
    if len(result) > 4000:
        parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
        for part in parts:
            await message.answer(part, reply_markup=main_menu_keyboard())
    else:
        await message.answer(result, reply_markup=main_menu_keyboard(), parse_mode="Markdown")



# === ОБРАБОТКА WEBAPP ===
import json

@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """Обработка данных из WebApp"""
    
    try:
        data = json.loads(message.web_app_data.data)
        content_type = data.get("type", "ideas")
        user_text = data.get("text", "")
        
        if not user_text:
            await message.answer("❌ Не указана тема")
            return
        
        type_names = {
            "ideas": "🎯 Генерирую идеи",
            "post": "📝 Пишу пост",
            "reels": "🎬 Создаю сценарий Reels",
            "plan": "📅 Составляю контент-план"
        }
        
        status_msg = await message.answer(
            f"{type_names.get(content_type, '⏳ Генерирую')}... Подожди 15-30 секунд"
        )
        
        if content_type == "plan":
            user_message = f"Составь подробный контент-план на 7 дней на тему: {user_text}"
        else:
            user_message = user_text
        
        result = await generate_content(
            user_id=message.from_user.id,
            content_type=content_type,
            user_message=user_message
        )
        
        increment_requests(message.from_user.id)
        save_history(message.from_user.id, content_type, user_text, result)
        
        await status_msg.delete()
        
        if len(result) > 4000:
            parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
            for part in parts:
                await message.answer(part, reply_markup=main_menu_keyboard())
        else:
            await message.answer(result, reply_markup=main_menu_keyboard(), parse_mode="Markdown")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
