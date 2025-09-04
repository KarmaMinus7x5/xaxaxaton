"""
Функции форматирования текста
"""
from database.models import User


def format_profile(user: User) -> str:
    """Форматировать профиль пользователя"""
    role_emoji = "👨‍🏫" if user.role == "mentor" else "👨‍🎓"
    role_text = "Ментор" if user.role == "mentor" else "Студент"

    text = f"{role_emoji} <b>{role_text}</b>\n\n"
    text += f"<b>Имя:</b> {user.full_name}\n"

    if user.role == "student" and user.course_info:
        text += f"<b>Курс и направление:</b> {user.course_info}\n"

    if user.description:
        text += f"<b>О себе:</b> {user.description}\n"

    text += f"<b>Количество проектов:</b> {user.projects_count}\n"

    if user.tags:
        tags_str = ", ".join([f"#{tag.name}" for tag in user.tags])
        text += f"<b>Технологии:</b> {tags_str}\n"

    if user.is_test_user:
        text += f"\n<i>📌 Это тестовая анкета</i>"

    return text


def format_profile_with_stats(user: User) -> str:
    """Форматировать профиль со статистикой"""
    profile_text = format_profile(user)
    stats_text = (
        f"\n📊 <b>Статистика:</b>\n"
        f"Отправлено лайков: {len(user.sent_likes)}\n"
        f"Получено лайков: {len(user.received_likes)}\n"
        f"Взаимных лайков: {len([l for l in user.received_likes if l.is_mutual])}"
    )
    return profile_text + stats_text


def format_likes_list(user: User) -> str:
    """Форматировать список лайков"""
    received_likes = [like for like in user.received_likes if not like.is_mutual]
    mutual_likes = [like for like in user.received_likes if like.is_mutual]

    text = "❤️ <b>Ваши лайки</b>\n\n"

    if mutual_likes:
        text += "🎉 <b>Взаимные лайки:</b>\n"
        for like in mutual_likes:
            text += f"• {like.from_user.full_name}"
            text += "\n"
        text += "\n"

    if received_likes:
        text += "💕 <b>Вам поставили лайк:</b>\n"
        for like in received_likes:
            text += f"• {like.from_user.full_name}\n"

    if not mutual_likes and not received_likes:
        text += "Пока что лайков нет 😔\n"
        text += "Продолжайте смотреть анкеты!"

    return text