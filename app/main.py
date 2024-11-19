import os

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from database import Config
from forms import LoginForm, TovarForm, KupitForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = KupitForm()

    from models import Tovar
    tovars = Tovar.query.filter(Tovar.price > 300).order_by(desc(Tovar.name)).all()
    if form.validate_on_submit():
        print(form.kolvo.data)
        print(type(form.kolvo.data))
        return render_template('index.html', tovars=tovars, form=form)
    else:
        return render_template('index.html', tovars=tovars, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form3 = LoginForm()
    if form3.validate_on_submit():
        from models import User
        name = form3.username.data
        proverka = User.query.filter_by(name=name).one_or_none()
        if proverka is None:
            data = User(name=form3.username.data, password=form3.pasword.data, is_active=False)

            db.session.add(data)
            db.session.commit()
            flash('ПОЛЬЗОВАТЕЛЬ ' + name + ' ЗАРЕГИСТРИРОВАН')
            return redirect(url_for('index'))
        else:
            flash('ПОЛЬЗОВАТЕЛЬ ' + name + ' УЖЕ СУЩЕСТВУЕТ')
            return redirect(url_for('index'))
    return render_template('login.html', form2=form3)


@app.route('/tovar_add', methods=['GET', 'POST'])
def tovar_add():
    form = TovarForm()
    if form.validate_on_submit():
        from models import Tovar
        name = form.name.data
        price = form.price.data
        ostatok = form.ostatok.data
        data = Tovar(name=name, price=int(price), ostatok=int(ostatok))
        db.session.add(data)
        db.session.commit()
        flash('Товар добавлен')
        return redirect(url_for('index'))
    return render_template('tovar_add.html', form=form)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
