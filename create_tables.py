import asyncio
from models import Base, engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())


# Run this script to create the tables:

# python create_tables.py
