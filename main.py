from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from db import create_db_and_tables, get_session
from models import Hero

app = FastAPI()

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
def read_heroes(session=Depends(get_session)):
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
