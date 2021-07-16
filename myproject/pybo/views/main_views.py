from flask import Blueprint, render_template

from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    # 질문 목록은 Question.query.order_by로 얻을 수 있으며, 
    # 이 때 order_by 함수는 조회 결과를 정렬해준다.
    # 즉, Question.create_date.desc() 코드는 조회된 질문 목록을 '작성일시 기준 역순으로 정렬하라'라는 의미
    question_list = Question.query.order_by(Question.create_date.desc())
    # render_template 함수는 템플릿 파일을 화면에 그려준다. 조회된 질문 목록을 템플릿으로 전달하면
    # 전달받은 데이터(question_list)로 화면을 구성한다.
    return render_template('question/question_list.html', question_list=question_list)