from contextlib import asynccontextmanager
from functools import wraps
from os import name
from typing import Callable, TypeVar, ParamSpec, Awaitable

from sqlalchemy import select, update, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import async_session
from app.db.models import User

def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


@with_session
async def get_user(session: AsyncSession, tg_id: int):
    return await session.scalar(select(User).where(User.tg_id == tg_id))

@with_session
async def set_user(session: AsyncSession, tg_id: int, name: str):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    
    if not user:
        session.add(User(tg_id=tg_id, name=name))
        await session.commit()

