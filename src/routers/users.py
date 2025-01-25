from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from starlette import status
import os
from ..models import Profiles
from ..database import SessionLocal
from fastapi.templating import Jinja2Templates

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

router = APIRouter(prefix="/profiles", tags=["profiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class ProfileRequest(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    age: int = Field(gt=18)
    height: int = Field(gt=0)
    weight: int = Field(gt=0)
    hair_color: str = Field(min_length=1)
    bust: int = Field(gt=0)
    waist: int = Field(gt=0)
    hips: int = Field(gt=0)

### Pages ###
@router.get("/profile-page")
async def render_profile_page(request: Request, db: db_dependency):
    profiles = db.query(Profiles).all()
    return templates.TemplateResponse(
        "profile.html", {"request": request, "profiles": profiles}
    )

@router.get("/add-profile-page")
async def render_add_profile_page(request: Request):
    return templates.TemplateResponse(
        "add-profile.html", {"request": request}
    )

@router.get("/edit-profile-page/{profile_id}")
async def render_edit_profile_page(request: Request, profile_id: int, db: db_dependency):
    profile = db.query(Profiles).filter(Profiles.id == profile_id).first()
    return templates.TemplateResponse(
        "edit-profile.html", {"request": request, "profile": profile}
    )

### Endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Profiles).all()

@router.get("/profile/{profile_id}", status_code=status.HTTP_200_OK)
async def read_profile(db: db_dependency, profile_id: int = Path(gt=0)):
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is not None:
        return profile_model
    raise HTTPException(status_code=404, detail="Profile not found.")

@router.post("/profile", status_code=status.HTTP_201_CREATED)
async def create_profile(db: db_dependency, profile_request: ProfileRequest):
    profile_model = Profiles(**profile_request.model_dump())
    db.add(profile_model)
    db.commit()

@router.put("/profile/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(
    db: db_dependency,
    profile_request: ProfileRequest,
    profile_id: int = Path(gt=0),
):
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is None:
        raise HTTPException(status_code=404, detail="Profile not found.")

    profile_model.name = profile_request.name
    profile_model.description = profile_request.description
    profile_model.age = profile_request.age
    profile_model.height = profile_request.height
    profile_model.weight = profile_request.weight
    profile_model.hair_color = profile_request.hair_color
    profile_model.bust = profile_request.bust
    profile_model.waist = profile_request.waist
    profile_model.hips = profile_request.hips

    db.add(profile_model)
    db.commit()

@router.delete("/profile/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(db: db_dependency, profile_id: int = Path(gt=0)):
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is None:
        raise HTTPException(status_code=404, detail="Profile not found.")
    db.query(Profiles).filter(Profiles.id == profile_id).delete()
    db.commit()






