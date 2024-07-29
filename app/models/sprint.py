from sqlalchemy import Column, String, UniqueConstraint

from app.models.db import BaseDatabase, database


class Sprint(BaseDatabase):
    __tablename__ = "sprint"
    name = Column(String)
    UniqueConstraint(name)

　　

# how can i get foreign key?
@staticmethod
def get_or_create(name):
    session = database.connect_db()
    # 最初のを持ってきてあるかどうかチェック
    row = session.query(Sprint).filter(Sprint.name == name).first()
    if row:
        session.close()
        return row
    # なければデータ作成で終わり！
    sprint = Sprint(name=name)
    session.add(sprint)
    session.commit()

    row = session.query(Sprint).filter(Sprint.name == name).first()
    session.close()
    return row







