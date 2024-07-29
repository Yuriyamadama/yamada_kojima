from flask import Flask, redirect, render_template, request, url_for

from app.controllers.forms import RateForm, YesOrNoForm
from app.models.user import User
import settings

#上から理解する
#理解するのに時間がかかることを恐れない。

# to be hello.htmlで全てのデータを集約できるように。
## 1.make model
## 2.make rethome、いったんformはなしでOK
## 3.make hello.html


##ロボターでappでテンプレートの場所を追加
##
#さらにバックエンドのappにスタティックファイルの場所をせってい
app = Flask(__name__, template_folder='../../templates', static_folder='../../static')

#作成したappを元にwebserverclassを作成。
class WebServer(object):
    def start(self, debug=False):
        app.run(host="127.0.0.1", port=settings.PORT, debug=debug)

server = WebServer()


ROBOT_NANE = 'Rhizome'

#App routeでhtmlファイルを登録
#if request で受け取る、それをさらにリターンrender templateで渡す流れ
#ここでは、hellohtmlで、受け取ったデータを全て次のページで表示する。
@app.route("/", methods=["GET", "POST"])
def hello() -> str:
    if request.method == "POST":
        user_name = request.form.get("user_name").strip()
        user = User.get_or_create(user_name)
        restaurants = Rate.recommend_restaurant(user)
        if restaurants:
            form = YesOrNoForm(request.form)
            form.user_name.data = user_name
            return render_template("recommend_restaurant.html", user_name=user_name, restaurants=restaurants, form=form)

        form = RateForm(request.form)
        form.user_name.data = user_name
        return render_template("evaluate_restaurant.html", user_name=user_name, form=form)

    return render_template("hello.html", name=ROBOT_NANE)






