from functools import wraps
from asyncmy.connection import Connection

from backend.sql.connection import Database, init_db


def manage_db_transaction(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if Database.pool is None:
            await init_db()
        async with Database.pool.acquire() as conn:
            try:
                result = await func(conn, *args, **kwargs)
                await conn.commit()
                return result
            except Exception as e:
                await conn.rollback()
                raise e

    return wrapper


async def insert_query(conn: Connection, sql: str, sql_params=()) -> int:
    async with conn.cursor() as cursor:
        await cursor.execute(sql, sql_params)
        return cursor.lastrowid


@manage_db_transaction
async def bulk_insert_query(conn: Connection, sql: str, sql_params: list[tuple]) -> None:
    async with conn.cursor() as cursor:
        await cursor.executemany(sql, sql_params)
