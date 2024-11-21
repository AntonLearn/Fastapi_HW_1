from contextlib import asynccontextmanager
from fastapi import FastAPI
from models import engine
from utils import create_tables, delete_tables
from config import DROP_ALL_TABLES


@asynccontextmanager
async def lifespan(app: FastAPI):
    if DROP_ALL_TABLES != 'Off':
        await delete_tables()
        print('DATABASE INITIALIZED')
    await create_tables()
    print('DATABASE READY')
    print('START')
    yield
    await engine.dispose()
    print('FINISH')
