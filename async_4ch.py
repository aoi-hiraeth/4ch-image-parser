import asyncio
import aiohttp
import logging
import re
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

pattern = r"/(\d+\.[a-z]+)$"
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


async def get_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()


async def download_file(url, name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            with open(name, "wb") as f:
                f.write(await response.read())
                logging.info(f'Качаем файл: {name} \t {url}')


async def main(url):
    htmldata = await get_data(url)
    soup = BeautifulSoup(htmldata, 'html.parser')

    tasks = []
    for item in soup.find_all(class_="fileThumb"):
        match = re.search(pattern, item['href'])
        if match:
            name = str(match.group(1))
            task = asyncio.create_task(download_file("https:" + item['href'], name))
            tasks.append(task)

    await asyncio.gather(*tasks)
    logging.info("DONE")


if __name__ == "__main__":
    url = input("URL: ")
    asyncio.run(main(url))