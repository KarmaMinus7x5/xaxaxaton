"""
Конфигурация проекта
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# База данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///mentors.db")
if DATABASE_URL.startswith("sqlite+aiosqlite:///") and DATABASE_URL.count(":///") == 1:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_sqlite = os.path.join(base_dir, "mentors.db")
    if os.getenv("DATABASE_URL") is None:
        DATABASE_URL = f"sqlite+aiosqlite:///{default_sqlite}"

# Список доступных технологий
TECH_TAGS = [
    "Python", "JavaScript", "React", "Node.js", "Django", "FastAPI",
    "TypeScript", "Vue.js", "Angular", "Java", "Spring", "C#",
    ".NET", "Go", "Rust", "Swift", "iOS", "Android", "Kotlin",
    "Flutter", "React Native", "Docker", "Kubernetes", "AWS",
    "DevOps", "ML", "AI", "Data Science", "PostgreSQL", "MongoDB"
]