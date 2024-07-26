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
    hn_posts = db.upvoted_posts.find().limit(5)
    post_data = [post for post in hn_posts]
    return f"{post_data}"

@app.route("/")
def main():
    return render_template("home.html")

@app.route("/upvotedPosts")
def upvoted():
    posts = get_hn_posts()
    return posts

@app.route("/blog")
def blogHome():
    return render_template("/blog/blogHome.html")

@app.route("/getRecentLikes")
def showLikesInfo():
    if htmx:
        return render_template("/elements/recentLike.html")
    return Response(status=400)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("/pages/404.html"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)