from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


# QuestionForm 클래스는 Flask-WTF 모듈의 FlaskForm 클래스를 상속받으며 subject, content 속성을 포함한다.
# 폼 클래스의 속성과 모델 클래스의 속성은 비슷하다.
# 글자 수 제한이 있는 '제목'은 StringField를 사용
# 글자 수 제한이 없는 '내용'은 TextAreaField를 사용
# 이를 플라스크 폼의 속성 또는 필드라고 한다.
# 각 필드의 첫 번째 인자는 폼 라벨로 사용되며, 템플릿에서 이 값으로 라벨을 출력할 수 있다.
# 각 필드의 두 번째 인자는 validators로 필드 값을 검증할 때 사용하는 도구다.
# 이는 필수 항목인지 점검하는 DataRequired, 이메일인지 점검하는 Email, 길이를 점검하는 Length 등이 있다.
# 예를 들어 필수값이면서 이메일이어야 한다면 validators=[DataRequired(), Email()]
class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])