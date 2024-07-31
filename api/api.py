from flask import Flask, render_template, Response, session, request
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.environ['APPKEY']

def get_hn_posts(page):
    conn = MongoClient(f"mongodb://{os.environ['MONGOUN']}:{os.environ['MONGOPW']}@mongo:27017/")
    db = conn.personal_site
    hn_posts = [post for post in db.upvoted_posts.find().skip(page*5).limit(5)]
    posts_html = []
    for post in hn_posts:
        posts_html.append(render_template("elements/recentLike.html",
                                          title=post.get('title'), 
                                          link=post.get('link'), 
                                          date=post.get('date_posted'), 
                                          hn_link=post.get('discussion_link')))
    return "".join(posts_html)

@app.route("/getUpvoted/<page>")
def getUpvoted(page=0):
    return get_hn_posts(int(page))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)