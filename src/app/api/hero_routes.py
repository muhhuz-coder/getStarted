# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from ..models.hero import Hero
from ..db.database import get_session
from ..utils.rate_limiter import limiter
from sqlmodel import select

hero_router = APIRouter()

@hero_router.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session=Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@hero_router.get("/heroes/", response_model=list[Hero])
@limiter.limit("2/minute")
def read_heroes(request: Request, session=Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes

@hero_router.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session=Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero