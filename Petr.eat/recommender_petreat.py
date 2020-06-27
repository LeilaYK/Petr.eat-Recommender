import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec, FastText

# 첫 번째 모듈
class Recommend_items:
    def __init__(self, data_path):
        with open(data_path, encoding="UTF-8") as f:
            self.data = json.load(f)
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
