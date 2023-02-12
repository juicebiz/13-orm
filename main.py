import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import join
from sqlalchemy.orm import sessionmaker, query
from models import create_tables, Publisher, Book, Shop, Stock, Sale

load_dotenv()
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
db = os.environ.get('DB')

DSN = f"postgresql://{user}:{password}@localhost:5432/{db}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='АСТ')
publisher2 = Publisher(name='Эксмо')
session.add_all([publisher1, publisher2])
session.commit()

book1 = Book(title='Капитанская дочка', publisher=publisher1)
book2 = Book(title='Руслан и Людмила', publisher=publisher2)
book3 = Book(title='Евгений Онегин', publisher=publisher1)
session.add_all([book1, book2, book3])
session.commit()

shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')
session.add_all([shop1, shop2, shop3])
session.commit()

stock1 = Stock(book=book1, shop=shop1, count=9)
stock2 = Stock(book=book2, shop=shop2, count=8)
stock3 = Stock(book=book3, shop=shop3, count=7)
session.add_all([stock1, stock2, stock3])
session.commit()

sale1 = Sale(price=111, date_sale='2023-02-08', stock=stock1, count=1)
sale2 = Sale(price=222, date_sale='2023-02-09', stock=stock2, count=1)
sale3 = Sale(price=333, date_sale='2023-02-10', stock=stock3, count=1)
sale4 = Sale(price=444, date_sale='2023-02-11', stock=stock1, count=1)
sale5 = Sale(price=555, date_sale='2023-02-12', stock=stock2, count=1)
session.add_all([sale1, sale2, sale3, sale4, sale5])
session.commit()

pub_name = input('Название издательства: ')
pub_id = input('Идентификатор издательства: ')

def get_sales(publisher_name='', publisher_id=''):
    if(publisher_name != ''):
        q = session.query(Publisher).filter(Publisher.name == publisher_name).one()
        publisher_id = q.id

    records = session.query(
        Publisher, Book, Stock, Shop, Sale
    ).filter(
        Publisher.id == publisher_id,
    ).filter(
        Publisher.id == Book.id_publisher,
    ).filter(
        Stock.id_book == Book.id,
    ).filter(
        Shop.id == Stock.id_shop,
    ).filter(
        Sale.id_stock == Stock.id,
    ).filter(
        Publisher.id == publisher_id,
    ).all()

    for publisher, book, stock, shop, sale in records:
        print(book.title, shop.name, sale.price, sale.date_sale, sep = '|')

if __name__ == '__main__':
    get_sales(pub_name, pub_id)

session.close()