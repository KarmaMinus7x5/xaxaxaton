"""
Тестовые данные для бота
"""
import logging
from sqlalchemy import select
from database.database import async_session
from database.models import User, Tag
from database.crud import create_user
from config.settings import TECH_TAGS

logger = logging.getLogger(__name__)

# Тестовые менторы
TEST_MENTORS = [
    {
        "telegram_id": -1001,
        "full_name": "Александр Петров",
        "role": "mentor",
        "description": "Senior Python Developer с 8-летним опытом. Специализируюсь на веб-разработке и машинном обучении.",
        "projects_count": 45,
        "tags": ["Python", "Django", "FastAPI", "PostgreSQL", "Docker", "ML"],
        "is_test_user": True
    },
    {
        "telegram_id": -1002,
        "full_name": "Мария Иванова",
        "role": "mentor",
        "description": "Frontend Team Lead. Помогу освоить современный JavaScript и React.",
        "projects_count": 32,
        "tags": ["JavaScript", "React", "TypeScript", "Node.js", "Vue.js"],
        "is_test_user": True
    },
    {
        "telegram_id": -1003,
        "full_name": "Дмитрий Сидоров",
        "role": "mentor",
        "description": "DevOps инженер. Научу работать с облачными технологиями и CI/CD.",
        "projects_count": 28,
        "tags": ["Docker", "Kubernetes", "AWS", "DevOps", "Python", "Go"],
        "is_test_user": True
    },
    {
        "telegram_id": -1004,
        "full_name": "Елена Козлова",
        "role": "mentor",
        "description": "Mobile Developer. Разрабатываю приложения для iOS и Android.",
        "projects_count": 23,
        "tags": ["Swift", "iOS", "Android", "Kotlin", "Flutter", "React Native"],
        "is_test_user": True
    },
    {
        "telegram_id": -1005,
        "full_name": "Андрей Волков",
        "role": "mentor",
        "description": "Backend архитектор. Проектирую высоконагруженные системы.",
        "projects_count": 51,
        "tags": ["Java", "Spring", "PostgreSQL", "MongoDB", "Kubernetes", "AWS"],
        "is_test_user": True
    }
]

# Тестовые студенты
TEST_STUDENTS = [
    {
        "telegram_id": -2001,
        "full_name": "Иван Смирнов",
        "role": "student",
        "description": "Изучаю веб-разработку, интересуюсь бэкендом.",
        "course_info": "3 курс, Прикладная информатика",
        "projects_count": 3,
        "tags": ["Python", "Django", "PostgreSQL"],
        "is_test_user": True
    },
    {
        "telegram_id": -2002,
        "full_name": "Анна Федорова",
        "role": "student",
        "description": "Начинающий frontend разработчик.",
        "course_info": "2 курс, Программная инженерия",
        "projects_count": 2,
        "tags": ["JavaScript", "React", "TypeScript"],
        "is_test_user": True
    },
    {
        "telegram_id": -2003,
        "full_name": "Максим Новиков",
        "role": "student",
        "description": "Интересуюсь мобильной разработкой и UI/UX.",
        "course_info": "4 курс, Информационные системы",
        "projects_count": 5,
        "tags": ["Flutter", "React Native", "JavaScript"],
        "is_test_user": True
    },
    {
        "telegram_id": -2004,
        "full_name": "Ольга Морозова",
        "role": "student",
        "description": "Изучаю Data Science и машинное обучение.",
        "course_info": "Магистратура 1 курс, Искусственный интеллект",
        "projects_count": 4,
        "tags": ["Python", "ML", "Data Science", "AI"],
        "is_test_user": True
    },
    {
        "telegram_id": -2005,
        "full_name": "Павел Егоров",
        "role": "student",
        "description": "Хочу стать DevOps инженером.",
        "course_info": "3 курс, Компьютерные науки",
        "projects_count": 2,
        "tags": ["Docker", "Kubernetes", "DevOps", "Python"],
        "is_test_user": True
    }
]


async def init_test_data():
    """Создает тестовых пользователей и теги при первом запуске"""
    async with async_session() as session:
        # Создаем теги
        for tag_name in TECH_TAGS:
            result = await session.execute(select(Tag).filter_by(name=tag_name))
            if not result.scalar_one_or_none():
                session.add(Tag(name=tag_name))
        await session.commit()

        # Проверяем, есть ли уже тестовые пользователи
        result = await session.execute(
            select(User).filter_by(is_test_user=True).limit(1)
        )
        if result.scalar_one_or_none():
            logger.info("Тестовые пользователи уже созданы")
            return

        logger.info("Создаем тестовых пользователей...")