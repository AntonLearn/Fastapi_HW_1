import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import ORM_OBJECT, User, Advertisement
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


async def add_user_to_db(session: AsyncSession, user_obj: ORM_OBJECT) -> ORM_OBJECT:
    session.add(user_obj)
    try:
        await session.commit()
    except IntegrityError as err:
        if err.orig.pgcode == "23505":
            raise HTTPException(status_code=409, detail=f'User [{user_obj.name}] already exists!')
        raise err
    return user_obj


async def add_advertisement_to_db(session: AsyncSession, advertisement_obj: ORM_OBJECT) -> ORM_OBJECT:
    session.add(advertisement_obj)
    try:
        await session.commit()
    except IntegrityError as err:
        if err.orig.pgcode == "23503":
            raise HTTPException(status_code=404,
                                detail=f"Advertisement [{advertisement_obj.header}]: Owner [id: "
                                       f"{advertisement_obj.owner_id}] not found in user's table!")
        if err.orig.pgcode == "23505":
            raise HTTPException(status_code=409, detail=f'Advertisement [{advertisement_obj.header}] already exists!')
        raise err
    return advertisement_obj


async def get_user_by_id(session: AsyncSession, user_id: int) -> ORM_OBJECT:
    user_obj = await session.get(User, user_id)
    if user_obj is None:
        raise HTTPException(status_code=404, detail=f'User id: {user_id} not found!')
    return user_obj


async def get_advertisement_by_id(session: AsyncSession, advertisement_id: int) -> ORM_OBJECT:
    advertisement_obj = await session.get(Advertisement, advertisement_id)
    if advertisement_obj is None:
        raise HTTPException(status_code=404, detail=f'Advertisement [id: {advertisement_id}] not found!')
    return advertisement_obj


async def delete_user_by_id(session: AsyncSession, user_id: int) -> ORM_OBJECT:
    user_obj = await get_user_by_id(session, user_id)
    await session.delete(user_obj)
    try:
        await session.commit()
    except IntegrityError as err:
        if err.orig.pgcode == "23503":
            raise HTTPException(status_code=404,
                                detail=f"User [id: {user_id}] cannot be deleted because he is "
                                       f"the owner of advertisement(s)!")
        raise err
    return user_obj


async def delete_advertisement_by_id(session: AsyncSession, advertisement_id: int) -> ORM_OBJECT:
    advertisement_obj = await get_advertisement_by_id(session, advertisement_id)
    await session.delete(advertisement_obj)
    await session.commit()
    return advertisement_obj


async def get_user_filter(session: AsyncSession, user_id: int | None = None, name: str |None = None,
                          time: datetime.datetime | None = None) -> list[ORM_OBJECT]:
    if user_id is not None and name is None and time is None:
        obj_select = select(User).where(User.id == user_id)
    if user_id is not None and name is None and time is not None:
        obj_select = select(User).where((User.id == user_id) & (User.registration_time == time))
    if user_id is not None and name is not None and time is None:
        obj_select = select(User).where((User.id == user_id) & (User.name == name))
    if user_id is not None and name is not None and time is not None:
        obj_select = select(User).filter((User.id == user_id) & (User.name == name)
                                         & (User.registration_time == time))
    if user_id is None and name is None and time is None:
        obj_select = select(User)
    if user_id is None and name is None and time is not None:
        obj_select = select(User).where(User.registration_time == time)
    if user_id is None and name is not None and time is None:
        obj_select = select(User).where(User.name == name)
    if user_id is None and name is not None and time is not None:
        obj_select = select(User).where((User.name == name) & (User.registration_time == time))
    return [user_obj.json for user_obj in (await session.execute(obj_select)).scalars().all()]


