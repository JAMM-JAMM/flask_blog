from flask import Blueprint, url_for
from werkzeug.utils import redirect

from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

# redirect: 입력받은 URL로 리다이렉트 해준다.
# url_for: 라우트가 설정된 함수명으로 URL을 역으로 찾아준다.
@bp.route('/')
def index():
    # url_for 함수에 전달된 'question._list'는 question, _list 순서로 해석되어 함수명을 찾는다.
    # question은 등록된 블루프린트 이름, _list는 블루프린트에 등록된 함수명이다.
    # 현재 _list 함수에 등록된 라우트는 @bp.route('/list/')이므로 
    # url_for('question._list')는 bp 객체의 url_prefix인 '/question/'과 '/list/'가 더해진
    # '/question/list/' URL을 반환한다.
    return redirect(url_for('question._list'))