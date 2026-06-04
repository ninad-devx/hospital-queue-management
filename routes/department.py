from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.department import department
from models.token import Token

from schemas.department import departmentcreate

router=APIRouter()


@router.post('/department')
def create_department(department_data:departmentcreate,db:Session=Depends(get_db)):
    new_department=department(name=department_data.name)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return{"message":"department created"}

@router.get("/departments")
def get_department(db:Session=Depends(get_db)):
    departments=db.query(department).all()
    return departments

@router.get("/department/{department_id}/tokens")
def department_tokens(department_id:int,db:Session=Depends(get_db)):
    departments=db.query(department).filter(department.id==department_id).first()
    return departments.tokens

@router.get("/department/{department_id}/stats")
def department_stats(department_id:int,db:Session=Depends(get_db)):
    departments=db.query(department).filter(department.id==department_id).first()
    if not departments:
        return{"message":"department not found"}
    
    total_token=db.query(Token).filter(Token.department_id==department_id).count()


    waiting=db.query(Token).filter(Token.department_id==department_id,Token.status=="waiting").count()


    serving=db.query(Token).filter(Token.department_id==department_id,Token.status=="serving").count()

    completed = db.query(Token).filter(
    Token.department_id == department_id,
    Token.status == "completed").count()

    return {
    "department": departments.name,
    "total_token": total_token,
    "waiting": waiting,
    "serving": serving,
    "completed": completed}


@router.delete("/department/{department_id}/reset")
def reset_department_queue(department_id:int,db:Session=Depends(get_db)):
    departments=db.query(department).filter(department.id==department_id).first()

    if not departments:
        return{
            "message":"department not found"
        }
    
    tokens=db.query(Token).filter(Token.department_id==department_id).all()

    for token in tokens:
        db.delete(token)
        db.commit()
        return {
    "message":"Queue reset successfully"
}

