"""
Reply клавиатуры
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard(is_registered: bool = False) -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    if is_registered:
        keyboard = [
            [KeyboardButton(text="👤 Мой профиль")],
            [KeyboardButton(text="🔍 Смотреть анкеты")],
            [KeyboardButton(text="❤️ Мои лайки")],
            [KeyboardButton(text="⚙️ Настройки")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📝 Регистрация")]
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)