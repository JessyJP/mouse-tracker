import logging

from backend.utils.db_helper_functions import retry_insert


class BatchManager:
    def __init__(self, cache_conn):
        self.cache_conn = cache_conn
        self._batch_limit = 1000

    async def process_full_batch(self, uuid: str, batch_number):
        batch_key = f"{uuid}:batch:{batch_number}"
        batch_data = await self.cache_conn.get_queue_items(batch_key, 0, -1)
        try:
            await retry_insert(batch_data, uuid, batch_number)
            await self._add_batch(uuid)
        except Exception as e:
            logging.error(f"Failed to process batch {batch_number} for {uuid} after retries: {e}")
            await self._log_unprocessed_batch(uuid, batch_number, batch_data)
            return
        await self._remove_batch(uuid)
        await self.cache_conn.delete(batch_key)

    async def add_to_batch(self, uuid: str, data):
        current_batch_number = await self._find_available_batch(uuid)
        if current_batch_number is None:
            current_batch_number = await self._add_batch(uuid)
        batch_key = f"{uuid}:batch:{current_batch_number}"
        await self.cache_conn.queue_push(batch_key, data)

        batch_length = await self.cache_conn.get_len(batch_key)
        if batch_length is not None and batch_length >= self._batch_limit:
            await self.process_full_batch(uuid, current_batch_number)

    async def _find_available_batch(self, uuid: str) -> int | None:
        last_batch_num = await self.cache_conn.get_queue_items(uuid, -1, -1)
        if last_batch_num:
            return int(last_batch_num[0])
        return None

    async def _remove_batch(self, uuid: str):
        return await self.cache_conn.queue_pop(uuid)

    async def _add_batch(self, uuid: str) -> int:
        latest_batch = await self._find_available_batch(uuid)
        new_batch_num = latest_batch + 1 if latest_batch is not None else 1
        await self.cache_conn.queue_push(uuid, new_batch_num)
        return new_batch_num

    async def handle_disconnect(self, uuid: str):
        """Process any pending data for a disconnected user."""
        current_batch_number = await self._find_available_batch(uuid)
        if current_batch_number is not None:
            await self.process_full_batch(uuid, current_batch_number)
            await self.cache_conn.delete(uuid)

    async def _log_unprocessed_batch(self, uuid: str, batch_number: str, batch_data):
        # todo Implement logic to log or store the unprocessed batch number
        pass
