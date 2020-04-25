import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class Recommend_items:
    def __init__(self, data_path='/Users/junghyunwoo/혀누에-의한-혀누를-위한-혀누의/일 관련/changer/Petr.EAT/petreat.json'):
        self.data_path = data_path
    
    def load_data(self, path):
        return json.load(open(self.data_path,'r'))
    
    def recommend_item(self, title):
        data = self.load_data(self.data_path)
        item = [item for item in data if item['name']==title][0]
        score_series = pd.Series(np.array(item['similarity'])).sort_values(ascending = False)
        top_5_indices = list(score_series.iloc[1:6].index)
        recommended_items = []
        for i in top_5_indices:
            recommended_items.append(data[i]['name'])
        return recommended_items
    
    def recommend_id(self, title):
        data = self.load_data(self.data_path)
        item = [item for item in data if item['name']==title][0]
        score_series = pd.Series(np.array(item['similarity'])).sort_values(ascending = False)
        top_5_indices = list(score_series.iloc[1:6].index)
        recommended_items = []
        for i in top_5_indices:
            recommended_items.append(data[i]['id'])
        return recommended_items

    def recommend_json(self, title):
        data = self.load_data(self.data_path)
        item = [item for item in data if item['name']==title][0]
        score_series = pd.Series(np.array(item['similarity'])).sort_values(ascending = False)
        top_5_indices = list(score_series.iloc[1:6].index)
        recommended_items = []
        for i in top_5_indices:
            recommended_items.append(data[i])
        return recommended_items

# test = Recommend_items()
# test.recommend_item('오리황태말이')
## ['오리안심육포', '한입오리', '메추리', '소떡심', '무염황태체 ']

# test.recommend_id('오리황태말이')
## [17, 5, 33, 49, 7]

# test.recommend_json('오리황태말이')
## {'id': 17, 'name': '오리안심육포', 'BOW': '오리안심 단백질 불포화지방 피부 혈관', 'similarity': ...}