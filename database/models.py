"""
Модели базы данных
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Таблица для связи многие-ко-многим (теги пользователей)
user_tags = Table('user_tags', Base.metadata,
                  Column('user_id', Integer, ForeignKey('users.id')),
                  Column('tag_id', Integer, ForeignKey('tags.id'))
                  )


class UserRole(Enum):
    STUDENT = "student"
    MENTOR = "mentor"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    role = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    projects_count = Column(Integer, default=0)
    course_info = Column(String, nullable=True)  # Только для студентов
    created_at = Column(DateTime, default=datetime.utcnow)
    is_test_user = Column(Boolean, default=False)

    tags = relationship("Tag", secondary=user_tags, back_populates="users", lazy="selectin")
    sent_likes = relationship("Like", foreign_keys="Like.from_user_id", back_populates="from_user", lazy="selectin")
    received_likes = relationship("Like", foreign_keys="Like.to_user_id", back_populates="to_user", lazy="selectin")


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", secondary=user_tags, back_populates="tags")


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_mutual = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_likes")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_likes")