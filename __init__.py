from flask import Flask, render_template
import sys
import os
sys.path.append(os.path.join(os.getcwd(), ''))
SECRET_KEY = b'\x143#\x1eV;\xc9\xa0\xecr\r\xd4/{b\n'

app = Flask(__name__)
app.config.from_object(__name__)


def create_app():
    #from web_app.flask_parser.flask_parser import parser_blueprint
    #from hh_parser.web_app.authorization.auth import auth_blueprint
    #app.register_blueprint(parser_blueprint)
    #app.register_blueprint(auth_blueprint)

    return app


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
