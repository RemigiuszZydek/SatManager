from sqlalchemy.orm import Session, joinedload
from .models import Material
from .schemas import MaterialCreate, MaterialUpdate
from fastapi import HTTPException, UploadFile
import csv

def create_material(db: Session, material_data: MaterialCreate):
    """
    Tworzy nowy materiał w bazie (słownik materiałów).
    """

    exists = db.query(Material).filter(Material.name == material_data.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Material already exists")
    
    material = Material(
        name=material_data.name,
        description=material_data.description,
        price=material_data.price,
    )

    db.add(material)
    db.commit()
    db.refresh(material)

    return material


def import_materials_from_csv(db:Session, file: UploadFile):
    """
    Importuje materiały z pliku CSV.
    """

    content = file.file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(content)

    imported = 0

    for row in reader:
        exists = db.query(Material).filter_by(name=row["name"]).first()
        if exists:
            continue

        material = Material(
            name=row["name"],
            description=row.get("description"),
            price=float(row["price"])
        )

        db.add(material)
        imported += 1

    db.commit()
    return imported

def update_material(db: Session, material_id: int, material_data: MaterialUpdate):
    """
    Edytuje istniejący materiał.
    """

    material = db.query(Material).get(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    if material_data.name and material_data.name != material.name:
        exists = db.query(Material).filter(Material.name == material_data.name).first()

        if exists:
            raise HTTPException(status_code=400, detail="Material with this name already exists")

    if material_data.name is not None:
        material.name = material_data.name

    if material_data.description is not None:
        material.description = material_data.description

    if material_data.price is not None:
        material.price = material_data.price

    db.commit()
    db.refresh(material)

    return material


def delete_material(db:Session, material_id: int):
    """
    Usuwa materiał, jeżeli nie był użyty w żadnym tasku.
    """

    material = (
        db.query(Material)
        .options(joinedload(Material.task_usages))
        .get(material_id)
    )

    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    if material.task_usages:
        raise HTTPException(
            status_code=400,
            detail="Material is used in tasks and cannot be deleted"
        )

    db.delete(material)
    db.commit()