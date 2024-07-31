from flask import Flask, render_template, Response, make_response
from flask_htmx import HTMX
from pymongo import MongoClient
import os

app = Flask(__name__)
htmx = HTMX(app)
htmx.init_app(app)

def get_hn_posts():
    conn = MongoClient(f"mongodb://{os.environ['MONGOUN']}:{os.environ['MONGOPW']}@mongo:27017/")
    db = conn.personal_site
    hn_posts = [post for post in db.upvoted_posts.find().limit(5)]
    posts_html = []
    for post in hn_posts:
        #posts_html.append(f"Title: {post.get('title')}\nLink: {post.get('link')}\nDate: {post.get('link')}\nDisc: {post.get('discussion_link')}")
        posts_html.append(render_template("elements/recentLike.html",
                                          title=post.get('title'), 
                                          link=post.get('link'), 
                                          date=post.get('date_posted'), 
                                          hn_link=post.get('discussion_link')))
    return "".join(posts_html)

@app.route("/")
def main():
    return render_template("home.html")

@app.route("/upvotedPosts")
def upvoted():
    if htmx:
        posts = get_hn_posts()
        return posts
    else:
        return "Error getting recently liked posts"

@app.route("/blog")
def blogHome():
    return render_template("/blog/blogHome.html")

@app.route("/getRecentLikes")
def showLikesInfo():
    if htmx:
        return render_template("/elements/recentLikes.html")
    return Response(status=400)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("/pages/404.html"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)