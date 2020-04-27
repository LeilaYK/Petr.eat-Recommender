from flask import Flask, request, jsonify
import numpy as np
import json
from petreat_recommend import Recommend_items

app = Flask(__name__)

item2sim = json.load(open('petreat.json', 'r'))

reco = Recommend_items(item2sim)

def item_to_json(item_ids):
    return jsonify({'recommend': item_ids})

@app.route('/')

@app.route('/recommend', methods=['GET'])
def recommend():
    args = request.get_json(force=True)
    recommend_type = args.get('recommend_type', None)
    itemTitle = args.get('recent_items', [])
    recommend_items = []

    if recommend_type == 'recommend_id':
        recommend_items = reco.recommend_id(item2sim, itemTitle)
    elif recommend_type == 'recommend_json':
        recommend_items = reco.recommend_json(item2sim, itemTitle)
    print(recommend_items)
    return item_to_json(recommend_items)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
