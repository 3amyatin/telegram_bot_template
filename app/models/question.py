from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    question_text = Column(String, nullable=False)
    answer1 = Column(String, nullable=False)
    answer2 = Column(String, nullable=False)
    answer3 = Column(String, nullable=False)
    answer4 = Column(String, nullable=False)
    correct_answer = Column(Integer, nullable=False)
    score_right = Column(Integer, nullable=False)
    score_wrong = Column(Integer, nullable=False)