import random
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

names = []
old_matches = {}


def loadFiles():
    global names, old_matches
    with open("names.txt", "r") as f:
        names = [n.strip() for n in f.readlines()]
    with open("old_matches.txt", "r") as f:
        old_matches_data = json.load(f)
        old_matches = {(match[0], match[1]): True for match in old_matches_data if len(match) == 2}
    print("names loaded:", names)
    print("old_matches loaded:", old_matches)


def generate_matches():
    while True:
        random.shuffle(names)
        matches = [names[i:i+2] for i in range(0, len(names), 2)]
        for match in matches:
            if tuple(match) in old_matches or tuple(match[::-1]) in old_matches:
                break
        else:
            return matches


@app.route('/save', methods = ['POST'])
def save():
    with open("old_matches.txt", "r") as f:
        old_matches_data = json.load(f)
    old_matches_data += request.get_json(force=True)
    with open("old_matches.txt", "w") as f:
        json.dump(old_matches_data, f)
    loadFiles()
    return "OK"


@app.route('/')
def generate():
    return jsonify(generate_matches())


if __name__ == '__main__':
    loadFiles()

    app.run(host='0.0.0.0')
