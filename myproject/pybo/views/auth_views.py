from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            # flash는 필드 자체 오류가 아닌 프로그램 논리 오류를 발생시키는 함수이다.
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            # 세션은 request와 마찬가지로 플라스크가 자동으로 생성하여 제공하는 변수이다.
            # 세션은 플라스크 서버를 구동하는 동안에 영구히 참조할 수 있는 값이다.
            # session 변수에 user의 id값을 저장했으므로 다양한 URL 요청에 이 세션 값을 사용할 수 있다.
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

'''
@bp.before_app_request 애너테이션
이 애너테이션이 적용된 함수는 라우트 함수보다 먼저 실행된다.
즉, 앞으로 load_logged_in_user 함수는 모든 라우트 함수보다 먼저 실행될 것이다.

g는 플라스크가 제공하는 컨텍스트 변수이다. 
이 변수는 request 변수와 마찬가지로 [요청 -> 응답] 과정에서 유효하다.
session 변수에 user_id 값이 있으면 데이터베이스에서 이를 조회하여 g.user에 저장한다.
이렇게 하면 이후 사용자 로그인 검사를 할 때, session을 조사할 필요가 없다.
g.user에는 User 객체가 저장되어 있으므로, g.user 값만 있다면 여러 가지 사용자 정보(username, email 등)
추가로 얻어내는 이점이 있다.
'''
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

'''
logout 함수에는 세션의 모든 값을 삭제할 수 있도록 session.clear()를 추가
따라서, session에 저장된 user_id는 삭제될 것이며, 앞서 작성한 load_logged_in_user 함수에서
session의 값을 읽을 수 없으므로 g.user가 None이 될 것이다.
'''

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

'''
@login_required 애너테이션을 지정하면 login_required 데코레이터 함수가 먼저 실행된다.
-> login_required 함수는 g.user가 있는 지를 조사하여 없으면 로그인 URL로 리다이렉트하고
g.user가 있으면 원래 함수를 그대로 실행
'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view