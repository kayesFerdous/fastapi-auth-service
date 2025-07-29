from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from config import settings


# Original URL from settings
db_url_str = settings.DATABASE_URL

# Parse the URL
url_obj = make_url(db_url_str)

# Set the driver to asyncpg
url_obj = url_obj.set(drivername="postgresql+asyncpg")

# Handle SSL configuration
connect_args = {}
if url_obj.query.get("sslmode") == "require":
    connect_args["ssl"] = True
    # Remove sslmode from query to prevent it being passed to the driver
    query = dict(url_obj.query)
    del query["sslmode"]
    # Also remove channel_binding if it exists
    if "channel_binding" in query:
        del query["channel_binding"]
    url_obj = url_obj.set(query=query)


# Create the async engine
engine = create_async_engine(url_obj, connect_args=connect_args) #echo=True for debugging

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        yield db
