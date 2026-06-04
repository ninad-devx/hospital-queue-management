from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

user="root"
password="12345678"
host="localhost"
port="3306"
database="hospital"

DATABASE_URL=f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
engine=create_engine(DATABASE_URL)

sessionlocal=sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

base=declarative_base()

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()