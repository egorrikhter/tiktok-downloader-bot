import os

from dotenv import load_dotenv

load_dotenv()
import asyncpg

pool: asyncpg.Pool | None = None

def read_schema_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )
    sql_script = read_schema_file("schema.sql")
    async with pool.acquire() as conn:
        await conn.execute(sql_script)

async def close_db():
    if pool:
        await pool.close()
