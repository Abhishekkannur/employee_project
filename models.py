from database import Base
from sqlalchemy import Column, Integer,String,LargeBinary,Date,ForeignKey,DateTime
from pydantic import *
from fastapi import *
app=FastAPI
import regex
from database import SessionLocal
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
db=SessionLocal()

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
class Register(Base):
    __tablename__ = "user_register"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    
    

    
class Employeedb(Base):
    
    def last_emp_id():
        last=db.query(Employeedb).count()
        if last==None:
            result=last+1
            return f'I{result}'
        elif last==last:
            result=last+1
            return f'I{result}'
        elif last!=None:
            result=last+1
            return f'I{result}'
    __tablename__='employee_table'

    id = Column(Integer,primary_key=True, index= True)
    firstname=Column(String)
    lastname=Column(String)
    email=Column(String,unique=True)
    emp_id=Column(String,default=last_emp_id)
    user_id=Column(Integer,ForeignKey("user_register.id"))
    
class Employee_Profile(Base):
    __tablename__='emp_profile_table'

    id= Column(Integer, primary_key=True, index=True)
    date_of_birth = Column(Date)
    address=Column(String)
    country=Column(String)
    Intrests=Column(String)
    
    employee_id=Column(Integer,ForeignKey("employee_table.id"))
    
class EmployeeRequest(BaseModel):
    
    firstname : constr(min_length=3,max_length=70)
    @validator('firstname')
    def validate_firstname(cls, value):
        if not value.replace(' ', '').isalpha():
            raise ValueError("First name must contain only alphabetic characters and spaces.")
        return value.strip()
    lastname : str = Field ( max_length=150)
    @validator('lastname')
    def validate_lastname(cls, value):
        if not value.replace(' ', '').isalpha():
            raise ValueError("last name must contain only alphabetic characters and spaces.")
        return value.strip()
    email: EmailStr = Field ( max_length=150)
    user_id: int = Field(gt=0)
    
    #r'^\+?91[1-9]\d{9}$'
    class config:
        json_schema_extra = {
            'example':{
                "firstname": "first name of the employee",
                "lastname":"lastname of employee",
                "email":"enter the email id",
            }
        }

class EmployeeProfileCreate(BaseModel):
    date_of_birth: str
    address: str
    country: str
    Intrests: str
    @validator('date_of_birth')
    def validate_date_of_birth(cls, value):
        if not value:
            raise ValueError("Invalid date format for date_of_birth. It should be YYYY-MM-DD.")
        return value

class Employee_profile_data(Base):
    __tablename__='profile_data_table'
    id = Column(Integer,primary_key=True, index= True)
    profile_pic=Column(LargeBinary)
    resume=Column(LargeBinary)
    profile_id=Column(Integer,ForeignKey("emp_profile_table.id"))
    



  
    