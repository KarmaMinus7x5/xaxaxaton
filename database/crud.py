"""
CRUD операции с базой данных
"""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging
from database.models import User, Tag, Like

logger = logging.getLogger('crud')
async def get_user(session: AsyncSession, telegram_id: int) -> Optional[User]:
    """Получить пользователя по telegram_id"""
    result = await session.execute(
        select(User)
        .options(selectinload(User.tags))
        .options(selectinload(User.sent_likes))
        .options(selectinload(User.received_likes))
        .filter_by(telegram_id=telegram_id)
    )
    user = result.scalar_one_or_none()
    logger.debug("get_user: telegram_id=%s found=%s", telegram_id, bool(user))
    return user


async def create_user(session: AsyncSession, telegram_id: int, role: str, data: dict) -> User:
    """Создать нового пользователя"""
    user = User(
        telegram_id=telegram_id,
        role=role,
        full_name=data.get('name'),
        description=data.get('description'),
        projects_count=data.get('projects_count', 0),
        course_info=data.get('course_info'),
        photo_url=data.get('photo_url'),
        is_test_user=data.get('is_test_user', False)
    )

    # Добавляем теги
    for tag_name in data.get('tags', []):
        result = await session.execute(select(Tag).filter_by(name=tag_name))
        tag = result.scalar_one_or_none()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
        user.tags.append(tag)

    session.add(user)
    await session.commit()
    logger.info("create_user: created user telegram_id=%s role=%s tags=%s",telegram_id, role, [t.name for t in user.tags])

    # Перезагружаем пользователя с его связями
    await session.refresh(user)
    return user


async def get_next_profile(session: AsyncSession, viewer_id: int, filters: dict = None) -> Optional[User]:
    """Получить следующий профиль для просмотра"""
    viewer = await get_user(session, viewer_id)
    if not viewer:
        return None

    # Получаем роль для поиска (студенты ищут менторов и наоборот)
    target_role = "mentor" if viewer.role == "student" else "student"

    # Базовый запрос с eager loading
    query = select(User).options(
        selectinload(User.tags),
        selectinload(User.sent_likes),
        selectinload(User.received_likes)
    ).filter(
        User.role == target_role,
        User.telegram_id != viewer_id
    )

    # Исключаем уже просмотренные профили
    viewed_ids = [like.to_user_id for like in viewer.sent_likes]
    if viewed_ids:
        query = query.filter(~User.id.in_(viewed_ids))

    # Применяем фильтры по тегам если есть
    if filters and filters.get('tags'):
        query = query.join(User.tags).filter(Tag.name.in_(filters['tags']))

    result = await session.execute(query.limit(1))
    return result.scalar_one_or_none()


async def create_like(session: AsyncSession, from_telegram_id: int, to_user_id: int) -> tuple[bool, Optional[User]]:
    """
    Создать лайк
    Возвращает (is_mutual, liked_user)
    """
    from_user = await get_user(session, from_telegram_id)
    if not from_user:
        return False, None

    # Проверяем, не было ли уже лайка
    result = await session.execute(
        select(Like).filter_by(from_user_id=from_user.id, to_user_id=to_user_id)
    )
    if result.scalar_one_or_none():
        return False, None

    # Получаем пользователя, которому ставим лайк
    liked_user = await session.get(User, to_user_id)
    if not liked_user:
        return False, None

    # Создаем лайк
    like = Like(from_user_id=from_user.id, to_user_id=to_user_id)

    # Проверяем взаимность
    reverse_result = await session.execute(
        select(Like).filter_by(from_user_id=to_user_id, to_user_id=from_user.id)
    )
    reverse_like = reverse_result.scalar_one_or_none()

    if reverse_like:
        like.is_mutual = True
        reverse_like.is_mutual = True

    session.add(like)
    await session.commit()

    return reverse_like is not None, liked_user


async def delete_user_data(session: AsyncSession, telegram_id: int) -> bool:
    """Удалить данные пользователя"""
    user = await get_user(session, telegram_id)
    if not user or user.is_test_user:
        return False

    # Удаляем лайки
    likes_to_delete = await session.execute(
        select(Like).filter(
            (Like.from_user_id == user.id) | (Like.to_user_id == user.id)
        )
    )
    for like in likes_to_delete.scalars():
        await session.delete(like)

    # Удаляем пользователя
    await session.delete(user)
    await session.commit()
    return True


async def create_tag(session: AsyncSession, tag_name: str) -> Tag:
    """Создать или получить существующий тег"""
    result = await session.execute(select(Tag).filter_by(name=tag_name))
    tag = result.scalar_one_or_none()
    if not tag:
        tag = Tag(name=tag_name)
        session.add(tag)
        await session.commit()
    return tag

