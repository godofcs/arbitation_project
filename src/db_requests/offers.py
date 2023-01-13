import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Offer(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'offers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    market = sqlalchemy.Column(sqlalchemy.String(7))
    payment = sqlalchemy.Column(sqlalchemy.String(14))
    sell_buy = sqlalchemy.Column(sqlalchemy.Boolean)
    init_coin = sqlalchemy.Column(sqlalchemy.String(5))
    receive_coin = sqlalchemy.Column(sqlalchemy.String(5))
    id_limit = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Float)
    maker_commission = sqlalchemy.Column(sqlalchemy.Float)
    taker_commission = sqlalchemy.Column(sqlalchemy.Float)

