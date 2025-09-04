"""
Обработчики команды /start и /reset
"""
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.database import async_session
from database.crud import get_user, delete_user_data
from keyboards.reply import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()

    async with async_session() as session:
        user = await get_user(session, str(message.from_user.id))

        if user:
            await message.answer(
                f"С возвращением, {user.full_name}! 👋\n"
                "Выберите действие из меню:",
                reply_markup=get_main_keyboard(True),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "👋 Добро пожаловать в <b>MentorMatch</b>!\n\n"
                "Это бот для поиска менторов и студентов.\n"
                "Начните с регистрации!",
                reply_markup=get_main_keyboard(False),
                parse_mode="HTML"
            )


@router.message(Command("reset"))
async def cmd_reset(message: types.Message, state: FSMContext):
    """Команда для сброса данных пользователя (для тестирования)"""
    async with async_session() as session:
        if await delete_user_data(session, message.from_user.id):
            await message.answer(
                "✅ Ваши данные сброшены. Можете зарегистрироваться заново.",
                reply_markup=get_main_keyboard(False)
            )
        else:
            await message.answer("Нечего сбрасывать.")
    await state.clear()