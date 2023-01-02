import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Offer(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'offer'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    market = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    init_coin = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    receive_coin = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_limit = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.DECIMAL, nullable=True)
    maker_commission = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    taker_commission = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    las_time_update = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)