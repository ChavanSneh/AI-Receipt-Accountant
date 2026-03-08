from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ledger.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class LedgerItem(Base):
    __tablename__ = "ledger"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)


def init_db():
    Base.metadata.create_all(bind=engine)


def add_item(item_id, name, price):
    session = SessionLocal()
    try:
        item = LedgerItem(id=item_id, name=name, price=price)
        session.add(item)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()


def get_all_items():
    session = SessionLocal()
    try:
        items = session.query(LedgerItem).all()
        return [
            {"id": i.id, "name": i.name, "price": i.price}
            for i in items
        ]
    finally:
        session.close()


def delete_item_by_id(item_id):
    session = SessionLocal()
    try:
        rows = session.query(LedgerItem).filter(
            LedgerItem.id == item_id
        ).delete()
        session.commit()
        return rows
    finally:
        session.close()


def clear_database():
    session = SessionLocal()
    try:
        session.query(LedgerItem).delete()
        session.commit()
    finally:
        session.close()