from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from config import settings


# Original URL from settings
DATABASE_URL = settings.DATABASE_URL

# Create the async engine
engine = create_async_engine(DATABASE_URL) #echo=True for debugging

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        yield db
