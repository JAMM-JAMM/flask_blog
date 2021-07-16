from flask import Flask

# 플라스크 애플리케이션을 생성하는 코드
# __name__이라는 변수에는 모듈명이 담긴다.
# 즉, 이 파일이 실행되면 pybo.py라는 모듈이 실행되는 것이므로
# __name__ 변수에는 'pybo'라는 문자열이 담긴다.

'''
app = Flask(__name__)
'''

# 특정 주소에 접속하면 바로 다음 줄에 있는 함수를 호출하는 플라스크의 데코레이터이다.
# 데코레이터란 기존 함수를 변경하지 않고 추가 기능을 덧붙일 수 있도록 해주는 함수이다.
'''
@app.route('/')
def hello_pybo():
    return 'Hello, Pybo!'
'''

# 플라스크는 app 객체를 사용하여 여러 가지 설정을 진행한다. 
# 그런데 이와 같은 방식으로 app 객체를 전역으로 사용하면 프로젝트 규모가 커질수록 문제가 발생할 확률이 높아진다.
# 순환 참조(circular import) 오류가 대표적이다.

# 이 문제를 해결하기 위해 '애플리케이션 팩토리를 사용하라'고 플라스크 공식 홈페이지에서 권하고 있다.
# 애플리케이션 팩토리는 쉽게 말해 'app 객체를 생성하는 함수를 의미한다.

def create_app():

    app = Flask(__name__)

    @app.route('/')
    def hello_pybo():
        return 'Hello, Pybo!'
    
    return app

# create_app 함수가 app 객체를 생성하여 반환하도록 코드를 수정
# app 객체가 함수 안에서 사용되므로 hello_pybo 함수도 또한 create_app 함수 내에 포함
# 여기서 사용된 create_app 함수가 애플리케이션 팩토리이다.
# create_app은 플라스크 내부에서 정의된 함수명이므로, 다른 이름을 사용하면 정상 동작하지 않는다.