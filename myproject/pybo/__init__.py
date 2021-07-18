from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

from . import models

def create_app():

    app = Flask(__name__)

    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint
    from .views import main_views
    app.register_blueprint(main_views.bp)

    from .views import question_views
    app.register_blueprint(question_views.bp)

    from .views import answer_views
    app.register_blueprint(answer_views.bp)

    from .views import auth_views
    app.register_blueprint(auth_views.bp)

    # Filter
    from .filter import format_datetime
    # datetime이라는 이름으로 필터 등록
    app.jinja_env.filters['datetime'] = format_datetime
    
    return app