from aiogram import types, F, Router

from database.database import async_session
from database.crud import get_user
from handlers.inline import get_back_to_menu_keyboard
from utils.formatters import format_likes_list

likes_router = Router()


@likes_router.callback_query(F.data == "my_likes")
async def show_likes(callback: types.CallbackQuery):
    """Показать список лайков"""
    async with async_session() as session:
        user = await get_user(session, str(callback.from_user.id))

        if not user:
            await callback.answer("Сначала нужно зарегистрироваться!", show_alert=True)
            return

        text = format_likes_list(user)
        await callback.message.edit_text(
            text,
            reply_markup=get_back_to_menu_keyboard(),
            parse_mode="HTML"
        )
    await callback.answer()