from flask import Flask, render_template, flash, redirect, url_for, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import Config
from forms import LoginForm, TovarForm
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from myapp.models import Product
import uuid
import os


app = Flask(__name__, static_folder='static', template_folder='templates')
login_manager = LoginManager(app)

app.config.from_object(Config)
# Добавляем путь сохранения изображения
# Это так же можно сделать (и правильно сделать) в классе конфиг
app.config['UPLOAD_FOLDER'] = '/app/static'



db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import User, Tovar, load_user

korzina = []

with app.app_context():
    db.create_all()
    have_user = User.query.first()
    # print(have_user)
    if not have_user:
        from seed import seeds

        seeds()

from faker import Faker
import random

fake = Faker('ru_RU')

# Генерация категорий
categories = ['Одежда', 'Обувь', 'Для дома']
products = []

# Генерация товаров
for _ in range(300):
    product = {
        'name': fake.catch_phrase(),  # Название товара
        'category': random.choice(categories),  # Случайная категория
        'price': round(random.uniform(100, 5000), 2),  # Случайная цена
        'description': fake.text(max_nb_chars=200)  # Описание товара
    }
    products.append(product)

# Генерация пользователей
users = []
for _ in range(100):
    user = {
        'username': fake.user_name(),
        'email': fake.email(),
        'full_name': fake.name(),
        'address': fake.address(),
        'phone_number': fake.phone_number()
    }
    users.append(user)

print(products)
print(users)


@app.route('/')
@app.route('/index')
def index():
    global korzina
    tovar = Tovar.query.all()
    kolvo = len(korzina)

    return render_template('index.html', tovars=tovar, korzina=kolvo)


@app.route('/user_data', methods=['GET', 'POST'])
def user_data():
    if current_user.is_authenticated:
        return render_template('user_data.html', user=current_user)
    else:
        return redirect(url_for('not_found_error'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        print('*' * 20)
        print(user)
        if user is None or not user.check_password(form.pasword.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('index'))
    return render_template('login_enter.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
@login_required
def tovar_add():
    flash(current_user.name)
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
    global korzina
    data = Tovar.query.get(id)
    korzina.append(data)
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


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(400)
def error_400(error):
    return render_template('400.html'), 400


@app.errorhandler(401)
def error_401(error):
    return render_template('401.html'), 401


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)
