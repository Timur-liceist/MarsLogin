from io import BytesIO

import requests
from PIL import Image
from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.utils import redirect

from data import db_session, users_api
from data import jobs_api
from data.geocoder import get_ll_span, get_coordinates
from data.users import User
from forms.reg_form import RegisterForm
from forms.user_login import LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "yandex_liceist"


@app.route("/auto_answer")
def auto_answer():
    return render_template("auto_answer.html")

@app.route("/")
def news():
    return render_template("index.html")


@app.route('/users_show/<int:user_id>')
def show_map(user_id):
    # try:
    print(1)
    user = requests.get(f"http://127.0.0.1:5000/api/users/{user_id}").json()
    print(2)
    user = user["user"]
    print(3)
    address = user["address"]
    print(4)
    toponym_to_find = address
    print(5)
    ll = ",".join(map(str, get_coordinates(toponym_to_find)))
    print(6)
    map_params = {
        "ll": ll,
        "spn": get_ll_span(toponym_to_find)[1],
        "l": "sat"
    }
    print(7)
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    print(8)
    response = requests.get(map_api_server, params=map_params)
    print(9)
    Image.open(BytesIO(
        response.content)).save("static/img/img.png")
    print(10)
    return render_template("using_api.html", address=address, name=user["name"], surname=user["surname"])
    # except Exception:
    #     return "<h1>Not found user</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# @app.route("/answer")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.login.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == "__main__":
    db_session.global_init("db/blog.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()
