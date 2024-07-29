import logging
from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey, String

import pandas as pd
from surprise import SVD, Dataset, NormalPredictor, Reader
from surprise.model_selection import cross_validate

import settings
from app.models.db import BaseDatabase, database
from app.models.project import Project

class Topic(BaseDatabase):
    __tablename__ = "topic"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    UniqueConstraint(name)
    user_id = Column(ForeignKey("user.id"))
    project_id = Column(ForeignKey("project.id"))

    @staticmethod
    def get_or_create(name):
        session = database.connect_db()
        # Lazy import to avoid circular dependency
        from app.models.user import User
        # 最初のを持ってきてあるかどうかチェック
        row = session.query(User).filter(User.name == name).first()
        if row:
            session.close()
            return row
        # なければデータ作成で終わり！
        topic = Topic(name=name)
        session.add(topic)
        session.commit()

        row = session.query(Topic).filter(Topic.name == name).first()
        session.close()
        return row
