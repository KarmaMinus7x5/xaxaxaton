"""
Обработчики регистрации пользователей
"""
from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.database import async_session
from database.crud import get_user, create_user
from keyboards.reply import get_main_keyboard
from keyboards.inline import get_role_keyboard, get_tags_keyboard, get_skip_photo_keyboard
from states.states import RegistrationStates
from utils.formatters import format_profile

router = Router()


@router.message(F.text == "📝 Регистрация")
async def start_registration(message: types.Message, state: FSMContext):
    """Начало регистрации"""
    async with async_session() as session:
        user = await get_user(session, str(message.from_user.id))

        if user:
            await message.answer("Вы уже зарегистрированы!")
            return

    await message.answer(
        "Отлично! Давайте создадим вашу анкету.\n"
        "Для начала выберите вашу роль:",
        reply_markup=get_role_keyboard()
    )
    await state.set_state(RegistrationStates.choosing_role)


@router.callback_query(StateFilter(RegistrationStates.choosing_role))
async def process_role_choice(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора роли"""
    role = "student" if callback.data == "role_student" else "mentor"
    await state.update_data(role=role)

    await callback.message.edit_text(
        f"Вы выбрали: {'Студент' if role == 'student' else 'Ментор'}\n\n"
        "Теперь введите ваше полное имя:"
    )
    await state.set_state(RegistrationStates.entering_name)


@router.message(StateFilter(RegistrationStates.entering_name))
async def process_name(message: types.Message, state: FSMContext):
    """Обработка ввода имени"""
    await state.update_data(name=message.text)

    await message.answer(
        "Отлично! Теперь расскажите немного о себе.\n"
        "Напишите краткое описание (или отправьте '-' чтобы пропустить):"
    )
    await state.set_state(RegistrationStates.entering_description)


@router.message(StateFilter(RegistrationStates.entering_description))
async def process_description(message: types.Message, state: FSMContext):
    """Обработка описания"""
    description = None if message.text == "-" else message.text
    await state.update_data(description=description)

    data = await state.get_data()
    if data['role'] == 'student':
        await message.answer(
            "Укажите ваш курс и направление обучения:"
        )
        await state.set_state(RegistrationStates.entering_course)
    else:
        await message.answer(
            "Сколько проектов вы реализовали? Введите число:"
        )
        await state.set_state(RegistrationStates.entering_projects_count)


@router.message(StateFilter(RegistrationStates.entering_course))
async def process_course(message: types.Message, state: FSMContext):
    """Обработка курса (для студентов)"""
    await state.update_data(course_info=message.text)

    await message.answer(
        "Сколько проектов вы реализовали? Введите число:"
    )
    await state.set_state(RegistrationStates.entering_projects_count)


@router.message(StateFilter(RegistrationStates.entering_projects_count))
async def process_projects_count(message: types.Message, state: FSMContext):
    """Обработка количества проектов"""
    try:
        count = int(message.text)
        await state.update_data(projects_count=count)

        await message.answer(
            "Теперь выберите технологии, с которыми вы работаете.\n"
            "Можно выбрать несколько:",
            reply_markup=get_tags_keyboard()
        )
        await state.update_data(tags=[])
        await state.set_state(RegistrationStates.choosing_tags)
    except ValueError:
        await message.answer("Пожалуйста, введите число:")


@router.callback_query(StateFilter(RegistrationStates.choosing_tags))
async def process_tag_choice(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора технологий"""
    if callback.data == "tags_done":
        data = await state.get_data()
        if not data.get('tags'):
            await callback.answer("Выберите хотя бы одну технологию!", show_alert=True)
            return

        await callback.message.edit_text(
            f"Выбрано технологий: {len(data['tags'])}\n\n"
            "Последний шаг! Отправьте фото для профиля или нажмите кнопку ниже чтобы пропустить:",
            reply_markup=get_skip_photo_keyboard()
        )
        await state.set_state(RegistrationStates.entering_photo)
    elif callback.data.startswith("tag_"):
        tag = callback.data[4:]
        data = await state.get_data()
        tags = data.get('tags', [])

        if tag in tags:
            tags.remove(tag)
        else:
            tags.append(tag)

        await state.update_data(tags=tags)
        await callback.message.edit_reply_markup(reply_markup=get_tags_keyboard(tags))


@router.message(StateFilter(RegistrationStates.entering_photo), F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    """Обработка фото"""
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_url=photo_id)
    await complete_registration(message, state)


@router.callback_query(StateFilter(RegistrationStates.entering_photo), F.data == "skip_photo")
async def skip_photo(callback: types.CallbackQuery, state: FSMContext):
    """Пропуск фото"""
    await complete_registration(callback, state)


async def complete_registration(source, state: FSMContext):
    """Завершение регистрации"""
    data = await state.get_data()

    if isinstance(source, types.CallbackQuery):
        tg_id = source.from_user.id
        message = source.message
    else:
        tg_id = source.from_user.id
        message = source

    async with async_session() as session:
        user = await create_user(
            session,
            str(tg_id),
            data['role'],
            data
        )

        await message.answer(
            "✅ Регистрация завершена!\n\n"
            f"Ваша анкета:\n{format_profile(user)}\n\n"
            "Теперь вы можете начать поиск!",
            reply_markup=get_main_keyboard(True),
            parse_mode="HTML"
        )

    await state.clear()