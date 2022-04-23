import flask
from flask import jsonify, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


# Получение всех пользователей
# Получение одного пользователя
# Добавление пользователя
# Редактирование пользователя
# Удаление пользователя
@blueprint.route("/api/users", methods=["GET"])
def get_users():
    # try:
    print(1111111)
    sess = db_session.create_session()
    users = sess.query(User).all()
    # surname = sqlal
    # name = sqlalche
    # age = sqlalchem
    # position = sqla
    # speciality = sq
    # address = sqlal
    # email = sqlalch
    # hashed_password
    # modified_date =
    users = jsonify(
        {
            'users':
                [item.to_dict(only=(
                    "id",
                    'surname',
                    'name',
                    'age',
                    "position",
                    "speciality",
                    "address",
                    "email",
                    "hashed_password",
                    "modified_date"))
                    for item in users]
        }
    )
    return users
    # except Exception as e:
    #     return {
    #         "Message": e.__class__.__name__
    #     }


@blueprint.route("/api/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    try:
        sess = db_session.create_session()
        user = sess.query(User).filter(User.id == user_id).first()
        js = jsonify(
            {
                'user':
                    user.to_dict(only=(
                        "id",
                        'surname',
                        'name',
                        'age',
                        "position",
                        "speciality",
                        "address",
                        "email",
                        "hashed_password",
                        "modified_date"))
            }
        )
        return js
    except Exception as e:
        return {
            "Message": str(e)
        }


@blueprint.route("/api/users", methods=["POST"])
def add_user():
    try:
        sess = db_session.create_session()
        js = request.json
        user = User()
        user.surname = js["surname"]
        user.name = js["name"]
        user.age = js["age"]
        user.position = js["position"]
        user.speciality = js["speciality"]
        user.address = js["address"]
        user.email = js["email"]
        user.hashed_password = js["hashed_password"]
        user.modified_date = js["modified_date"]
        sess.add(user)
        sess.commit()
    except Exception:
        return {
            "Message": "Неверные параметры"
        }


@blueprint.route("/api/users/<int:user_id>", methods=["PUT"])
def redact_user(user_id):
    try:
        sess = db_session.create_session()
        js = request.json
        user = sess.query(User).filter(User.id == user_id).first()
        user.surname = js["surname"]
        user.name = js["name"]
        user.age = js["age"]
        user.position = js["position"]
        user.speciality = js["speciality"]
        user.address = js["address"]
        user.email = js["email"]
        user.hashed_password = js["hashed_password"]
        user.modified_date = js["modified_date"]
        sess.commit()
    except Exception:
        return {
            "Message": "Неверные параметры"
        }


@blueprint.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        sess = db_session.create_session()
        sess.query(User).filter(User.id == user_id).delete()
        sess.commit()
    except Exception:
        return {
            "Message": "Неверные параметры"
        }
