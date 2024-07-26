import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from pymongo import MongoClient

def get_upvoted():
	with requests.Session() as session:
			posts = []
			page = 1
			while True:
				resp = session.get(
					f"https://news.ycombinator.com/upvoted?id={os.getenv('HNUSER')}&p={page}",
					cookies={"user": f"{os.getenv('HNCOOKIE')}"},
				)
				tree = BeautifulSoup(resp.text, features="html.parser")
				hn_ids = [x["href"].split('=')[1] for x in tree.select(".subtext .age a")]
				titles = [x.getText() for x in tree.select(".titleline > a")]
				ages = [x.getText() for x in tree.select(".age a")]
				post_links = [x["href"] for x in tree.select(".title .titleline > a")]
				if len(post_links) == 0: break
				for i in range(len(post_links)):
					posts.append([hn_ids[i], titles[i], ages[i], post_links[i]])
				page += 1
			return posts


def update_coll(collection, upvoted_posts):
	collection.insert_many(
		[{	'id': post_id,
			'title': title,
			'link': link,
			'discussion_link': "https://news.ycombinator.com/item?id=" + post_id,
			'date_posted': date}
		for [post_id, title, date, link] in upvoted_posts]
	)


def main():
	load_dotenv()
	upvoted = get_upvoted()
	conn = MongoClient("mongodb://root:example@localhost:27117/")
	db = conn.personal_site
	db.drop_collection("upvoted_posts")
	db.create_collection("upvoted_posts")
	update_coll(db.upvoted_posts, upvoted)


if __name__ == '__main__':
	main()
