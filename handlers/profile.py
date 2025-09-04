from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from database.database import async_session
from database.crud import get_user, delete_user_data
from handlers.inline import get_back_to_menu_keyboard, get_settings_keyboard, get_delete_confirmation_keyboard, get_start_keyboard  # Исправлен импорт
from utils.formatters import format_profile_with_stats

profile_router = Router()


@profile_router.callback_query(F.data == "my_profile")
async def show_profile(callback: types.CallbackQuery):
    """Показать профиль пользователя"""
    async with async_session() as session:
        user = await get_user(session, str(callback.from_user.id))

        if not user:
            await callback.answer("Сначала нужно зарегистрироваться!", show_alert=True)
            return

        profile_text = format_profile_with_stats(user)

        if user.photo_url:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=user.photo_url,
                caption=profile_text,
                reply_markup=get_back_to_menu_keyboard(),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                profile_text,
                reply_markup=get_back_to_menu_keyboard(),
                parse_mode="HTML"
            )
    await callback.answer()


@profile_router.callback_query(F.data == "settings")
async def show_settings(callback: types.CallbackQuery):
    """Показать настройки"""
    await callback.message.edit_text(
        "⚙️ <b>Настройки</b>\n\n"
        "Выберите действие:",
        reply_markup=get_settings_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@profile_router.callback_query(F.data == "delete_profile")
async def ask_delete_confirmation(callback: types.CallbackQuery):
    """Запрос подтверждения удаления"""
    await callback.message.edit_text(
        "⚠️ <b>Внимание!</b>\n\n"
        "Вы действительно хотите удалить свою анкету?\n"
        "Это действие необратимо!",
        reply_markup=get_delete_confirmation_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@profile_router.callback_query(F.data == "confirm_delete")
async def confirm_delete(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждение удаления"""
    async with async_session() as session:
        if await delete_user_data(session, callback.from_user.id):
            await state.clear()
            await callback.message.edit_text(
                "✅ Ваша анкета удалена.\n\n"
                "Хотите создать новую?",
                reply_markup=get_start_keyboard()
            )
        else:
            await callback.answer("Не удалось удалить анкету", show_alert=True)
    await callback.answer()


@profile_router.callback_query(F.data == "edit_profile")
async def edit_profile_stub(callback: types.CallbackQuery):
    """Заглушка для редактирования профиля"""
    await callback.answer("Функция в разработке", show_alert=True)