import flask
from flask import send_from_directory
import game
app = flask.Flask(__name__)


@app.route('/')
def home():
   return flask.render_template('Transmutation.html')


if __name__ == '__main__':
    app.run()

