from passlib.context import CryptContext
from models import Base, engine
from math import ceil



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def validate_and_set_paginate_params(len_search: int, page: int | None = None,
                                     size: int | None = None) -> tuple[int, int]:
    if size is None or size not in range(1, len_search+1):
        return 1, len_search
    pages = ceil(len_search/size)
    if page is None or page not in range(1, pages+1):
        return 1, size
    return page, size
