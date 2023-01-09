import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    conn_str = f'mysql://root:9e6vmrmIGWZvQ6qylywn@containers-us-west-200.railway.app:7182/railway'
    print(f'Подключение к базе данных по адресу {conn_str}')

    engine = sa.create_engine(conn_str)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
