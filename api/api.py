from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)

#app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route("/")
def main():
    return render_template("home.html")

@app.route("/blog")
def blogHome():
    return render_template("/blog/blogHome.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)