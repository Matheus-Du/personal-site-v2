from flask import Flask, render_template, Response
from flask_htmx import HTMX

app = Flask(__name__)
htmx = HTMX(app)
htmx.init_app(app)

@app.route("/")
def main():
    return render_template("home.html")

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