from os import getenv
from flask import Flask
from flask import render_template

from tuck import auth

from tuck.db import db_session

app = Flask(__name__, instance_relative_config=True)

app.secret_key = getenv("APP_SECRET", "ElsyagfankAmfuffyobshinagCowbij8")

app.register_blueprint(auth.bp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
@auth.login_required
def hello_world():
    return render_template("index.html", content="hello world.")


app.add_url_rule("/", endpoint="index")