async def get_advertisement_filter(session: AsyncSession, advertisement_id: int | None = None,
                                   header: str | None = None, owner_id: int | None = None,
                                   time: datetime.datetime | None = None,
                                   description: str | None = None) -> list[ORM_OBJECT]:
    if (advertisement_id is not None and header is None and owner_id is None
        and time is None and description is None):
        obj_select = select(Advertisement).where(Advertisement.id == advertisement_id)
    if (advertisement_id is not None and header is None and owner_id is None
        and time is None and description is not None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.description == description))
    if (advertisement_id is not None and header is None and owner_id is None
        and time is not None and description is None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.registration_time == time))
    if (advertisement_id is not None and header is None and owner_id is None
        and time is not None and description is not None):
        obj_select = select(Advertisement).filter((Advertisement.id == advertisement_id) &
                                                  (Advertisement.registration_time == time) &
                                                  (Advertisement.description == description))
    if (advertisement_id is None and header is None and owner_id is None and time is None
        and description is None):
        obj_select = select(Advertisement)
    if (advertisement_id is None and header is None and owner_id is None and time is None
        and description is not None):
        obj_select = select(Advertisement).where(Advertisement.description == description)
    if (advertisement_id is None and header is None and owner_id is None and time is not None
        and description is None):
        obj_select = select(Advertisement).where(Advertisement.registration_time == time)
    if (advertisement_id is None and header is None and owner_id is None and time is not None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.registration_time == time) &
                                                 (Advertisement.description == description))
    if (advertisement_id is None and header is None and owner_id is not None and time is None
        and description is None):
        obj_select = select(Advertisement).where(Advertisement.owner_id == owner_id)
    if (advertisement_id is None and header is None and owner_id is not None and time is None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.owner_id == owner_id) &
                                                 (Advertisement.description == description))
    if (advertisement_id is None and header is None and owner_id is not None and time is not None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.owner_id == owner_id) &
                                                 (Advertisement.registration_time == time))
    if (advertisement_id is None and header is None and owner_id is not None and time is not None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.owner_id == owner_id) &
                                                 (Advertisement.registration_time == time) &
                                                 (Advertisement.description == description))
    if (advertisement_id is None and header is not None and owner_id is None and time is None
        and description is None):
        obj_select = select(Advertisement).where(Advertisement.header == header)
    if (advertisement_id is None and header is not None and owner_id is None and time is None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.header == header) &
                                                 (Advertisement.description == description))
    if (advertisement_id is None and header is not None and owner_id is None and time is not None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.header == header) &
                                                 (Advertisement.registration_time == time))
    if (advertisement_id is None and header is not None and owner_id is None and time is not None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.header == header) &
                                                 (Advertisement.registration_time == time) &
                                                 (Advertisement.description == description))
    if (advertisement_id is None and header is not None and owner_id is not None and time is None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.header == header) &
                                                 (Advertisement.owner_id == owner_id))
    if (advertisement_id is None and header is not None and owner_id is not None and time is None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.header == header) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.description == description))
    if (advertisement_id is None and header is not None and owner_id is not None and time is not None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.header == header) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.registration_time == time))
    if (advertisement_id is None and header is not None and owner_id is not None and time is not None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.header == header) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.registration_time == time) &
                                                 (Advertisement.description == description))
    if (advertisement_id is not None and header is None and owner_id is not None and time is None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.owner_id == owner_id))
    if (advertisement_id is not None and header is None and owner_id is not None and time is None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.description == description))
    if (advertisement_id is not None and header is None and owner_id is not None and time is not None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.registration_time == time))
    if (advertisement_id is not None and header is None and owner_id is not None and time is not None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.registration_time == time) &
                                                 (Advertisement.description == description))
    if (advertisement_id is not None and header is not None and owner_id is None and time is None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.header == header))
    if (advertisement_id is not None and header is not None and owner_id is None and time is None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.header == header) &
                                                 (Advertisement.description == description))
    if (advertisement_id is not None and header is not None and owner_id is None and time is not None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.header == header) &
                                                 (Advertisement.registration_time == time))
    if (advertisement_id is not None and header is not None and owner_id is None and time is not None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.header == header) &
                                                 (Advertisement.registration_time == time) &
                                                 (Advertisement.description == description))
    if (advertisement_id is not None and header is not None and owner_id is not None and time is None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.header == header) &
                                                 (Advertisement.owner_id == owner_id))
    if (advertisement_id is not None and header is not None and owner_id is not None and time is None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.header == header) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.description == description))
    if (advertisement_id is not None and header is not None and owner_id is not None and time is not None
        and description is None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.header == header) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.registration_time == time))
    if (advertisement_id is not None and header is not None and owner_id is not None and time is not None
        and description is not None):
        obj_select = select(Advertisement).where((Advertisement.id == advertisement_id) &
                                                 (Advertisement.header == header) &
                                                 (Advertisement.owner_id == owner_id) &
                                                 (Advertisement.registration_time == time) &
                                                 (Advertisement.description == description))
    return [user_obj.json for user_obj in (await session.execute(obj_select)).scalars().all()]
