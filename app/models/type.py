from sqlalchemy import Column, String, UniqueConstraint

from app.models.db import BaseDatabase, database


class Type(BaseDatabase):
    __tablename__ = "type"
    name = Column(String)
    UniqueConstraint(name)

　　

# how can i get foreign key?
@staticmethod
def get_or_create(name):
    session = database.connect_db()
    # 最初のを持ってきてあるかどうかチェック
    row = session.query(type).filter(Type.name == name).first()
    if row:
        session.close()
        return row
    # なければデータ作成で終わり！
    type = Type(name=name)
    session.add(type)
    session.commit()

    row = session.query(Type).filter(Type.name == name).first()
    session.close()
    return row







