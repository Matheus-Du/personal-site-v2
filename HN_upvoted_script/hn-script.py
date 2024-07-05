import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

with requests.Session() as session:
    page = 1
    while True:
        resp = session.get(
            f"https://news.ycombinator.com/upvoted?id={os.getenv('HNUSER')}&p={page}",
            cookies={"user": f"{os.getenv('HNCOOKIE')}"},
        )
        tree = BeautifulSoup(resp.text, features="html.parser")
        links = [x["href"] for x in tree.select(".subtext .age a")]
        posts = [x["href"] for x in tree.select(".title .titleline > a")]
        if len(links) == 0: break
        for i in range(len(posts)):
            print(i, "https://news.ycombinator.com/" + links[i], posts[i])
        page += 1