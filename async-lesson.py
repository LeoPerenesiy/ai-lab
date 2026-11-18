import asyncio


async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(1)
    print("Fetching data success")
    return 41

