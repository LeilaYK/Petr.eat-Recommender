import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec, FastText


class Recommend_items:
    def __init__(self, data):
        self.data = data
        self.df = pd.DataFrame(self.data).T
        self.corpus = self.json_to_corpus()

    def list2str(self, data):
        result = ' '.join(data)
        return result

    def json_to_corpus(self):
        self.df['BOW'] = (self.df['ingredient'] + self.df['taglst']).apply(self.list2str)
        tokenized = ''
        for ingredient, tags in zip(self.df['ingredient'].values, self.df['taglst'].values):
            item_token = ''
            for token in ingredient:
                if token == '?':
                    continue
                else:
                    item_token = item_token + ' ' + token
            for tag in tags:
                    item_token = item_token + ' ' + tag
            tokenized = tokenized + "{} \n".format(item_token)
            corpus = [sent.strip().split(" ") for sent in tokenized.split('\n')]        
        return corpus

    def word_dictionary(self):
        embedding_model = Word2Vec(self.corpus, size=100, window = 2, min_count=1, workers=4, iter=1000, sg=1)

        word_dict = {}
        for vocab, vector in zip(embedding_model.wv.index2word, embedding_model.wv.vectors):
            vocab = vocab.lower()
            word_dict[vocab] = vector
        return word_dict

    def get_item_vector(self):
        corpus = self.json_to_corpus

        df = pd.DataFrame(self.data).T
        df['BOW'] = (df['ingredient'] + df['taglst']).apply(self.list2str)
        tfidf = TfidfVectorizer()
        tfidf_score = tfidf.fit_transform(df['BOW'])
        tfidf_feature_names = tfidf.get_feature_names()

        # 상품과 성분 매칭시켜주기
        product_dict = {}
        for bow, name in zip(self.corpus, df['title']):
            name = name.lower()
            product_dict[name] = bow

        # TF-IDF score 저장해주기
        tfidf_dict = {}
        for idx, val in zip(tfidf_score.indices, tfidf_score.data):
            word = tfidf_feature_names[idx].upper()
            tfidf_dict[word] = val

        list_column = []
        item_vector = {}
        for idx in df.index:
            list_vector =[]
            for ingre in product_dict[df['title'][idx]]:
                if ingre in tfidf_dict.keys():
                    list_vector.append(self.word_dictionary()[ingre] * tfidf_dict[ingre])
            item_vector[idx] = np.sum(list_vector, axis=0).tolist()
        return item_vector

    def recommend_ids(self, item_id, topn=5):
        similarity = {}
        target = item_id
        for item in self.data:
            if item != target:
                if np.array(self.data[item]['vector']).reshape(1,-1).shape[1] != 1:
                    sim = cosine_similarity(np.array(self.data[target]['vector']).reshape(1,-1), np.array(self.data[item]['vector']).reshape(1,-1))
                    similarity[item] = float(sim)
        rating = [key for key, value in sorted(similarity.items(), key=lambda item: item[1], reverse=True)]
        return rating[:topn]

class Form_filter():
    def __init__(self, data):
        self.data = data
        self.df = pd.DataFrame(data).T
        self.df['tag_list'] = [' '.join(map(str, l)) for l in self.df['tag_list']]

    def recommend_by_condition(self, disease_input):
        good_items = []
        for item in self.df.index:
            good = False
            for disease in disease_input:
                if disease in self.df.loc[item]['tag_list']:
                    good = True
            if good == True:
                good_items.append(item)
        return good_items
    
    def filter_allergy(self, allergy_input):
        cannot_eat_items = []
        for item in self.df.index:
            possible = True
            for allergy in allergy_input:
                if allergy in self.df.loc[item]['ingredient']:
                    possible = False
            if possible == False:
                cannot_eat_items.append(item)
        return cannot_eat_items
    
    def final_recommend(self, disease_input, allergy_input ):
#         tag_list = {"닭": ["닭발", "닭안심", "닭가슴살"], "오리": ["오리안심", "오리목뼈", "오리근위", "오리가슴살", "오리장각", "오리 도가니", "오리 연골"], "소": ["우족", "사골뼈", "소떡심", "소고기(홍두깨살)", "소 간", "소 힘줄"], "계란흰자": ["달걀"], "계란 노른자": ["달걀"], "고구마": ["고구마", "호박고구마"], "해바라기유": ["해바라기씨유"]}
        good_items = self.recommend_by_condition(disease_input)
        cannot_eat_items = self.filter_allergy(allergy_input)
        final_recommend = {}
        list_temp = []
        for good in good_items:
            possible = True
            for ingre in self.data[good]['ingredient']:
                for allergy in allergy_input:
                    if allergy in ingre:
                        possible = False
                        if possible == False:
                            break
                    if possible == False:
                        break
            if possible == True:
                list_temp.append(good)
        if len(list_temp) <= 3:
            more_items = self.data[list_temp[0]]['recommend_20'][:4]
            list_temp.extend(more_items)
        list_temp = list(set(list_temp))
        final_recommend['result'] = list_temp[:5]
        return final_recommend