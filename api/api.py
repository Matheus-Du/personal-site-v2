from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def main():
    return render_template("home.html")

@app.route("/blog")
def blogHome():
    return render_template("/blog/blogHome.html")