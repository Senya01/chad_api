import json
from libs import TimeCalc
from flask import Flask

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def load_config():
    with open("config.json") as f:
        return json.load(f)


@app.route('/')
def index():
    return {}


@app.route("/time/<user_id>")
def time(user_id):
    time_calc = TimeCalc.TimeCalc(load_config())
    return time_calc.main(user_id)


if __name__ == '__main__':
    config = load_config()
    app.run(host=config['server']['host'], port=config['server']['port'])
