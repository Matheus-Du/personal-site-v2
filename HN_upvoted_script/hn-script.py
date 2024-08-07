import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from pymongo import MongoClient, timeout as pymongo_timeout
from pymongo.errors import PyMongoError, ConnectionFailure, OperationFailure

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
	# get upvoted posts; if this doesn't work, throw an exception and exit without updating DB
	try:
		upvoted = get_upvoted()
		if len(upvoted) == 0: raise Exception
	except Exception as exc:
		print(f"Error: Couldn't retrieve updated posts\n{exc}")
		return
	
	conn = MongoClient(f"mongodb://{os.getenv('MONGOUN')}:{os.getenv('MONGOPW')}@localhost:27117/?timeoutMS=10000")
	try:
		db = conn.personal_site
	except Exception as exc:
		print(f"Error: Cannot connect to Database\n{exc}")
		return
	try:
		db.validate_collection("upvoted_posts")
	except OperationFailure: pass
	else: 
		# if collection already exists (should), create a backup and drop collection
		old_posts = db.upvoted_posts.find()
		db.drop_collection("upvoted_posts")

	db.create_collection("upvoted_posts")

	try:
		update_coll(db.upvoted_posts, upvoted)
	except PyMongoError as exc:
		# if an error occurs when adding new data to collection, add old data back
		db.upvoted_posts.insert_many(old_posts)
		print(f"Error inserting posts into collection\n{exc}")


if __name__ == '__main__':
	main()
