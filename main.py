from fastapi import *
import models
from database import *
from typing import *
from sqlalchemy.orm import Session
from models import *
from routers import auth , employees

app=FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router (employees.router)
