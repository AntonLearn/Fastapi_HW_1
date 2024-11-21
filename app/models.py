import datetime
from config import PG_DSN
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncAttrs)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func, ForeignKey


engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time
        }


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    header: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    description: Mapped[str] = mapped_column(String(240), nullable=False)

    @property
    def json(self):
        return {
            "id": self.id,
            "header": self.header,
            "owner_id": self.owner_id,
            "registration_time": self.registration_time,
            "description": self.description
        }


ORM_OBJECT = User | Advertisement
ORM_CLS = type[User | Advertisement]