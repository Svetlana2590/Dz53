from models import User, Tovar
from main import db


def seeds():
    data = User(name="Vasiliy", is_active=True)
    data.set_password('111')
    data2 = User(name="Evgeniy", is_active=True)
    data2.set_password('111')
    data3 = User(name="Nikolay",  is_active=True)
    data3.set_password('111')

    data4 = Tovar(name="Костюм", price=50, ostatok=20, url_photo="111.jpg")
    data5 = Tovar(name="Брюки", price=150, ostatok=14, url_photo="111.jpg")
    data6 = Tovar(name="Рубашка", price=250, ostatok=10, url_photo="111.jpg")

    db.session.add(data)
    db.session.add(data2)
    db.session.add(data3)
    db.session.commit()

    db.session.add(data4)
    db.session.add(data5)
    db.session.add(data6)
    db.session.commit()

