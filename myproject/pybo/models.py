from pybo import db


# 질문 모델 속성
# id: 질문 데이터의 고유 번호
# subject: 질문 제목
# content: 질문 내용
# create_date: 질문 작성일시

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)

# 답변 모델 속성
# id: 답변 데이터의 고유 번호
# question_id: 질문 데이터의 고유 번호(어떤 질문에 달린 답변인지 알아야 하므로)
# content: 답변 내용
# create_date: 답변 작성일시

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)

# 유저 모델 속성
# id: 유저 데이터의 고유 번호
# username: 사용자 이름
# password: 비밀번호
# email: 이메일

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# 댓글 모델 속성
# id: 댓글 고유 번호
# user_id: 댓글 작성자 (User 모델과 관계를 가짐)
# content: 댓글 내용
# create_date: 댓글 작성일시
# modify_date: 댓글 수정일시
# question_id: 댓글의 질문 (Question 모델과 관계를 가짐)
# answer_id: 댓글의 답변 (Answer 모델과 관계를 가짐)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete="CASCADE"), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))