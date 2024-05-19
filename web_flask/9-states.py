#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from operator import attrgetter


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """display states"""
    all_states = storage.all(State).values()
    sorted_states = sorted(all_states, key=lambda x: x.name)
    return render_template("9-states.html", states=sorted_states)


@app.route("/states/<id>", strict_slashes=False)
def statesid(id):
    """displayes city id"""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown_db(self):
    """calls close method"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
