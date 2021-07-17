from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

# create 함수의 매개변수 question_id는 URL에서 전달된다.
# 만약 localhost:5000/answer/create/2/ 페이지를 요청받으면
# question_id에는 2가 넘어온다.
@bp.route('/create/<int:question_id>', methods=['POST'])
def create(question_id):
    question = Question.query.get_or_404(question_id)
    
    # form 엘리먼트를 통해 전달된 데이터들은 create 함수에서 request 객체로 얻을 수 있다.
    # request.form['content'] 코드는 POST 폼 방식으로 전송된 데이터 항목 중 name 속성이 'content'인 값을 의미한다.
    content = request.form['content']
    
    answer = Answer(content=content, create_date=datetime.now())
    
    # question.answer_set은 '질문에 달린 답변들'을 의미한다.
    # Question과 Answer 모델이 연결되어 있어 backref에 설정한 answer_set를 사용할 수 있다.
    question.answer_set.append(answer)

    '''
    answer = Answer(question=question, content=content, create_date=datetime.now())
    db.session.add(answer)
    '''
    
    db.session.commit()

    # redirect 함수에 사용한 question_id는 question_views.py 파일에 있는 detail 함수의 매개변수로 전달된다.
    return redirect(url_for('question.detail', question_id=question_id))