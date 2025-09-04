"""
Inline клавиатуры
"""
from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.settings import TECH_TAGS


def get_role_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора роли"""
    keyboard = [
        [InlineKeyboardButton(text="👨‍🎓 Я студент", callback_data="role_student")],
        [InlineKeyboardButton(text="👨‍🏫 Я ментор", callback_data="role_mentor")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_tags_keyboard(selected_tags: List[str] = None) -> InlineKeyboardMarkup:
    """Клавиатура выбора технологий"""
    if selected_tags is None:
        selected_tags = []

    keyboard = []
    row = []
    for i, tag in enumerate(TECH_TAGS):
        emoji = "✅" if tag in selected_tags else ""
        btn_text = f"{emoji} {tag}" if emoji else tag
        row.append(InlineKeyboardButton(text=btn_text, callback_data=f"tag_{tag}"))

        if (i + 1) % 3 == 0:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="✅ Готово", callback_data="tags_done")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_profile_keyboard(liked: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура для просмотра профиля"""
    keyboard = [
        [
            InlineKeyboardButton(text="👎 Скип", callback_data="skip"),
            InlineKeyboardButton(text="❤️ Лайк" if not liked else "❤️ Уже лайкнули",
                                 callback_data="like" if not liked else "already_liked")
        ],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_skip_photo_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для пропуска фото"""
    keyboard = [
        [InlineKeyboardButton(text="⏭️ Пропустить фото", callback_data="skip_photo")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)