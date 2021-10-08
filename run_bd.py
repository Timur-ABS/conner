import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    tg_id = sqlalchemy.Column(sqlalchemy.String,
                              primary_key=True)
    role = sqlalchemy.Column(sqlalchemy.String)
    cit = sqlalchemy.Column(sqlalchemy.String)
    pr_cit = sqlalchemy.Column(sqlalchemy.String)

class Run(SqlAlchemyBase):
    __tablename__ = 'run'

    num = sqlalchemy.Column(sqlalchemy.String,
                            primary_key=True)
    photo = sqlalchemy.Column(sqlalchemy.String)
    # date_run = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    place = sqlalchemy.Column(sqlalchemy.String)
    pace = sqlalchemy.Column(sqlalchemy.String)
    distance = sqlalchemy.Column(sqlalchemy.String)
    partner = sqlalchemy.Column(sqlalchemy.String)

# session = create_session()