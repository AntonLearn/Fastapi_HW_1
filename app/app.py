import datetime
from fastapi import FastAPI, HTTPException
from lifespan import lifespan
from schema import (CreateUserResponse, CreateUserRequest,
                    CreateAdvertisementResponse, CreateAdvertisementRequest,
                    DeleteUserResponse, DeleteAdvertisementResponse,
                    GetUserResponse, GetAdvertisementResponse,
                    SearchUserPageListResponse, SearchAdvertisementPageListResponse,
                    UpdateUserResponse, UpdateUserRequest,
                    UpdateAdvertisementResponse, UpdateAdvertisementRequest)
from crud import (add_user_to_db, add_advertisement_to_db,
                  delete_user_by_id, delete_advertisement_by_id,
                  get_user_by_id, get_advertisement_by_id,
                  get_user_filter, get_advertisement_filter)
from models import User, Advertisement
from dependencies import SessionDependency
from fastapi_pagination import paginate, add_pagination, Params
from utils import validate_and_set_paginate_params, get_hashed_password, verify_password


app = FastAPI(
    title="Advertisement Application",
    version='0.0.1',
    description='This project is about creating a buy/sell advertisements service on FastAPI',
    lifespan=lifespan
)
add_pagination(app)


@app.post(path="/v1/user/", response_model=CreateUserResponse)
async def add_user(user_json: CreateUserRequest, session: SessionDependency):
    user_obj = User(**user_json.model_dump())
    user_obj.password = get_hashed_password(user_obj.password)
    user_obj = await add_user_to_db(session, user_obj)
    return {'result': user_obj.json}


@app.post(path="/v1/advertisement/", response_model=CreateAdvertisementResponse)
async def add_advertisement(advertisement_json: CreateAdvertisementRequest,
                          session: SessionDependency):
    advertisement_obj = Advertisement(**advertisement_json.model_dump())
    advertisement_obj = await add_advertisement_to_db(session, advertisement_obj)
    return {'result': advertisement_obj.json}


@app.delete(path="/v1/user/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency):
    user_obj = await delete_user_by_id(session, user_id)
    return {'result': {'deleted': user_obj.json}}


@app.delete(path="/v1/advertisement/{advertisement_id}", response_model=DeleteAdvertisementResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement_obj = await delete_advertisement_by_id(session, advertisement_id)
    return {'result': {'deleted': advertisement_obj.json}}


@app.get(path="/v1/user/{user_id}", response_model=GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user_obj = await get_user_by_id(session, user_id)
    return {'result': user_obj.json}


@app.get(path="/v1/advertisement/{advertisement_id}", response_model=GetAdvertisementResponse)
async def get_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement_obj = await get_advertisement_by_id(session, advertisement_id)
    return {'result': advertisement_obj.json}


@app.get(path='/v1/user/', response_model=SearchUserPageListResponse)
async def search_user(session: SessionDependency, page: int | None = None, size: int | None =  None,
                      user_id: int | None = None, name: str | None = None,
                      registration_time: datetime.datetime | None = None):
    search_result_list = await get_user_filter(session, user_id, name, registration_time)
    if not search_result_list:
        raise HTTPException(status_code=404, detail=f'Users not found!')
    len_search_result_list = len(search_result_list)
    if page is None and size is None:
        return {"result": search_result_list}
    else:
        page, size = validate_and_set_paginate_params(len_search_result_list, page, size)
        return {'result': paginate(search_result_list, params=Params(page=page, size=size))}


@app.get(path='/v1/advertisement/', response_model=SearchAdvertisementPageListResponse)
async def search_advertisement(session: SessionDependency, page: int | None = None,
                               size: int | None =  None, advertisement_id: int | None = None,
                               header: str | None = None, owner_id: int | None = None,
                               registration_time: datetime.datetime | None = None,
                               description: str | None = None):
    search_result_list = await get_advertisement_filter(session, advertisement_id, header,
                                                        owner_id, registration_time, description)
    if not search_result_list:
        raise HTTPException(status_code=404, detail=f'Advertisements not found!')
    len_search_result_list = len(search_result_list)
    if page is None and size is None:
        return {"result": search_result_list}
    else:
        page, size = validate_and_set_paginate_params(len_search_result_list, page, size)
        return {'result': paginate(search_result_list, params=Params(page=page, size=size))}


@app.patch(path="/v1/user/{user_id}", response_model=UpdateUserResponse)
async def update_user(user_id: int, user_json: UpdateUserRequest, session: SessionDependency):
    user_json_dict = user_json.model_dump(exclude_unset=True)
    if not user_json_dict:
        raise HTTPException(status_code=400, detail=f'Bad request, not modified, request does not match model User!')
    user_obj = await get_user_by_id(session, user_id)
    for field, value in user_json_dict.items():
        setattr(user_obj, field, value)
    if user_json_dict.get('password'):
        user_obj.password = get_hashed_password(user_obj.password)
    user_obj = await add_user_to_db(session, user_obj)
    return {'result': user_obj.json}


@app.patch(path="/v1/advertisement/{advertisement_id}", response_model=UpdateAdvertisementResponse)
async def update_adv(advertisement_id: int, advertisement_json: UpdateAdvertisementRequest, session: SessionDependency):
    advertisement_json_dict = advertisement_json.model_dump(exclude_unset=True)
    if not advertisement_json_dict:
        raise HTTPException(status_code=400, detail=f'Bad request, not modified, request does not match model Advertisement!')
    advertisement_obj = await get_advertisement_by_id(session, advertisement_id)
    for field, value in advertisement_json_dict.items():
        setattr(advertisement_obj, field, value)
    advertisement_obj = await add_advertisement_to_db(session, advertisement_obj)
    return {'result': advertisement_obj.json}
