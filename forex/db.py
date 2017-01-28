from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, String, Float, Integer
from sqlalchemy.orm import sessionmaker


eng = create_engine('mysql+mysqlconnector://root:root@localhost/forex_db')
Base = declarative_base()


class Forex(Base):
    __tablename__ = "forex"

    id = Column(Integer, primary_key=True)
    currency = Column(String(5))
    rate = Column(Float)
    time = Column(BIGINT)


# Create tables only when called
if __name__ == '__main__':
    Base.metadata.bind = eng
    Base.metadata.create_all()


def load_data(forex_list):
    session_gen = sessionmaker(bind=eng)
    session = session_gen()
    session.add_all(forex_list)
    session.commit()


def get_data(currency: str, start_time: int, end_time: int):
    session_gen = sessionmaker(bind=eng)
    session = session_gen()

    filters = {
        Forex.time > start_time,
        Forex.time < end_time,
    }

    if currency:
        filters.add(Forex.currency == currency)

    results = session.query(Forex).filter(*filters).all()
    results_useful = list(
        map(lambda x: dict(
            currency=x.currency,
            rate=x.rate,
            time=x.time
        ), results)
    )
    return results_useful
