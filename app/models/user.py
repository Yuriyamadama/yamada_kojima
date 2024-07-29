from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

import pandas as pd
from surprise import SVD, Dataset, NormalPredictor, Reader
from surprise.model_selection import cross_validate

import settings
from app.models.db import BaseDatabase, database


class User(BaseDatabase):
    __tablename__ = "user"
    name = Column(String, unique=True, nullable=False)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)

    # Define relationships
    topic = relationship("Topic", back_populates="users")
    projects = relationship("Project", back_populates="user")

    @staticmethod
    def get_or_create(name):
        session = database.connect_db()
        # Lazy import to avoid circular dependency
        from app.models.topic import Topic
        # 最初のを持ってきてあるかどうかチェック
        row = session.query(User).filter(User.name == name).first()
        if row:
            session.close()
            return row
        # なければデータ作成
        user = User(name=name)
        session.add(user)
        session.commit()

        row = session.query(User).filter(User.name == name).first()
        session.close()
        return row
