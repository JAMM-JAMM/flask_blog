from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

from . import models

def page_not_found(e):
    return render_template('404.html'), 404

def server_error(e):
    return render_template('500.html'), 500

def create_app():

    app = Flask(__name__)

    app.config.from_object(config)

    # ORM
    db.init_app(app)
    
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    
    from . import models

    # Blueprint
    from .views import main_views
    app.register_blueprint(main_views.bp)

    from .views import question_views
    app.register_blueprint(question_views.bp)

    from .views import answer_views
    app.register_blueprint(answer_views.bp)

    from .views import auth_views
    app.register_blueprint(auth_views.bp)

    from .views import comment_views
    app.register_blueprint(comment_views.bp)

    from .views import vote_views
    app.register_blueprint(vote_views.bp)

    # Filter
    from .filter import format_datetime
    # datetime이라는 이름으로 필터 등록
    app.jinja_env.filters['datetime'] = format_datetime

    # Markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # 오류 페이지
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)
    
    
    return app