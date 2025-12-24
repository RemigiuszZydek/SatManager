from fastapi import APIRouter, Depends
from .dependencies import require_roles, get_current_user

router = APIRouter(
    prefix="/test-role",
    tags=['test_role']
    )

@router.get("/admin-data")
async def admin_data(user: dict= Depends(require_roles(["ADMIN"]))):
    return {"msg":"Tylko dla admina"}

@router.get("/koordynator-data")
async def koordynator_data(user: dict= Depends(require_roles(["ADMIN","KOORDYNATOR"]))):
    return {"msg":"Admin i Koordynator"}

@router.get("/general-data")
async def general_data(user: dict= Depends(get_current_user)):
    return {"msg":"Wszyscy to widza"}
