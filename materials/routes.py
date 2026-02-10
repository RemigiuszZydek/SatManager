from fastapi import APIRouter, status,UploadFile,Depends,File
from sqlalchemy.orm import Session
import csv
from ..database.database import get_db
from .models import Material
from .schemas import MaterialRead,MaterialCreate,MaterialUpdate
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

@router.patch("/{material_id}", response_model=MaterialRead)
def update_material_endpoint(material_id:int, data: MaterialUpdate, db: Session = Depends(get_db),current_user = Depends(require_roles(["ADMIN"]))):
    services.update_material(db,material_id,data)                       
    
@router.delete("/{material_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_material_endpoint(material_id:int, db: Session = Depends(get_db),current_user = Depends(require_roles(["ADMIN"]))):
    services.delete_material(db,material_id)