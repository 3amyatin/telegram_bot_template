import os
from dotenv import load_dotenv
from typing import Annotated, List
import datetime
import enum

from sqlalchemy import Table, Column, ForeignKey, String, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL found in environment variables")

async_engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]  # or =text("TIMEZONE('UTC', now())") # for UTC
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=func.now(),
        onupdate=datetime.datetime.now(),
    )]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[intpk]

    tg_id = mapped_column(BigInteger)
    name = mapped_column(String)

    results: Mapped[List['Result']] = relationship(back_populates='user')  # Result.user
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, tg_id={self.tg_id!r})"

questions_tests = Table(
    "questions_tests",
    Base.metadata,
    Column("test_id", ForeignKey("tests.id"), primary_key=True),
    Column("question_id", ForeignKey("questions.id"), primary_key=True),
)

class Test(Base):
    __tablename__ = 'tests'
    id: Mapped[intpk]

    name = mapped_column(String)
    description = mapped_column(String)

    questions: Mapped[List['Question']] = relationship(secondary=questions_tests, back_populates='test')  # Question.test

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[intpk]

    test_id = mapped_column(ForeignKey('tests.id'))
    question = mapped_column(String)
    A = mapped_column(String)
    B = mapped_column(String)
    C = mapped_column(String)
    D = mapped_column(String)
    answer = mapped_column(String(1))

    tests: Mapped[List['Test']] = relationship(back_populates='questions')  # Test.questions
    results: Mapped[List['Result']] = relationship(secondary=questions_tests, back_populates='question')   # Result.question

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class Choice_ABCD(enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'

class Result(Base):
    __tablename__ = 'results'
    id: Mapped[intpk]

    user_id = mapped_column(ForeignKey('users.id'))
    question_id = mapped_column(ForeignKey('questions.id'))
    answer: Mapped[Choice_ABCD]

    user: Mapped['User'] = relationship(back_populates='results')  # User.results
    question: Mapped['Question'] = relationship(back_populates='results')  # Question.results

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]



async def async_main():
    async with async_engine.begin() as conn:  # .begin() does commit automatic, .connect() requires explicit commit
        await conn.run_sync(Base.metadata.create_all)