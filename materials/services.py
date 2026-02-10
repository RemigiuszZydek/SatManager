from sqlalchemy.orm import Session
from .models import Material
from .schemas import MaterialCreate
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