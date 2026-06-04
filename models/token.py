from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey
)
from database.database import base
from sqlalchemy.orm import relationship

class Token(base):

    __tablename__ = "tokens"

    id = Column(
        Integer,
        primary_key=True
    )

    token_number = Column(
        String(20)
    )

    patient_name = Column(
        String(100)
    )

    status = Column(
        String(20),
        default="waiting"
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id")
    )
    department=relationship(
        "department",back_populates="tokens"
    )