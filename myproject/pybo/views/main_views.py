from flask import Blueprint

# Blueprint 클래스로 객체를 생성할 때는 이름, 모듈명, URL 프리픽스 값을 전달해야 한다.
# 'main': 블루프린트 객체의 이름인 'main'은 나중에 함수명으로 URL을 찾아주는 url_for 함수에서 사용된다.
# __name__: 블루프린트 객체의 모듈명인 'main_views'
# url_prefix='/': 블루프린트 객체에서 특정 파일('main_views.py')에 있는 함수의 애너테이션 URL 앞에 기본으로 붙일 접두어 URL을 의미한다.
bp = Blueprint('main', __name__, url_prefix='/')

# bp는 Blueprint 클래스로 생성한 객체를 의미한다.
@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    return 'Pybo index'