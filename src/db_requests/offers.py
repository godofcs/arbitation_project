import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from src.db_requests.db_session import SqlAlchemyBase


class Offer(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'offer'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    market = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    payment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sell_buy = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    init_coin = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    receive_coin = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_limit = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.DECIMAL, nullable=True)
    maker_commission = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    taker_commission = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    last_time_update = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    def __init__(self, init_coin: str, receive_coin: str, price: float, market: str):
        self.init_coin = init_coin
        self.receive_coin = receive_coin
        self.price = price
        self.market = market
