import os
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

schema_path = Path(__file__).parent / "schema.sql"
load_dotenv()

pool: asyncpg.Pool | None = None


async def init_db() -> None:
    global pool
    pool = await asyncpg.create_pool(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
    )
    sql_script = schema_path.read_text(encoding="utf-8")
    await pool.execute(sql_script)


async def close_db() -> None:
    if pool:
        await pool.close()
