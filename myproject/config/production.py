from config.default import *


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xda\x18$\xf0\x037H\xc5h\xf8\xec\x7fZ)\xf1\xf5'