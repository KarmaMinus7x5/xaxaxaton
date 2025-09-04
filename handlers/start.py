"""
Обработчики команды /start и /reset
"""
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.database import async_session
from database.crud import get_user, delete_user_data
from keyboards.inline import get_start_keyboard, get_main_menu_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()

    async with async_session() as session:
        user = await get_user(session, str(message.from_user.id))

        if user:
            await message.answer(
                f"С возвращением, {user.full_name}! 👋\n\n"
                "Выберите действие:",
                reply_markup=get_main_menu_keyboard(),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "👋 Добро пожаловать в <b>MentorMatch</b>!\n\n"
                "Это бот для поиска менторов и студентов.\n"
                "Здесь вы можете найти опытного наставника или талантливого студента для совместной работы над проектами.\n\n"
                "Готовы начать?",
                reply_markup=get_start_keyboard(),
                parse_mode="HTML"
            )


@router.callback_query(F.data == "start_registration")
async def start_registration_callback(callback: types.CallbackQuery):
    """Обработка нажатия кнопки Начать"""
    from keyboards.inline import get_role_keyboard
    from states.states import RegistrationStates

    await callback.message.edit_text(
        "Отлично! Давайте создадим вашу анкету.\n"
        "Для начала выберите вашу роль:",
        reply_markup=get_role_keyboard()
    )
    await callback.answer()
    await callback.message.bot.state.set_state(callback.from_user.id, RegistrationStates.choosing_role, callback.message.chat.id)


@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: types.CallbackQuery, state: FSMContext):
    """Показать главное меню"""
    await state.clear()

    async with async_session() as session:
        user = await get_user(session, str(callback.from_user.id))

        if user:
            await callback.message.edit_text(
                "Главное меню:",
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await callback.message.edit_text(
                "Вы еще не зарегистрированы.\n"
                "Хотите начать?",
                reply_markup=get_start_keyboard()
            )
    await callback.answer()


@router.message(Command("reset"))
async def cmd_reset(message: types.Message, state: FSMContext):
    """Команда для сброса данных пользователя (для тестирования)"""
    async with async_session() as session:
        if await delete_user_data(session, message.from_user.id):
            await message.answer(
                "✅ Ваши данные сброшены.\n"
                "Хотите зарегистрироваться заново?",
                reply_markup=get_start_keyboard()
            )
        else:
            await message.answer("Нечего сбрасывать.")
    await state.clear()