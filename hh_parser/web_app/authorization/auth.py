from binascii import hexlify
from datetime import datetime
from hashlib import sha256, pbkdf2_hmac
from os import urandom

from flask import Blueprint, render_template, request, redirect, \
    flash, session

from web_app.database import db_session
from web_app.models import User

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """
       Функция регистрации пользователя
    :return: Страницы Login или Register
    """
    if request.method == "POST":
        # Достаем из формы данные пользователя
        username = request.form["FirstName"]
        lastname = request.form["LastName"]
        email = request.form["Email"]
        password = request.form["Password"]
        repeat_password = request.form["RepeatPassword"]
        # Проверяем был ли зарегистрирован пользователь с таким
        # же адресом электронной почты
        row = db_session.query(User).filter(User.email == email).all()
        # Если пользователя с таким же адресом Email нет, то регистрируем его
        if not row:
            # Проверяем пароль
            if password != repeat_password:
                flash("Ошибка при вводе паролей")
            else:
                # Хешируем пароль
                h_password = hash_password(password)
                user = User(username, lastname, email, datetime.now(),
                            h_password)
                db_session.add(user)
                db_session.commit()
                # Отправляем пользователя на страницу авторизации
                return redirect("login")
        else:
            # Если пользователь с таким же адресом существует, то выдаем ошибку
            flash(
                "Такой пользователь уже зарегистрирован. "
                "Используйте другой адрес электронной почты.")
            return redirect("register")
    return render_template("register.html")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """
        Функция авторизации
    :return:
    """
    if request.method == "POST":
        # Достаем из формы данные о пользователе
        email = request.form["Email"]
        password = request.form["Password"]
        # Находим пользователя в БД
        row = db_session.query(User).filter(User.email == email).all()
        # Если пользователь не найден выдаем сообщение об ошибке
        if not row:
            flash("Такой пользователь не зарегестрирован.")
        else:
            # Если пользователь существует
            user_id = row[0].id
            user_name = row[0].name
            h_password = row[0].password
            # Проверяем правильность введеного пароля
            if verify_password(h_password, password):
                # Если пароль указан правильно, то отправляем пользователя на главную страницу
                session["user_name"] = user_name
                session["user_id"] = user_id
                return redirect("index")
            else:
                # Если пароль не правильный, то выдаем сообщение об ошибке
                flash("Указан неверный пароль")

    return render_template("login.html")


@auth_blueprint.route("/logout", methods=["POST", "GET"])
def logout():
    """
        Функция завершения сессии работы
    :return:
    """
    if request.method == "POST":
        # Удаляем из сессии атрибуты пользователя
        del session["user_id"]
        del session["user_name"]
        return redirect("login")
    return render_template("logout.html")


def hash_password(password):
    """Hash a password for storing."""

    salt = sha256(urandom(60)).hexdigest().encode('ascii')
    print(f"1-{urandom(60)}, 2-{sha256(urandom(60))}, "
          f"3-{sha256(urandom(60)).hexdigest()}, 4-{sha256(urandom(60)).hexdigest().encode('ascii')}")
    pwdhash = pbkdf2_hmac('sha512', password.encode('utf-8'),
                          salt, 100000)
    print(f"5-{pwdhash}")
    pwdhash = hexlify(pwdhash)
    print(f"6-{pwdhash}")
    print(f"7-{(salt + pwdhash).decode('ascii')}")
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    print(f"8-{stored_password, provided_password}")
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    print(f"9-{salt}")
    stored_password = stored_password[64:]
    print(f"10-{stored_password}")
    pwdhash = pbkdf2_hmac('sha512',
                          provided_password.encode('utf-8'),
                          salt.encode('ascii'),
                          100000)
    print(f"11-{pwdhash}")
    pwdhash = hexlify(pwdhash).decode('ascii')
    print(f"12-{pwdhash}")
    return pwdhash == stored_password
