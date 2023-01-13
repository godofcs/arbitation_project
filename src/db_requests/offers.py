import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_requests.db_session import SqlAlchemyBase


class Offer(SqlAlchemyBase, SerializerMixin):  # Это класс, описывающий таблицу в бд
    __tablename__ = 'offers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    market = sqlalchemy.Column(sqlalchemy.Text)
    payment = sqlalchemy.Column(sqlalchemy.Text)
    sell_buy = sqlalchemy.Column(sqlalchemy.Integer)
    init_coin = sqlalchemy.Column(sqlalchemy.Text)
    receive_coin = sqlalchemy.Column(sqlalchemy.Text)
    id_limit = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Float)
    maker_commission = sqlalchemy.Column(sqlalchemy.Float)
    taker_commission = sqlalchemy.Column(sqlalchemy.Float)

