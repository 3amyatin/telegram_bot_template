import os
from dotenv import load_dotenv
from typing import List
import datetime

from sqlalchemy import ForeignKey, String, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL found in environment variables")

engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)

    tg_id = mapped_column(BigInteger)
    name = mapped_column(String)

    results: Mapped[List['Result']] = relationship(back_populates='user')  # Result.user

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, tg_id={self.tg_id!r})"

class Test(Base):
    __tablename__ = 'tests'
    id: Mapped[int] = mapped_column(primary_key=True)

    name = mapped_column(String)
    description = mapped_column(String)

    questions: Mapped[List['Question']] = relationship(back_populates='test')  # Question.test


class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(primary_key=True)

    test_id = mapped_column(ForeignKey('tests.id'))
    question = mapped_column(String)
    A = mapped_column(String)
    B = mapped_column(String)
    C = mapped_column(String)
    D = mapped_column(String)
    answer = mapped_column(String(1))

    test: Mapped['Test'] = relationship(back_populates='questions')  # Test.questions
    results: Mapped[List['Result']] = relationship(back_populates='question')   # Result.question


class Result(Base):
    __tablename__ = 'results'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id = mapped_column(ForeignKey('users.id'))
    question_id = mapped_column(ForeignKey('questions.id'))
    answer = mapped_column(String(1))
    timestamp: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    user: Mapped['User'] = relationship(back_populates='results')  # User.results
    question: Mapped['Question'] = relationship(back_populates='results')  # Question.results



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)