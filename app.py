import random
from flask import Flask, jsonify
app = Flask(__name__)

names = []

def loadFiles():
    names = []
    with open("names.txt", "r") as f:
        names = [n.strip() for n in f.readlines()]
    return names

def generate_matches():
    random.shuffle(names)
    matches = [names[i:i+2] for i in range(0, len(names), 2)]

    return matches

@app.route('/')
def generate():
    return jsonify(generate_matches())

if __name__ == '__main__':

    names = loadFiles()
    print("names loaded")
    print(names)

    app.run(host='0.0.0.0')


# save in (name1, name2): true dict
