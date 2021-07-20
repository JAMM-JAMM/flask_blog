from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db

from ..models import Question
from ..forms import QuestionForm, AnswerForm

from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    # localhost:5000/question/list/?page=5인 URL에서 GET 방식으로 요청했다면
    # page 값 5를 받는다.
    # localhost:5000/question/list인 URL에 page 값이 없다면 default=1을 자동으로 적용
    page = request.args.get('page', type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    # paginate 함수는 조회한 데이터를 감싸 Pagination 객체로 반환한다.
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestionForm()
    # request.method는 create 함수로 요쳥된 전송 방식을 의미
    # form.validate_on_submit 함수는 전송된 폼 데이터의 정합성 점검 
    # (폼을 생성할 때, 각 필드에 지정한 점검 항목에 이상이 없는지 확인)
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=['GET', 'POST'])
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)

    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question_list'))