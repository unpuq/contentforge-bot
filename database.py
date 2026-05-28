import sqlite3
from config import DATABASE_PATH
from datetime import datetime


def init_db():
    """Создание базы данных и таблиц"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            niche TEXT DEFAULT '',
            style TEXT DEFAULT '',
            target_audience TEXT DEFAULT '',
            tone TEXT DEFAULT 'дружелюбный и экспертный',
            total_requests INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_active TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Таблица истории генераций
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content_type TEXT,
            prompt TEXT,
            result TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_id: int, username: str, full_name: str):
    """Добавление нового пользователя"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, username, full_name)
        VALUES (?, ?, ?)
    """, (user_id, username, full_name))
    conn.commit()
    conn.close()


def get_user(user_id: int):
    """Получение данных пользователя"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "user_id": user[0],
            "username": user[1],
            "full_name": user[2],
            "niche": user[3],
            "style": user[4],
            "target_audience": user[5],
            "tone": user[6],
            "total_requests": user[7],
            "created_at": user[8],
            "last_active": user[9]
        }
    return None


def update_user_field(user_id: int, field: str, value: str):
    """Обновление поля пользователя"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()


def increment_requests(user_id: int):
    """Увеличение счётчика запросов"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET total_requests = total_requests + 1,
        last_active = ? WHERE user_id = ?
    """, (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()


def save_history(user_id: int, content_type: str, prompt: str, result: str):
    """Сохранение генерации в историю"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (user_id, content_type, prompt, result)
        VALUES (?, ?, ?, ?)
    """, (user_id, content_type, prompt, result))
    conn.commit()
    conn.close()


def get_all_users():
    """Получение всех пользователей"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, full_name, niche, total_requests, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def get_stats():
    """Статистика для админки"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total_requests) FROM users")
    total_requests = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM history")
    total_generations = cursor.fetchone()[0]

    conn.close()
    return {
        "total_users": total_users,
        "total_requests": total_requests,
        "total_generations": total_generations
    }


def get_all_user_ids():
    """Получение всех ID пользователей для рассылки"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ids