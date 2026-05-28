from groq import AsyncGroq
from config import GROQ_API_KEY, GROQ_MODEL
from database import get_user

# Создаём клиент Groq
client = AsyncGroq(api_key=GROQ_API_KEY)


def build_system_prompt(user_data: dict, content_type: str) -> str:
    """Строим мощный системный промпт под пользователя"""

    niche = user_data.get("niche", "") or "не указана"
    style = user_data.get("style", "") or "не указан"
    audience = user_data.get("target_audience", "") or "не указана"
    tone = user_data.get("tone", "") or "дружелюбный и экспертный"

    base = f"""Ты — профессиональный AI контент-мейкер мирового уровня.
Ты создаёшь вирусный, цепляющий, продающий контент.

Данные о пользователе:
- Ниша: {niche}
- Стиль контента: {style}
- Целевая аудитория: {audience}
- Тон: {tone}

Правила:
1. Пиши на русском языке
2. Используй простой и понятный язык
3. Добавляй эмодзи где уместно
4. Делай контент, который хочется сохранить и репостнуть
5. Каждый текст должен цеплять с первой строки
"""

    if content_type == "ideas":
        base += """
Сейчас тебя попросят сгенерировать идеи для контента.
Дай 10 конкретных идей с короткими описаниями.
Для каждой идеи укажи:
- Название/тема
- Формат (пост, reels, stories, carousel)
- Почему зайдёт аудитории (1 предложение)
"""
    elif content_type == "post":
        base += """
Сейчас тебя попросят написать пост.
Структура поста:
1. Цепляющий заголовок (крючок)
2. Вступление, которое создаёт интригу
3. Основная часть с пользой/историей
4. Сильный вывод или призыв к действию
5. 3-5 релевантных хэштегов

Длина: 1000-1500 символов (оптимально для Telegram/VK).
"""
    elif content_type == "reels":
        base += """
Сейчас тебя попросят написать сценарий Reels/Shorts.
Структура:
1. HOOK (первые 3 секунды) — самое важное
2. ОСНОВНАЯ ЧАСТЬ (15-45 секунд)
3. CALL TO ACTION (последние 3-5 секунд)

Для каждой части укажи:
- Что говорить (текст)
- Что показывать на экране
- Субтитры
- Рекомендации по музыке/эффектам

Длина: 30-60 секунд.
"""
    elif content_type == "adapt":
        base += """
Сейчас тебя попросят адаптировать контент под разные площадки.
Адаптируй текст под 5 площадок:
1. Telegram
2. ВКонтакте
3. Instagram (Reels/пост)
4. YouTube (Shorts/Community)
5. TikTok

Для каждой площадки учитывай специфику, длину и стиль.
"""
    elif content_type == "plan":
        base += """
Сейчас тебя попросят составить контент-план.
Создай подробный контент-план в формате таблицы:
- День недели
- Тема
- Формат (пост/reels/stories/carousel)
- Цель (вовлечение/продажа/экспертность/личное)
- Краткое описание

Чередуй форматы и цели для максимального эффекта.
"""

    return base


async def generate_content(user_id: int, content_type: str, user_message: str) -> str:
    """Генерация контента через Groq"""

    user_data = get_user(user_id)
    if not user_data:
        return "❌ Ошибка: пользователь не найден. Напишите /start"

    system_prompt = build_system_prompt(user_data, content_type)

    try:
        response = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=4000,
            temperature=0.8
        )

        result = response.choices[0].message.content
        return result

    except Exception as e:
        return f"❌ Ошибка генерации: {str(e)}\n\nПопробуйте ещё раз."