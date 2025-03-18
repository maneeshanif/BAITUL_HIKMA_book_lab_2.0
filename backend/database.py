from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import  AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()

# ✅ Get the database URL
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "")

# ✅ Create an Async Engine using create_async_engine
engine = create_async_engine(DB_CONNECTION_STRING, echo=True, future=True)

# ✅ Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    pool_pre_ping=True, pool_size=5, max_overflow=10
)

# ✅ Async function to create database tables
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Database built successfully")

# ✅ Async dependency to get a session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session




# # from typing import TYPE_CHECKING

# # if TYPE_CHECKING:
# #     from sqlmodel import SQLModel,Session

# # from sqlmodel import create_engine,SQLModel,Session
# # from dotenv import load_dotenv
# # import os
# # load_dotenv()

# # DB_Key = os.getenv("DB_CONNECTION_STRING","")

# # engine = create_engine(DB_Key)

# # def create_db():
# #     SQLModel.metadata.create_all(engine)
# #     print("database build successfully")

# # def get_session():
# #     with Session(engine) as session:
# #         yield session


# from typing import TYPE_CHECKING
# from sqlmodel import SQLModel,create_engine
# from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession ,async_sessionmaker
# from dotenv import load_dotenv
# import os

# if TYPE_CHECKING:
#     from sqlmodel.ext.asyncio.session import AsyncSession

# # Load environment variables
# load_dotenv()

# # Get database connection string
# DB_Key = os.getenv("DB_CONNECTION_STRING", "")

# # ✅ Create an Async Engine
# engine = AsyncEngine(create_engine(DB_Key, echo=True, future=True))

# # ✅ Create async session factory
# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

# # ✅ Async function to create database tables
# async def create_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
#     print("Database built successfully")

# # ✅ Async generator for dependency injection
# async def get_async_session():
#     async with AsyncSessionLocal() as session:
#         yield session
