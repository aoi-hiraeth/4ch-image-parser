import requests 
from user_agent import generate_user_agent
from bs4 import BeautifulSoup 
import re
import logging


pattern = r"/(\d+\.[a-z]+)$"
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    
def getdata(url): 
    r = requests.get(url, timeout=5, headers=headers) 
    return r.text 

htmldata = getdata(input("URL: ")) 
soup = BeautifulSoup(htmldata, 'html.parser') 

for item in soup.find_all(class_="fileThumb"):
    match = re.search(pattern, item['href'])
    name = str(match.group(1))
    with open(name, "wb") as f:
        logging.info(f'Качаем файл: {name} \t {item["href"]}')
        r = requests.get("https:" + item['href'], timeout=5, headers=headers)
        f.write(r.content)

logging.info("DONE")