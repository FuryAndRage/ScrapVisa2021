from flask import Flask, render_template, jsonify, request
from scrap import Scraper
import os
import json
app = Flask(__name__)

@app.route('/')
def home():
    scrap = Scraper()
    return render_template('index.html', context = scrap.get_data_from_rows() )

@app.route('/api')
def api():
    base_dir = os.getcwd()
    path = os.path.join(base_dir, "static/")
    with open(f"{path}visa_2021.json", "r") as file:
        data = json.loads(file.read())
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)