"""
Обработчики просмотра анкет
"""
from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.database import async_session
from database.crud import get_user, get_next_profile, create_like
from keyboards.inline import get_profile_keyboard, get_main_menu_keyboard
from states.states import BrowsingStates
from utils.formatters import format_profile
from bot import bot

router = Router()


@router.callback_query(F.data == "browse_profiles")
async def start_browsing(callback: types.CallbackQuery, state: FSMContext):
    """Начать просмотр анкет"""
    async with async_session() as session:
        user = await get_user(session, str(callback.from_user.id))

        if not user:
            await callback.answer("Сначала нужно зарегистрироваться!", show_alert=True)
            return

        next_profile = await get_next_profile(session, str(callback.from_user.id))

        if not next_profile:
            await callback.message.edit_text(
                "😔 Анкеты закончились!\n"
                "Попробуйте зайти позже или измените фильтры.\n\n"
                "<i>💡 Совет: используйте команду /reset чтобы сбросить свои данные и посмотреть анкеты заново</i>",
                reply_markup=get_main_menu_keyboard(),
                parse_mode="HTML"
            )
            await callback.answer()
            return

        profile_text = format_profile(next_profile)

        if next_profile.photo_url:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=next_profile.photo_url,
                caption=profile_text,
                reply_markup=get_profile_keyboard(),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                profile_text,
                reply_markup=get_profile_keyboard(),
                parse_mode="HTML"
            )

        await state.update_data(current_profile_id=next_profile.id)
        await state.set_state(BrowsingStates.viewing_profiles)
        await callback.answer()


@router.callback_query(StateFilter(BrowsingStates.viewing_profiles))
async def handle_profile_action(callback: types.CallbackQuery, state: FSMContext):
    """Обработка действий с профилем"""
    if callback.data == "main_menu":
        await callback.message.delete()
        await callback.message.answer(
            "Главное меню:",
            reply_markup=get_main_menu_keyboard()
        )
        await state.clear()
        await callback.answer()
        return

    data = await state.get_data()
    current_profile_id = data.get('current_profile_id')

    async with async_session() as session:
        if callback.data == "like":
            is_mutual, liked_user = await create_like(
                session,
                str(callback.from_user.id),
                current_profile_id
            )

            if is_mutual and liked_user:
                # Получаем лайкера для отправки уведомления
                liker = await get_user(session, str(callback.from_user.id))

                await callback.answer("❤️ Это взаимный лайк! Обоим отправлены уведомления!", show_alert=True)

                # Отправляем уведомление второму пользователю
                try:
                    mutual_text = (
                        f"🎉 <b>У вас взаимный лайк!</b>\n\n"
                        f"{format_profile(liker)}\n"
                        f"Напишите первым: @{callback.from_user.username or 'username_not_set'}"
                    )
                    await bot.send_message(liked_user.telegram_id, mutual_text, parse_mode="HTML")

                    # Отправляем уведомление текущему пользователю
                    current_user_text = (
                        f"🎉 <b>У вас взаимный лайк!</b>\n\n"
                        f"{format_profile(liked_user)}\n"
                        f"Теперь вы можете начать общение!"
                    )
                    await callback.message.answer(current_user_text, parse_mode="HTML")
                except:
                    pass  # Пользователь мог заблокировать бота
            else:
                await callback.answer("❤️ Лайк отправлен!")

        elif callback.data == "skip":
            await callback.answer("Пропускаем...")

        # Показываем следующий профиль
        next_profile = await get_next_profile(session, str(callback.from_user.id))

        if not next_profile:
            if callback.message.photo:
                await callback.message.delete()
                await callback.message.answer(
                    "😔 Анкеты закончились!\n"
                    "Попробуйте зайти позже.",
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                await callback.message.edit_text(
                    "😔 Анкеты закончились!\n"
                    "Попробуйте зайти позже.",
                    reply_markup=get_main_menu_keyboard()
                )
            await state.clear()
            await callback.answer()
            return

        profile_text = format_profile(next_profile)

        # Если текущее сообщение с фото или следующий профиль с фото - удаляем и создаем новое
        if callback.message.photo or next_profile.photo_url:
            await callback.message.delete()
            if next_profile.photo_url:
                await callback.message.answer_photo(
                    photo=next_profile.photo_url,
                    caption=profile_text,
                    reply_markup=get_profile_keyboard(),
                    parse_mode="HTML"
                )
            else:
                await callback.message.answer(
                    profile_text,
                    reply_markup=get_profile_keyboard(),
                    parse_mode="HTML"
                )
        else:
            # Если оба без фото - просто редактируем текст
            await callback.message.edit_text(
                profile_text,
                reply_markup=get_profile_keyboard(),
                parse_mode="HTML"
            )

        await state.update_data(current_profile_id=next_profile.id)
        await callback.answer()