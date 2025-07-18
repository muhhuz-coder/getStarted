from fastapi import FastAPI, Depends, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlmodel import select
from db import create_db_and_tables, get_session
from models import Hero

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter    
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session=Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes/", response_model=list[Hero])
@limiter.limit("2/minute")
def read_heroes(request:Request,session=Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes

@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session=Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero: Hero, session=Depends(get_session)):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    for key, value in hero.dict(exclude_unset=True).items():
        setattr(db_hero, key, value)

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.delete("/heroes/{hero_id}", response_model=Hero)
def delete_hero(hero_id: int, session=Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    session.delete(hero)
    session.commit()
    return hero
