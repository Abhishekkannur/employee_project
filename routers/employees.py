from fastapi import FastAPI, APIRouter, Depends,UploadFile, File
from pydantic import BaseModel, Field
from database import SessionLocal
from datetime import datetime,timedelta
import models
from cryptography.fernet import Fernet
from models import Register
from passlib.context import CryptContext
from typing import *
from sqlalchemy.orm import Session
from models import *
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt,JWTError
from .auth import get_current_user
router = APIRouter()

def get_db():
        db=SessionLocal()
        try:
                yield db
        finally:
                db.close()
db_dependecy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/get_employee", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependecy):
        return db.query(Employeedb).all()

@router.get("/get_employee_by_id/{emp_id}", status_code=status.HTTP_200_OK)
async def get_emp_by_id(user: user_dependency,db:db_dependecy, emp_id: int = Path(gt=0)):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        emp_data=db.query(Employeedb).filter(Employeedb.id == emp_id ).first()
        if emp_data is not None:
                return emp_data
        
        raise HTTPException (status_code=400, detail="Employee not found")


@router.post("/employee/create_employee",status_code=status.HTTP_201_CREATED,response_model=EmployeeRequest)
async def create_employee(user: user_dependency,db:db_dependecy, employee_data: EmployeeRequest):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        new_employee=Employeedb(**employee_data.dict())
        db.add(new_employee)
        db.commit()
        return new_employee

@router.put("/employee/update_employee/{emp_id}",status_code=status.HTTP_200_OK,response_model=EmployeeRequest)
async def update_employee(user: user_dependency,db:db_dependecy, employeerequest: EmployeeRequest,emp_id:int=Path(gt=0)):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        employee_update=db.query(Employeedb).filter(Employeedb.id==emp_id).first()
        if employee_update is None:
                raise HTTPException(status_code=404, detail="No employee found on this id to update")
        employee_update.firstname=employeerequest.firstname
        employee_update.lastname=employeerequest.lastname
        employee_update.email=employeerequest.email
        db.add(employee_update)
        db.commit()
        return employee_update
        
@router.delete("/employee/delete_employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependecy, employee_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    employee_model = db.query(Employeedb).filter(Employeedb.id == employee_id)\
        .filter(Employeedb.user_id == user.get('id')).first()
    if employee_model is None:
        raise HTTPException(status_code=404, detail='Employee not found.')
    db.query(Employeedb).filter(Employeedb.id == employee_id).filter(Employeedb.user_id == user.get('id')).delete()
    db.commit()
@router.get("/get_employee", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependecy):
        return db.query(Employee_Profile).all()

@router.post("/employee/create_profile/{employee_id}",status_code=status.HTTP_201_CREATED)
async def create_employee_profile(profile_request: EmployeeProfileCreate,
    user:user_dependency,
    employee_id: int,
    db: Session = Depends(get_db),
    
):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    employee = db.query(models.Employeedb).filter(models.Employeedb.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee ID not found in the database")
    new_profile = models.Employee_Profile(**profile_request.dict(), employee_id=employee.id)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.get("/get_employee_profile_by_id/{emp_profile_id}", status_code=status.HTTP_200_OK)
async def get_emp_profile_by_id(user: user_dependency,db:db_dependecy, emp_profile_id: int = Path(gt=0)):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        emp_data=db.query(Employee_Profile).filter(Employee_Profile.id == emp_profile_id ).first()
        if emp_data is not None:
                return emp_data
        raise HTTPException (status_code=400, detail="Employee not found")
      
@router.put("/employee/update_employee_profile/{emp_profile_id}",status_code=status.HTTP_200_OK)
async def update_employee_profile(user: user_dependency,db:db_dependecy, employeerequest: EmployeeProfileCreate,emp_profile_id:int=Path(gt=0)):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        employee_profile_update=db.query(Employee_Profile).filter(Employee_Profile.id==emp_profile_id).first()
        if employee_profile_update is None:
                raise HTTPException(status_code=404, detail="No employee found on this id to update")
        
        employee_profile_update.date_of_birth=employeerequest.date_of_birth
        
        employee_profile_update.address=employeerequest.address
        employee_profile_update.country=employeerequest.country
        employee_profile_update.Intrests=employeerequest.Intrests
        db.add(employee_profile_update)
        db.commit()
        return employee_profile_update
@router.delete("/employee/delete_employee_profile/{employee_profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_profile(user: user_dependency, db: db_dependecy, emp_profile_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    employee_profile_model = db.query(Employee_Profile).filter(Employee_Profile.id == emp_profile_id)\
        .filter(Employee_Profile.user_id == user.get('id')).first()
    if employee_profile_model is None:
        raise HTTPException(status_code=404, detail='employee profile not found.')
    db.query(Employee_Profile).filter(Employee_Profile.id == emp_profile_id).filter(Employee_Profile.user_id == user.get('id')).delete()

    db.commit()

@router.post("/create_profile_data/",status_code=status.HTTP_201_CREATED)
async def create_profile_data(
    profile_pic: UploadFile,
    resume: UploadFile,
    profile_id: int,
    db: db_dependecy,
):
    
    profile_pic_content = profile_pic.file.read()
    resume_content = resume.file.read()

    
    profile_data = Employee_profile_data(
        profile_pic=profile_pic_content,
        resume=resume_content,
        profile_id=profile_id,
    )
    db.add(profile_data)
    db.commit()
    db.refresh(profile_data)
    return profile_data

    