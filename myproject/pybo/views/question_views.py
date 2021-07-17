from datetime import datetime
from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from .. import db

from ..models import Question
from ..forms import QuestionForm, AnswerForm

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=['GET', 'POST'])
def create():
    form = QuestionForm()
    # request.method는 create 함수로 요쳥된 전송 방식을 의미
    # form.validate_on_submit 함수는 전송된 폼 데이터의 정합성 점검 
    # (폼을 생성할 때, 각 필드에 지정한 점검 항목에 이상이 없는지 확인)
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)