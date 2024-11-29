import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import Config
from forms import LoginForm, TovarForm
from flask_login import LoginManager, current_user, login_user
import uuid

app = Flask(__name__, static_folder='static', template_folder='templates')
login_manager = LoginManager(app)

app.config.from_object(Config)
# Добавляем путь сохранения изображения
# Это так же можно сделать (и правильно сделать) в классе конфиг
app.config['UPLOAD_FOLDER'] = '/app/static'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import User, Tovar

with app.app_context():
    db.create_all()
    have_user = User.query.first()
    # print(have_user)
    if not have_user:
        from seed import seeds

        seeds()


@app.route('/')
def index():
    # form=GoTovarForm()
    tovar = Tovar.query.all()
    return render_template('index.html', tovars=tovar)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        print('*'*20)
        print(user)
        if user is None or not user.check_password(form.pasword.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('index'))
    return render_template('login_enter.html', form=form)

@app.route('/user_reg', methods=['GET', 'POST'])
def user_reg():
    form3 = LoginForm()
    if form3.validate_on_submit():
        name = form3.username.data
        data = User(name=form3.username.data, password=form3.pasword.data, is_active=False)
        db.session.add(data)
        db.session.commit()
        flash('ПОЛЬЗОВАТЕЛЬ ' + name + ' ЗАРЕГИСТРИРОВАН')
        return redirect(url_for('index'))
    return render_template('user_reg.html', form2=form3)


@app.route('/tovar_add', methods=['GET', 'POST'])
def tovar_add():

    form = TovarForm()
    print('Func add work')
    if form.validate_on_submit():

        # загрузка файла для дальнейшей обработки
        file = request.files['file']
        print(file.mimetype)

        rasshirenie = file.filename.split(".")[-1]
        print(rasshirenie)
        new_filename = uuid.uuid4().hex
        save_file_name = new_filename + '.' + rasshirenie
        list_ok = ['jpg', 'png']

        if rasshirenie not in list_ok:
            return 'Ne to!'

        # сохранение
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_file_name))

        name = form.name.data
        price = form.price.data
        ostatok = form.ostatok.data
        data = Tovar(name=name, price=int(price), ostatok=int(ostatok), url_photo=save_file_name)
        db.session.add(data)
        db.session.commit()
        flash('Товар добавлен')
        return redirect(url_for('index'))
    return render_template('tovar_add.html', form=form)


@app.route('/tovar_del/<tovar_id>', methods=['GET', 'POST'])
def del_tovar(tovar_id: int):
    data = Tovar.query.get(tovar_id)
    # data = Tovar.query.select(Tovar.id == tovar_id).one()
    # data = Tovar.query.where(Tovar.id == tovar_id).one()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/tovar_kupit', methods=['GET', 'POST'])
def tovar_kupit():
    id = request.args.get('id')
    print(id)
    data = Tovar.query.get(id)
    data.ostatok = data.ostatok - 1
    db.session.commit()
    print(data)
    return redirect(url_for('index'))


@app.route('/tovar_page', methods=['GET', 'POST'])
def tovar_page():
    id = request.args.get('id')
    print(id)
    data = Tovar.query.get(id)
    print(data)
    return render_template('tovar_page.html', data=data)


@app.route('/tovar_new_name/<tovar_id>/<new_name>', methods=['GET', 'POST'])
def name_tovar(tovar_id: int, new_name: str):
    data = Tovar.query.get(tovar_id)
    data.name = new_name
    db.session.commit()
    return redirect(url_for('index'))


# @app.route('/upload', methods=['POST'])
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']  # загрузка файла для дальнейшей обработки
#         file.save(os.path.join('app/static', file.filename))  # сохранение
#
#         return redirect(request.referrer)


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(port=5001, debug=True)
