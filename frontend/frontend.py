from flask import Flask, render_template, Response, session, request
import requests
from flask_htmx import HTMX
import os

app = Flask(__name__)
app.secret_key = os.environ['APPKEY']
htmx = HTMX(app)
htmx.init_app(app)

@app.route("/")
def main():
    session['page'] = 0
    return render_template("home.html")

@app.route("/upvotedPosts/", methods=['GET', 'POST'])
def upvoted():
    if not htmx:
        return "Error getting recently liked posts"
    if request.method == 'GET':
        session['page'] = 0
    elif request.method == 'POST':
        session['page'] += 1
    posts = requests.get(f"http://api:5000/getUpvoted/{session['page']}")
    return posts.text

@app.route("/blog")
def blogHome():
    return render_template("/blog/blogHome.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("/pages/404.html"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)