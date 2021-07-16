from pybo import db


# 질문 모델 속성
# id: 질문 데이터의 고유 번호
# subject: 질문 제목
# content: 질문 내용
# create_date: 질문 작성일시

'''
Question 클래스는 모든 모델의 기본 클래스인 db.Model을 상속받는다.
이 때, db는 '__init__.py' 파일에서 생성한 SQLAlchemy 객체이다.
질문 모델은 id, subject, content, create_date 속성으로 구성되었으며,
각 속성은 db.Column() 클래스를 사용하여 생성했다.
db.Column 클래스의 첫 번째 인수는 각 속성의 데이터 타입을 의미한다.
db.Integer: 고유 번호와 같은 숫자 값
db.String: 글자 수가 제한된 텍스트
db.Text: 글자 수를 제한할 수 없는 텍스트
db.DateTime: 날짜와 시각
''' 

# 데이터베이스에서 id와 같은 특징을 가진 속성을 기본 키(primary_key)라고 한다.
# 플라스크는 데이터 타입이 db.Integer이고 primary key로 지정한 속성은 값이 자동으로 증가하는 특징이 있다.
# 따라서, 데이터를 저장할 때 해당 속성값을 지정하지 않아도 1씩 자동으로 증가하여 저장된다.

# nullable: 속성에 빈값을 허용할 것인지를 결정한다.
# default 값은 True로 빈값을 허용한다.

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

# 답변 모델 속성
# id: 답변 데이터의 고유 번호
# question_id: 질문 데이터의 고유 번호(어떤 질문에 달린 답변인지 알아야 하므로)
# content: 답변 내용
# create_date: 답변 작성일시

'''
question_id 속성은 답변 모델이 어떤 질문에 대한 답변인지 표시해야 하므로
질문 모델과 연결된 속성을 포함해야 함. 이처럼 어떤 속성을 기존 모델과 연결하려면
db.ForeignKey()를 사용해야 한다.

db.ForeignKey에서 지정한 첫 번째 값인 'question(테이블명).id(컬럼명)'는 Question 모델의 id 속성을 의미한다.

db.ForeignKey에서 지정한 두 번째 값인 'ondelete'에 지정한 값은 삭제 연동 설정이다.
즉, 답변 모델의 question_id 속성은 질문 모델의 id 속성과 연결되며 ondelete='CASCADE'에 의해
데이터베이스에서 쿼리를 이용하여 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제된다.

정확히 말하면, 질문 데이터를 삭제했을 때 해당 질문과 연관된 답변 데이터는 삭제되지 않고 답변 데이터의
question_id 컬럼만 빈 값으로 업데이트된다.
만약 파이썬 코드로 질문 데이터를 삭제할 때, 연관된 답변 데이터가 모두 삭제되기를 바란다면
question 속성의 db.backref 설정에서 cascade='all, delete-orphan' 옵션을 추가해주면 된다.
'''

'''
question 속성은 답변 모델에서 질문 모델을 참조하기 위해 사용된다.
이 때, 주의할 점은 기존의 모델을 참조하는 것이기 때문에 db.Column이 아닌 db.relationship()을 사용해야 한다.

db.relationship에서 첫 번째 값은 참조할 모델명이다.

db.relationship에서 두 번째 backref에 지정한 값은 역참조 설정이다.
역참조란 쉽게 말해서 '질문'에서 '답변'을 참조하는 것을 의미한다.
예를 들어, 한 질문에 여러 개의 답변이 달릴 수 있는데 역참조는 이 질문에 달린 답변을 참조할 수 있게 한다.
어떤 질문에 해당하는 객체가 a_question이라고 한다면, a_question.answer_set을 사용하여
a_question에 달린 여러 개의 답변을 참조할 수 있다.
'''

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)