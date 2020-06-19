from flask import Flask, request, jsonify
import numpy as np
import json
from recommender import Recommend_items, Form_filter

app = Flask(__name__)

with open('/Users/junghyunwoo/혀누에-의한-혀누를-위한-혀누의/일-관련/changer/Petr.EAT/petreat 문진표 recommend_20 ver1.0.json', 'r') as f:
    data = json.load(f)

reco = Form_filter(data)

def item_to_json(item_ids):
    return jsonify({'recommend': item_ids})

@app.route('/')

@app.route('/recommend', methods=['GET'])
def recommend():
    # args = request.get_json(force=True)
    # itemId = args.get('recommend_ids', [])
    user_disease = ['췌장', '암']
    user_allergy = ['닭', '오리', '황태']
    recommend_items = reco.final_recommend(user_disease, user_allergy)
    print(recommend_items)
    return recommend_items

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
