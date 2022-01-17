from bs4 import BeautifulSoup
import requests
import csv
import json
import re
from pprint import pprint
import logging
from tqdm import tqdm

logging.getLogger().setLevel(logging.INFO)


def get_poets_info(link: str) -> dict:
    source = requests.get(link).text
    soup = BeautifulSoup(source, "lxml")
    poets_info = {}
    logging.info(f"working on link {link}")

    for poet_info in soup.find_all(
        "div", class_=re.compile("col-6 col-md-8 px-0 text-center.*")
    ):
        poet_link = f'www.aldiwan.net/{poet_info.a["href"]}'
        poet_name = poet_info.span.text
        poets_info[poet_name] = poet_link

        # print(i, poet_name, poet_link)
    # old logic
    # for poet_info in soup.find_all("a", href=re.compile("cat-poet.*")):
    #     if poet_info.span:
    #         poet_link = f'www.aldiwan.net/{poet_info["href"]}'
    #         poet_name = poet_info.span.text
    #         poets_info[poet_name] = poet_link
    return poets_info


def save_poets(poets_info: dict) -> None:

    with open("poets_info.json", "w") as outfile:
        json.dump(poets_info, outfile)


if __name__ == "__main__":
    # the links of the male and female autions pages
    authors_males = "https://www.aldiwan.net/authers-1"
    authors_females = "https://www.aldiwan.net/authers-2"

    # getting all the pages to be scraped and put it into one list
    links = [f"{authors_males}?page={idx}" for idx in range(1, 28)]
    links.extend([f"{authors_females}?page={idx}" for idx in range(1, 3)])
    all_poets = {}
    for link in tqdm(links):
        poets_info = get_poets_info(link)
        logging.info(f"got {len(poets_info)}")
        all_poets.update(poets_info)

    save_poets(all_poets)
    # pprint(links)
