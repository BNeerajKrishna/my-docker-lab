from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from sqlalchemy.orm import Session
from database import SessionLocal, database, AnimeModel, init_db

app = FastAPI()

# Initialize the database
init_db()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Anime(BaseModel):
    title: str
    release_year: int
    genre: str
    seasons: int
    episodes: int

class AnimeWithID(Anime):
    id: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/animes", response_model=List[AnimeWithID])
async def get_animes():
    query = AnimeModel.__table__.select()
    result = await database.fetch_all(query)
    return [AnimeWithID(title=row["title"], release_year=row["release_year"], genre=row["genre"], seasons=row["seasons"], episodes=row["episodes"]) for row in result]

@app.post("/animes", response_model=AnimeWithID)
async def add_anime(anime: Anime):
    anime_id = str(uuid4())
    query = AnimeModel.__table__.insert().values(id=anime_id, **anime.dict())
    await database.execute(query)
    return AnimeWithID(id=anime_id, **anime.dict())

@app.get("/animes/{anime_id}", response_model=AnimeWithID)
async def get_anime(anime_id: str):
    query = AnimeModel.__table__.select().where(AnimeModel.id == anime_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return AnimeWithID(id=result["id"], title=result["title"], release_year=result["release_year"], genre=result["genre"], seasons=result["seasons"], episodes=result["episodes"])

@app.put("/animes/{anime_id}", response_model=AnimeWithID)
async def update_anime(anime_id: str, anime: Anime):
    query = AnimeModel.__table__.select().where(AnimeModel.id == anime_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    query = AnimeModel.__table__.update().where(AnimeModel.id == anime_id).values(**anime.dict())
    await database.execute(query)
    return AnimeWithID(id=anime_id, **anime.dict())

@app.delete("/animes/{anime_id}")
async def delete_anime(anime_id: str):
    query = AnimeModel.__table__.select().where(AnimeModel.id == anime_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    query = AnimeModel.__table__.delete().where(AnimeModel.id == anime_id)
    await database.execute(query)
    return {"detail": "Anime deleted"}
