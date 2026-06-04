from database.database import base
from database.database import engine

from models.department import department
from models.token import Token

base.metadata.create_all(bind=engine)

print("tables created")