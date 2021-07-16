from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

# 중요!
# db 객체를 create_app 함수 안에서 생성하면 블루프린트와 같은 다른 모듈에서 불러올 수 없다.
# 따라서, db와 migrate 객체를 create_app 함수 밖에서 전역 변수로 선언하고
# create_app 함수 안에서 'init_app' 메서드를 이용하여 객체를 초기화해야 함.
db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)

    # config.py 파일에 작성한 항목을 app.config 환경 변수로 부르기 위해
    # app.config.from_object(config) 코드 추가
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main_views
    app.register_blueprint(main_views.bp)
    
    return app