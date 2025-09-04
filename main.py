"""
Главный файл для запуска бота
"""
import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot import bot
from database.database import init_db
from utils.test_data import init_test_data
from utils.logging_utils import setup_logging, get_logger
from config.settings import LOG_LEVEL
from utils.logging_middleware import LoggingMiddleware

# Импорт роутеров
from handlers import (
    start,
    registration,
    browsing,
    profile,
    likes
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def register_routers(dp: Dispatcher):
    """Регистрация всех роутеров"""
    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(browsing.router)
    dp.include_router(profile.router)
    dp.include_router(likes.router)


async def main():
    setup_logging(LOG_LEVEL)
    logger = get_logger('bot')

    """Главная функция запуска бота"""
    # Инициализация диспетчера
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(LoggingMiddleware())
    # Регистрация роутеров
    register_routers(dp)

    # Инициализация БД
    logger.info("Инициализация базы данных...")
    await init_db()

    # Создание тестовых данных
    logger.info("Создание тестовых данных...")
    await init_test_data()

    # Запуск бота
    logger.info("Бот запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())