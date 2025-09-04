"""
Обработчики профиля пользователя
"""
from aiogram import types, F, Router

from database.database import async_session
from database.crud import get_user
from utils.formatters import format_profile_with_stats

router = Router()


@router.message(F.text == "👤 Мой профиль")
async def show_profile(message: types.Message):
    """Показать профиль пользователя"""
    async with async_session() as session:
        user = await get_user(session, str(message.from_user.id))

        if not user:
            await message.answer("Сначала нужно зарегистрироваться!")
            return

        profile_text = format_profile_with_stats(user)

        if user.photo_url:
            await message.answer_photo(
                photo=user.photo_url,
                caption=profile_text,
                parse_mode="HTML"
            )
        else:
            await message.answer(
                profile_text,
                parse_mode="HTML"
            )