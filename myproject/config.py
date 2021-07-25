import os

# 루트 디렉토리인 'myproject' 폴더의 절대 경로
BASE_DIR = os.path.dirname(__file__)

# 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLAlchemy의 이벤트를 처리하는 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 사실 SECRET_KEY = 'dev'는 위험한 설정이다.
# 실제 서비스를 운영할 때에는 "dev"처럼 유추하기 쉬운 문자열을 입력하면 안된다.
# 현재는 개발환경이기 때문에 괜찮지만, 실제 서비스 운영 환경에서는 SECRET_KEY를 변경해줘야 한다.
SECRET_KEY = 'dev'