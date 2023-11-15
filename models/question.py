from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, Sequence('question_id_seq'), primary_key=True)
    question_text = Column(String(255))
    answer_text = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
