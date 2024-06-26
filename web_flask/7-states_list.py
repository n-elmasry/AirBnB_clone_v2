#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from operator import attrgetter


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def state_list():
    """display the states"""
    all_states = list(storage.all(State).values())
    sorted_states = sorted(all_states, key=attrgetter('name'))
    return render_template("7-states_list.html", states=sorted_states)


@app.teardown_appcontext
def teardown_db(self):
    """call close method"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
