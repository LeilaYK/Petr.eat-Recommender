# `Petr.eat Recommender (반려동물 간식 추천시스템)`
`#NLP` `#word2vec` `#Flask` `#ngrok`

# 1. Petr.eat 서비스 소개
- Petr.eat은 `인공지능 기반으로 반려동물 수제간식을 추천`해주는 커머스 플랫폼이다.
- 기존 반려동물 간식을 제공해주는 사이트에서는 추천시스템을 사용하고 있지 않았다. 그래서 수제간식을 반려동물의 상태(건강, 알러지, 기호식품 등)에 따라 추천해주는 서비스를 만들고자 했다.
- 상품별로 효능, 성분, #태그 등의 상품정보가 있었고 이를 기반으로 한 추천시스템을 만들었다. int로 된 값들은 아예 없었고 모두 텍스트 기반이었다.
- 내가 Petr.eat에서 `추천시스템 개발`을 맡았다.

---

# 2. 추천방식
- 약 15여개 업체에서 공급받기로 한 상품은 약 100여개였다. 각 상품별로 유사한 상품과 반려동물 상태를 고려한 filter를 개발하고자 하였다.
- 사용자의 구매내역에 따른 collaborative filtering과 log data에 따른 추천시스템도 구축해보고자 했으나 사용자 데이터의 부족으로 하지 못하였다.
- 크케 추천시스템을 3가지 단계로 만들어보았다.
  - TF-IDF
  - Word2vec & TF-IDF
  - Recommender with Filter
  
## 2-1) TF-IDF 추천
- 처음에는 TF-IDF로 추천시스템을 만들었다. 
- 가장 간단한 추천방식으로 [이곳](https://towardsdatascience.com/how-to-build-from-scratch-a-content-based-movie-recommender-with-natural-language-processing-25ad400eb243)에 나오는 코드를 따라서 만들었다.
- 단점
  > - TF-IDF를 활용한 추천시스템은 상품의 개수가 변함에 따른 유동적인 대처가 불가능했다. 
  > - 상품이 하나씩 추가될 때마다 모든 TF-IDF score를 다시 계산해야해서 서비스에 반영하기는 어려웠다.
  > - 또한 상품 고유벡터가 존재하지 않았다. 그래서 사용자의 구매여정(customer journey)에 따른 사용자 vector를 구하기 힘들었다.

## 2-2) word2vec & TF-IDF
- 그렇게 해서 만든 모델이 word2vec과 TF-IDF를 사용한 추천시스템이었다.
- 상품설명에 있는 모든 단어를 word2vec에 학습시켜서 단어별 고유 벡터를 만들었다. 또한 TF-IDF를 계산해서 단어의 출현빈도에 따른 score를 계산했다.
- 상품 내 성분별 벡터를 구한 뒤(word2vec에서 학습된 단어 벡터에 TF-IDF score를 곱함) 모든 성분별 벡터를 더해서 상품별 vector를 만들었다.
- 상품별 고유 벡터가 생겨서 추천시스템이 훨씬 원활해졌다.
- `recommender.py`참조

## 2-3) Recommender with Filter
- 마지막으로 반려동물의 건강상태, 기호식품, 알러지에 따라 상품이 필터링이 되어나오는 추천시스템을 만들었다.
- 반려동물 상태에 따라서 알러지 있는 상품들을 제거한 뒤, 기호식품과 건강상태에 좋은 음식들이 우선적으로 추천되게 만들었다.
- `recommender_filter.py`참조

---

# 3. 서버랑 API 주고받기
- 서버 구축 (Ruby-on-Rails) & 추천시스템 구축 (Python 3)
- Ruby-on-Rails에서 python 2까지만 호환이 된다고 해서 Flask로 Rails와 API를 주고받도록 구축했다.
- Rails에서 사용자 정보를 넘겨주면 Flask에서 사용자에 맞게 추천된 상품을 반환하는 형식

## 3-1) Flask 쓰는 방법은 요로로콤
``` python
 from flask import Flask, render_template, request, redirect, url_for  ## Web 구현용

 app = Flask(__name__)   # Flask 객체를 생성해주고
 
 @app.route('/home', methods=['POST'])   # 원하는 페이지를 렌더링!
 def index():
     return render_template('home.html')   # 인스턴스 내 templates 폴더에서 html 파일을 찾아서 실행

 @app.route('/index', methods=['POST'])  
     return render_template('index.html')   
 
 if __name__ == '__main__':
     app.run(host = '0.0.0.0')  # 모든 ip에 대해서 listen함. Flask를 실행해줌. 앞에 있어도 되고 뒤에 있어도 됨
```

## 3-2) ngrok로 외부에서 로컬서버 접속 환경 구성하기
- Flask를 AWS EC2에 올려보려고 했는데 실패했음. 그래서 Flask를 로컬에서 돌리고 외부에서 접속이 가능하도록 구축했다.
- 설치는 이렇게 하면 된다.
  - $ brew cask install ngrok
- 사용은 이렇게 하면 된다.
  - $ ngrok http 로컬서버포트
  - $ ngrok http 5000
