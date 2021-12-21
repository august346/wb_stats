import asyncio
from copy import copy
from typing import Iterable

from db.dal import SaleReportDAL
from parse.api import SaleReportGetter, get_storage
from utils.transformer import Transformer


class Collector:
    def __init__(self, sri: SaleReportGetter, sr_dal: SaleReportDAL):
        self.sri = sri
        self.sr_dal = sr_dal

        self.queue = asyncio.Queue()

    def transform(self, row: dict) -> dict:
        return Transformer.transform(row, self.sri.key)

    async def producer(self):
        max_row_id = await self.sr_dal.get_max_row_id(self.sri.key)

        async for rows_batch in self.sri.get_sale_reports(max_row_id, pause_between=0.3):
            await self.queue.put(rows_batch)

    async def consumer(self):
        while True:
            rows_batch = await self.queue.get()

            if rows_batch is None:
                self.queue.task_done()
                continue

            await self.sr_dal.add_many(list(map(self.transform, rows_batch)))

            self.queue.task_done()

    async def run(self):
        consumers = [asyncio.ensure_future(self.consumer()) for _ in range(2)]

        await asyncio.gather(*[self.producer()], return_exceptions=True)
        await self.queue.join()  # wait until the consumer has processed all items

        for cons in consumers:
            cons.cancel()


async def add_stock_balances(api_key: str, sale_report_rows: Iterable[dict]):
    stock_balances = await get_storage(api_key)

    for r in sale_report_rows:
        new_r = copy(r)
        wb_id = new_r["wb_id"]
        new_r["stock_balance"] = stock_balances.get(str(wb_id), {}).get("quantityNotInOrders")

        yield new_r
