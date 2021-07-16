from flask import Flask

# 플라스크는 app 객체를 사용하여 여러 가지 설정을 진행한다. 
# 그런데 이와 같은 방식으로 app 객체를 전역으로 사용하면 프로젝트 규모가 커질수록 문제가 발생할 확률이 높아진다.
# 순환 참조(circular import) 오류가 대표적이다.

# 이 문제를 해결하기 위해 '애플리케이션 팩토리를 사용하라'고 플라스크 공식 홈페이지에서 권하고 있다.
# 애플리케이션 팩토리는 쉽게 말해 'app 객체를 생성하는 함수를 의미한다.

def create_app():

    app = Flask(__name__)

    # create_app 함수에 등록되었던 hello_pybo 함수 대신 블루프린트를 사용하도록 변경
    # 블루프린트를 사용하기 위해 'main_views.py' 파일에서 생성한 블루프린트 객체인 bp를 등록
    from .views import main_views
    app.register_blueprint(main_views.bp)
    
    return app

# create_app 함수가 app 객체를 생성하여 반환하도록 코드를 수정
# app 객체가 함수 안에서 사용되므로 hello_pybo 함수도 또한 create_app 함수 내에 포함
# 여기서 사용된 create_app 함수가 애플리케이션 팩토리이다.
# create_app은 플라스크 내부에서 정의된 함수명이므로, 다른 이름을 사용하면 정상 동작하지 않는다.