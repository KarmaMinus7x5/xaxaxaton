"""
FSM состояния для бота
"""
from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """Состояния регистрации"""
    choosing_role = State()
    entering_name = State()
    entering_description = State()
    entering_course = State()  # Только для студентов
    entering_projects_count = State()
    choosing_tags = State()
    entering_photo = State()


class BrowsingStates(StatesGroup):
    """Состояния просмотра анкет"""
    viewing_profiles = State()
    filtering_tags = State()