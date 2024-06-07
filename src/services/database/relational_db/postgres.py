from sqlalchemy import Column, BigInteger, String, select, insert

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .base import Database, MessageInfo
from app_config import AppConfig

Base = declarative_base()


class Messages(Base):
    __tablename__ = "messages"

    message_id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger)
    user = Column(String)
    text = Column(String)
    file_path = Column(String)


class Postgres(Database):
    def __init__(self, app_config: AppConfig):
        self.engine = create_async_engine(app_config.postgres.build_dsn())
        self.Session = async_sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_message(self, message: MessageInfo) -> None:
        async with self.Session() as session:
            session.add(
                Messages(
                    message_id=message.message_id,
                    chat_id=message.chat_id,
                    user=message.user,
                    text=message.text,
                    file_path=message.file_path
                )
            )
            await session.commit()

    async def get_message(self, message_id: int) -> MessageInfo | None:
        if not isinstance(message_id, int):
            raise ValueError("message_id must be an integer")

        async with self.Session() as session:
            message = await session.get(Messages, message_id)
            if not message:
                return None

            return MessageInfo(
                message_id=message.message_id,
                chat_id=message.chat_id,
                user=message.user,
                text=message.text,
                file_path=message.file_path
            )
