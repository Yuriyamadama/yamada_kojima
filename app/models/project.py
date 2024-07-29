・正規化について具体例とともに説明して。

・projectモデルでおかしなところを修正して。修正に当たって以下の四点を考慮して
・以下のようなテーブルの適切なリレーションを考慮したものにして
・projectは、以下のようなコントローラで、呼び出す前提
・以下のようなdb.py、つまるベースとなるデータベースがすでに設定されている前提
・コメントアウトした箇所を削除しないで。

・project.pyと同じ要領で、以下のmodelを作成して。



①Sprint:これはプロジェクトに対する小タスク、つまりスプリントのテーブルです。
カラムはsprint1_start_date,sprint1_end_date,sprint1_name,sprint2_start_date,sprint2_end_date,sprint2_name,sprint3_start_date,sprint3_end_date,sprint3_name

このようなイメージです。
sprint1_start_time = Column(Date, nullable=True)
sprint1_end_time = Column(Date, nullable=True)

②Topic:これはプロジェクトのトピックを決めるテーブルです。プロジェクトがどのようなトピックに分類されるのか整理するテーブルです。例えば、福祉系、教育系などのトピック。
カラムはname,user_id,project_id
このようなイメージです。
name = Column(String)
UniqueConstraint(name)
user_id = Column(ForeignKey("user.id"))
project_id = Column(ForeignKey("project.id"))

③User:ユーザに関するテーブルです。関心のあるトピックや、コミットしているプロジェクトなどに関する情報とユーザ名、ユーザidなどを管理するテーブルです。
カラムはname,topic_id,project_id

from sqlalchemy import Column, String, UniqueConstraint, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

#ベースデータベースをインポート
from app.models.db import BaseDatabase, database

class Project(BaseDatabase):
    __tablename__ = "project"
    name = Column(String, unique=True, nullable=False)
    to_be = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    module_1 = Column(String, nullable=True)
    module_2 = Column(String, nullable=True)
    module_3 = Column(String, nullable=True)
    module_4 = Column(String, nullable=True)
    module_5 = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="projects")
    topic = relationship("Topic", back_populates="projects")


    # initでクラスを初期化
    def __init__(self, name, to_be, type, sprint_start_time=None, sprint_end_time=None, module_1=None, module_2=None,
                 module_3=None, module_4=None, module_5=None, user_id=None):
        self.name = name
        self.to_be = to_be
        self.type = type
        self.sprint_start_time = sprint_start_time
        self.sprint_end_time = sprint_end_time
        self.module_1 = module_1
        self.module_2 = module_2
        self.module_3 = module_3
        self.module_4 = module_4
        self.module_5 = module_5
        self.user_id = user_id


    @staticmethod
    def get_or_create(name, to_be, type, sprint_start_time=None, sprint_end_time=None, module_1=None, module_2=None,module_4=None,module_5=None,user_id=None)
        # make a session from base database
        session = database.connect_db()
        #session からrowを持ってくる
        #session.query(database name).filter(filter).first()←最初のやつ
        row = session.query(Project).filter(User.name == name).first()

        #もし、一行でも存在するならrowを返して終わり
        if row:
            session.close()
            return row
        #なければ、projectを作成
        project = Project(name=name)
        session.add(project)
        session.commit()

        row = session.query(Project).filter(Project.name == name).first()
        session.close()
        return row



    """Here we access the model for the first time. First, import the model in the controller,
    check if the first line exists, commit the session if it doesn't, and create the database.
    Put it as a static method in the model."""
