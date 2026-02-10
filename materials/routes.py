from fastapi import APIRouter, status,UploadFile,Depends,File
from sqlalchemy.orm import Session
import csv
from ..database.database import get_db
from .models import Material
from .schemas import MaterialRead,MaterialCreate
from ..auth.dependencies import require_roles
from . import services

router = APIRouter(prefix="/materials", tags=["materials"])

@router.post("",response_model = MaterialRead,status_code=status.HTTP_201_CREATED)
def create_material_endpoint(data: MaterialCreate, db:Session = Depends(get_db), current_user = Depends(require_roles(["ADMIN"]))):
    return services.create_material(db,data)

@router.post("/import")
def import_materials_endpoint(file: UploadFile = File(...), db:Session = Depends(get_db), current_user = Depends(require_roles(["ADMIN"]))):
    imported = services.import_materials_from_csv(db,file)
    return {"imported":imported}
    