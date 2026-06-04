from pydantic import BaseModel


class TokenCreate(BaseModel):

    patient_name: str

    department_id: int