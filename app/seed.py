from models import User, Tovar
from main import db


def seeds():
    data = User(name="Vasiliy", password="111", is_active=True)
    data2 = User(name="Evgeniy", password="111", is_active=True)
    data3 = User(name="Nikolay", password="111", is_active=True)

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

