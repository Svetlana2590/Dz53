from flask import Flask, render_template, flash, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from database import Config
from forms import LoginForm, TovarForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import User, Tovar

with app.app_context():
    db.create_all()
    have_user = User.query.first()
    print(have_user)
    if not have_user:
        from seed import seeds
        seeds()


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form3 = LoginForm()
    if form3.validate_on_submit():
        name = form3.username.data
        data = User(name=form3.username.data, password=form3.pasword.data, is_active=False)
        db.session.add(data)
        db.session.commit()
        flash('ПОЛЬЗОВАТЕЛЬ ' + name + ' ЗАРЕГИСТРИРОВАН')
        return redirect(url_for('index'))
    return render_template('login.html', form2=form3)


@app.route('/tovar_add', methods=['GET', 'POST'])
def tovar_add():
    form = TovarForm()
    if form.validate_on_submit():
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
    # with app.app_context():
    #     db.create_all()
    app.run(port=5001, debug=True)
