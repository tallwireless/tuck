from os import getenv
from flask import Flask
from flask import render_template

from tuck import auth

from tuck.db import db_session

from tuck.device_views import DeviceClassView, DeviceView

app = Flask(__name__, instance_relative_config=True)

app.secret_key = getenv("APP_SECRET", "ElsyagfankAmfuffyobshinagCowbij8")

app.register_blueprint(auth.bp)


def register_api(view, endpoint, url, pk="id", pk_type="int"):
    view_func = view.as_view(endpoint)
    # view_func = auth.login_required(view.as_view(endpoint))
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=["GET"])
    app.add_url_rule(url, view_func=view_func, methods=["POST"])
    app.add_url_rule(
        "%s<%s:%s>" % (url, pk_type, pk),
        view_func=view_func,
        methods=["GET", "PATCH", "DELETE"],
    )


register_api(DeviceClassView, "device_class_api", "/api/device_class/", pk="id")
register_api(DeviceView, "device_api", "/api/device/", pk="id")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
@auth.login_required
def hello_world():
    return render_template("index.html", content="hello world.")


app.add_url_rule("/", endpoint="index")
