import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_requests.db_session import SqlAlchemyBase


class Offer(SqlAlchemyBase, SerializerMixin):  # Это класс, описывающий таблицу в бд
    """
    Класс, описывающий схему таблицы в нашей БД. 
    id - primary key
    market - имя криптобиржи
    payment - банк, через который мы олпачиваем/принимаем платеж перевода "Фиат" -> "Крипта" и наоборот
    sell_buy - флаг показывающий через какую вкладку нам покупать. В вкладке sell, то sell_buy == 0, во вкладке buy, то sell_buy == 1
    init_coin - имя валюты/крипты, которую мы отдаем
    receive_coin - имя валюты/крипты, которую мы принимаем
    id_limit - айди, обозначающий уровень ставки пользователя
    price - курс обмена
    maker_commission - коммисия, если мы продаем как мейкер. В случае maker_commission == 100, то как мейкер мы продать не можем
    taker_commission - коммисия, если мы продаем как тейкер. В случае taker_commission == 100, то как тейкер мы продать не можем
    """
    __tablename__ = 'offers'
    __table_args__ = {'extend_existing': True}

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

