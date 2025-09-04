from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.settings import TECH_TAGS


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для начала работы"""
    keyboard = [
        [InlineKeyboardButton(text="🚀 Начать", callback_data="start_registration")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню в виде inline кнопок"""
    keyboard = [
        [InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile")],
        [InlineKeyboardButton(text="🔍 Смотреть анкеты", callback_data="browse_profiles")],
        [InlineKeyboardButton(text="❤️ Мои лайки", callback_data="my_likes")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


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


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Кнопка возврата в главное меню"""
    keyboard = [
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура настроек"""
    keyboard = [
        [InlineKeyboardButton(text="✏️ Изменить анкету", callback_data="edit_profile")],
        [InlineKeyboardButton(text="🗑️ Удалить анкету", callback_data="delete_profile")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_delete_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Да, удалить", callback_data="confirm_delete"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)