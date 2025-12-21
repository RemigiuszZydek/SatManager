from fastapi import FastAPI, status, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session 

app = FastAPI()

@app.get("/")
def root():
    return{"Hello": "World"}