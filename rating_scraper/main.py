from asyncio import constants
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from scraper import scrap_rating
import json, concurrent.futures

MAX_THREADS = 30

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['POST'])
@cross_origin()
def return_ratings():
    # request.form['titles']
    data = request.get_json()
    # threads = min(MAX_THREADS, len(data))
    # res = {data['title']: scrap_rating(data)}
    # with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    #     futures = {executor.submit(scrap_rating, title): title for title in data}
    # for f in concurrent.futures.as_completed(futures):
    #     res[futures[f]["title"]] = f.result()
    return json.dumps(scrap_rating(data))
