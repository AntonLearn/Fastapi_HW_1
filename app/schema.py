from pydantic import BaseModel
import datetime
from typing import Annotated, List
from annotated_types import Len


class UserIdName(BaseModel):
    id: int
    name: str


class UserDict(UserIdName):
    registration_time: datetime.datetime


class CreateUserResponse(BaseModel):
    result: UserDict


class UserName(BaseModel):
    name: str


class CreateUserRequest(UserName):
    password: Annotated[str, Len(min_length=8)]


class AdvertisementIdHeader(BaseModel):
    id: int
    header: str


class AdvertisementDict(AdvertisementIdHeader):
    owner_id: int
    registration_time: datetime.datetime
    description: str


class CreateAdvertisementResponse(BaseModel):
    result: AdvertisementDict


class AdvertisementName(BaseModel):
    header: str


class CreateAdvertisementRequest(AdvertisementName):
    owner_id: int
    description: str


class DeletedUser(BaseModel):
    deleted: UserDict


class DeletedAdvertisement(BaseModel):
    deleted: AdvertisementDict


class DeleteUserResponse(BaseModel):
    result: DeletedUser


class DeleteAdvertisementResponse(BaseModel):
    result: DeletedAdvertisement


class GetUserResponse(BaseModel):
    result: UserDict


class GetAdvertisementResponse(BaseModel):
    result: AdvertisementDict


class SearchUserPageResponse(BaseModel):
    items: List[UserDict]
    total: int
    page: int
    size: int
    pages: int


class SearchUserPageListResponse(BaseModel):
    result: SearchUserPageResponse | List[UserDict]


class SearchAdvertisementPageResponse(BaseModel):
    items: List[AdvertisementDict]
    total: int
    page: int
    size: int
    pages: int


class SearchAdvertisementPageListResponse(BaseModel):
    result: SearchAdvertisementPageResponse | List[AdvertisementDict]


class UpdateUserResponse(BaseModel):
    result: UserDict


class UpdateAdvertisementResponse(BaseModel):
    result: AdvertisementDict


class UpdateUserRequest(BaseModel):
    name: str | None = None
    password: Annotated[str, Len(min_length=8)] | None = None


class UpdateAdvertisementRequest(BaseModel):
    header: str | None = None
    owner_id: int | None = None
    description: str | None = None
