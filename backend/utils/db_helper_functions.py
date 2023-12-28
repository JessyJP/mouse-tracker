import asyncio
import logging
from backend.constants import RETRY_ATTEMPTS, RETRY_BACKOFF
from backend.sql.db_queries import bulk_insert_query, insert_query, manage_db_transaction
from asyncmy.connection import Connection


async def db_send_batch_data(uuid: str, batch_data: list[str]):
    sql = "INSERT INTO coordinates (user_id, x_coordinate, y_coordinate) VALUES (%s, %s, %s)"
    values = [(uuid, int(x), int(y)) for data in batch_data for x, y in [data.decode('utf-8').split(" ")]]
    await bulk_insert_query(sql, values)


async def retry_insert(batch_data, uuid, batch_number):
    for attempt in range(RETRY_ATTEMPTS):
        try:
            return await db_send_batch_data(uuid, batch_data)
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed for batch {batch_number} for {uuid}: {e}")
            if attempt < RETRY_ATTEMPTS - 1:
                await asyncio.sleep(RETRY_BACKOFF)
            raise Exception(f"All retry attempts failed for batch {batch_number} for {uuid}")


@manage_db_transaction
async def db_add_user(conn: Connection, uuid: str):
    sql = "INSERT INTO users (user_id) VALUES (%s)"
    await insert_query(conn, sql, (uuid,))


@manage_db_transaction
async def db_add_picture_path(conn: Connection, user_id: str, filepath: str):
    sql = "INSERT INTO images (user_id, image_path) VALUES (%s,%s)"
    await insert_query(conn, sql, (user_id, filepath))
