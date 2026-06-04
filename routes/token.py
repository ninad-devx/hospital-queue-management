from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.database import get_db

from models.token import Token
from models.department import department

from schemas.token import TokenCreate

router = APIRouter()

router=APIRouter()

@router.post("/tokens")
def create_token(token_data: TokenCreate, db: Session = Depends(get_db)):
    
    departments = db.query(department).filter(
        department.id == token_data.department_id
    ).first()

    if not departments:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )
    
    prefix = departments.name[0].upper()

    existing_tokens = db.query(Token).filter(
        Token.department_id ==
        token_data.department_id
    ).count()

    token_number = (
        f"{prefix}-{existing_tokens + 1}"
    )

    new_token = Token(
        token_number=token_number,
        patient_name=token_data.patient_name,
        department_id=token_data.department_id
    )
    db.add(new_token)

    db.commit()

    db.refresh(new_token)

    return {
        "message": "token created",
        "token": new_token.token_number,
        "patient": new_token.patient_name,
        "status": new_token.status
    }

@router.get("/queue/{department_id}")
def get_queue(
    department_id: int,
    db: Session = Depends(get_db)
):
    tokens = db.query(Token).filter(
        Token.department_id == department_id,
        Token.status == "waiting"
    ).all()

    return tokens


@router.put("/next/{department_id}")
def call_next_patient(department_id:int,db:Session=Depends(get_db)):
    current_serving = db.query(Token).filter(
    Token.department_id == department_id,
    Token.status == "serving").first()


    if current_serving:
     return {
        "message": "A patient is already being served",
        "token": current_serving.token_number
    }




    next_token=db.query(Token).filter(Token.department_id==department_id,Token.status=="waiting").first()

    if not next_token:
        return{
            "message":"NO PATIENT WAITING"
        }
    
    next_token.status="serving"

    db.commit()
    db.refresh(next_token)

    return {
    "message": "Now serving",
    "token": next_token.token_number,
    "patient": next_token.patient_name
}

@router.put("/complete/{token_id}")
def complete_patient(token_id:int,db:Session=Depends(get_db)):
    current_token=db.query(Token).filter(Token.id==token_id).first()
    if not current_token:
        return{
            "message":"token not found"
        }
    current_token.status="completed"
    db.commit()
    db.refresh(current_token)

    return {
    "message": "Patient completed",
    "token": current_token.token_number
}



@router.get("/serving/{department_id}")
def get_serving_patient(department_id:int,db:Session=Depends(get_db)):
    serving_patient=db.query(Token).filter(Token.department_id==department_id,Token.status=="serving").first()
    if not serving_patient:
        return{
            "message":"no patient being served"
        }
    return serving_patient



@router.get("/dashboard/{department_id}")
def dashboard(department_id:int,db:Session=Depends(get_db)):
    waiting=db.query(Token).filter(Token.department_id==department_id,Token.status=="waiting").count()
    serving=db.query(Token).filter(Token.department_id==department_id,Token.status=="serving").count()
    completed=db.query(Token).filter(Token.department_id==department_id,Token.status=="completed").count()
    return{
        "waiting":waiting,
        "serving":serving,
        "completed":completed
    }


@router.get("/wait-time/{token_id}")
def estimated_wait_time(token_id:int,db:Session=Depends(get_db)):
    current_token=db.query(Token).filter(Token.id==token_id).first()
    if not current_token:
        return{
            "message": f" {token_id} token not found"
        }
    people_ahead=db.query(Token).filter(Token.department_id==current_token.department_id,Token.id<current_token.id,Token.status.in_(["waiting","serving"])).count()
    avg_service_time=10

    estimated_time=(
        people_ahead*avg_service_time
    )

    return {
    "token": current_token.token_number,
    "people_ahead": people_ahead,
    "estimated_wait_minutes": estimated_time
}


@router.get("/token/{token_id}")
def token_details(
    token_id:int,
    db:Session=Depends(get_db)
):
    token = db.query(Token).filter(
    Token.id == token_id
).first()
    if not token:
     return {
        "message":"Token not found"
    }
    return {
    "token": token.token_number,
    "patient": token.patient_name,
    "status": token.status,
    "department": token.department.name
}


@router.get("/search-token/{token_number}")
def search_token(token_number:str,db:Session=Depends(get_db)):
    token=db.query(Token).filter(Token.token_number==token_number).first()

    if not token:
        return{
            "message":"token not found"
        }
    
    return {
    "token": token.token_number,
    "patient": token.patient_name,
    "status": token.status,
    "department": token.department.name
}