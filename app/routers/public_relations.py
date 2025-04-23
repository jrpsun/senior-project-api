from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import public_relations as crud
from app.schemas.public_relations import (
    PublicRelationsCreate,
    PublicRelationsResponse,
    PublicRelationsUpdate
)

router = APIRouter()

# 🔹 Create (POST)
@router.post("/", response_model=PublicRelationsResponse)
def create_pr(pr_data: PublicRelationsCreate, db: Session = Depends(get_db)):
    return crud.create_public_relation(db, pr_data)

# 🔹 Read All (GET)
@router.get("/get-all-pr", response_model=list[PublicRelationsResponse])
def read_prs(db: Session = Depends(get_db)):
    return crud.get_public_relations(db)

# 🔹 Read One (GET by ID)
@router.get("/get-pr/{pr_id}", response_model=PublicRelationsResponse)
def read_pr(pr_id: str, db: Session = Depends(get_db)):
    pr = crud.get_public_relation_by_id(db, pr_id)
    if not pr:
        raise HTTPException(status_code=404, detail="PublicRelations not found")
    return pr

# 🔹 Update (PUT)
@router.put("/update-pr/{pr_id}", response_model=PublicRelationsResponse)
def update_pr(pr_id: str, pr_data: PublicRelationsUpdate, db: Session = Depends(get_db)):
    pr = crud.update_public_relation(db, pr_id, pr_data)
    if not pr:
        raise HTTPException(status_code=404, detail="PublicRelations not found")
    return pr

# 🔹 Delete (DELETE)
@router.delete("/delete-pr/{pr_id}")
def delete_pr(pr_id: str, db: Session = Depends(get_db)):
    pr = crud.delete_public_relation(db, pr_id)
    if not pr:
        raise HTTPException(status_code=404, detail="PublicRelations not found")
    return {"message": "Deleted successfully"}
