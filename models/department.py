from sqlalchemy import Column,Integer,String
from database.database import base
from sqlalchemy.orm import relationship

class department(base):
    __tablename__="departments"

    id=Column(Integer,primary_key=True)
    name=Column(String(100))
    tokens=relationship("Token",back_populates="department")
    







