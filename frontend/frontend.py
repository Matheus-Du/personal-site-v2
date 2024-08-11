from flask import Flask, render_template, session, request, send_file
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

@app.route("/books/", methods=['GET'])
def books():
    if not htmx:
        return "Error getting recently liked posts"
    books = requests.get(f"http://api:5000/getBooks")
    return books.text

@app.route("/getResume", methods=['GET'])
def getResume():
    return send_file('static/files/Matheus Duncan Resume.pdf', mimetype='application/pdf')

@app.route("/blog")
def blogHome():
    return render_template("/pages/blog.html")

@app.route("/blog/homeServer")
def postHomeServer():
    return render_template("/pages/blog_posts/homeServer.html")

@app.route("/bookshelf")
def bookshelf():
    return render_template("/pages/bookshelf.html")

@app.route("/projects")
def projects():
    return render_template("/pages/projects.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("/pages/404.html"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)