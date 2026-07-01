import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq


async def get_data():
    browser = await launch()
    page = await browser.newPage()