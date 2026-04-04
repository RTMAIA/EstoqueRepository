from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from model.model import Base
import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

folder_data = os.path.join(BASE_DIR, 'data')
os.makedirs(folder_data, exist_ok=True)

DATABASE_URL = f'sqlite:///{os.path.join(folder_data, "gestao_de_estoque.db")}'


engine = create_engine(DATABASE_URL, echo=True)

if not os.path.exists('gestao_de_estoque.db'):
    Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)

def get_session():
    Session = session
    try:
        yield Session()
    finally:
        Session.close_all()
        

