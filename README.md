과연 성공할 것인가?

# 1. Petr.eat
- changer의 첫 번째 프로젝트! 반려동물 수제간식 커머스 플랫폼!

## 1-1) First milestone
 - 서버 구축 (Rails)
 - 추천시스템 구축 (TF-IDF score)
 - Flask로 Rails와 API를 주고받도록 구축
 
 - 후기
   > - 추천시스템이 python으로 되어있어서 Rails에서 호환이 안 되었음 (python 2.0을 >지원해서)  
   > - 그래서 AWS에 Flask 서버를 구축한 다음에 API를 송수신하려고 했음!  
   > - 와이파이에서는 성공적으로 작동함!
   > - AWS에서는 외부에서 아무리 접속해도 안 되길래 찾아본 결론은 "Flask Is Not Your Production Server"  
   > - Flask는 scale이 되지 않고 기본적으로 제공되는 내장 웹서버는 한 번에 한 사람만 접근하기에 적합하다는 것...  
   > - 그래서 갈아엎고 django로 다시 구축해보려고 함! 화이팅!
   
 - Flask 쓰는 방법은 간단하다!
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

## 1-2) ngrok로 외부에서 로컬서버 접속 환경 구성하기
- flask를 로컬에서 돌리는데 외부에서 접속이 가능하도록 구성하기
- 설치는 요로로콤
  - $ brew cask install ngrok
- 사용은 요로로콤
  - $ ngrok http 로컬서버포트
  - $ ngrok http 5000