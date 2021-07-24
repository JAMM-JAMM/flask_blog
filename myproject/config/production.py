from config.default import *


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATION = False
SECRET_KEY = b'V\x1e\xb0Iw\x06J!i\x17\xaa\xce\x07\xb2\x97\r'