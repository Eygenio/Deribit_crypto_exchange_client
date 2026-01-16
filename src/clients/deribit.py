import aiohttp

URL = "https://www.deribit.com/api/v2/public/get_index_price"


async def fetch_price(ticker: str) -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params={"index_name": ticker}) as response:
            data = await response.json()
            return data["result"]["index_price"]
