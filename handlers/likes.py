"""
Обработчики лайков
"""
from aiogram import types, F, Router

from database.database import async_session
from database.crud import get_user
from utils.formatters import format_likes_list

router = Router()


@router.message(F.text == "❤️ Мои лайки")
async def show_likes(message: types.Message):
    """Показать список лайков"""
    async with async_session() as session:
        user = await get_user(session, str(message.from_user.id))

        if not user:
            await message.answer("Сначала нужно зарегистрироваться!")
            return

        text = format_likes_list(user)
        await message.answer(text, parse_mode="HTML")