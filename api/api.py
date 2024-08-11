from flask import Flask, render_template
from pymongo import MongoClient, DESCENDING
import os

app = Flask(__name__)
app.secret_key = os.environ['APPKEY']


def connect():
    conn = MongoClient(f"mongodb://{os.environ['MONGOUN']}:{os.environ['MONGOPW']}@mongo:27017/")
    db = conn.personal_site
    return db

def get_hn_posts(page):
    db = connect()
    hn_posts = [post for post in db.upvoted_posts.find().skip(page*5).limit(5)]
    posts_html = []
    for post in hn_posts:
        posts_html.append(render_template("elements/recentLike.html",
                                          title=post.get('title'), 
                                          link=post.get('link'), 
                                          date=post.get('date_posted'), 
                                          hn_link=post.get('discussion_link')))
    return "".join(posts_html)


def buildBookshelf():
    db = connect()
    books = [book for book in db.books.find().sort('date_read', DESCENDING)]
    books_html = []
    for book in books:
        tags = []
        for tag in book['tags']:
            tag_info = db.book_tags.find_one({'name': tag})
            tags.append(tag_info)

        books_html.append(render_template('elements/bookReview.html',
                                          title=book['title'],
                                          author=book['author'],
                                          isbn=book['isbn'],
                                          dateRead=f"{book['date_read'][4:]}/{book['date_read'][:4]}",
                                          review=book['review'],
                                          coverImage=book['cover_image'],
                                          tags=tags))
    return "".join(books_html)


def getReview(isbn):
    db = connect()
    book = db.books.find_one({'isbn': isbn})
    return book['review']


@app.route("/longReview/<isbn>")
def longReview(isbn):
    return render_template('elements/longReview.html', review=getReview(isbn), isbn=isbn)

@app.route("/shortReview/<isbn>")
def shortReview(isbn):
    return render_template('elements/shortReview.html', review=getReview(isbn), isbn=isbn)

@app.route("/getTag")
def getTag():
    return render_template('elements/bookTag.html', tagColour='#000000', tagName='Test Tag')

@app.route("/getUpvoted/<page>")
def getUpvoted(page=0):
    return get_hn_posts(int(page))

@app.route("/getBooks")
def getBooks():
    return buildBookshelf()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)