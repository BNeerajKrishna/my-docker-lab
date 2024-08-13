from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

# In-memory anime database
animes_db = {}

class Anime(BaseModel):
    title: str
    release_year: int
    genre: str
    seasons: int
    episodes: int

class AnimeWithID(Anime):
    id: str

@app.get("/animes", response_model=List[AnimeWithID])
def get_animes():
    return [AnimeWithID(id=anime_id, **anime.dict()) for anime_id, anime in animes_db.items()]

@app.post("/animes", response_model=AnimeWithID)
def add_anime(anime: Anime):
    anime_id = str(uuid4())
    animes_db[anime_id] = anime
    return AnimeWithID(id=anime_id, **anime.dict())

@app.get("/animes/{anime_id}", response_model=AnimeWithID)
def get_anime(anime_id: str):
    anime = animes_db.get(anime_id)
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return AnimeWithID(id=anime_id, **anime.dict())

@app.put("/animes/{anime_id}", response_model=AnimeWithID)
def update_anime(anime_id: str, anime: Anime):
    if anime_id not in animes_db:
        raise HTTPException(status_code=404, detail="Anime not found")
    animes_db[anime_id] = anime
    return AnimeWithID(id=anime_id, **anime.dict())

@app.delete("/animes/{anime_id}")
def delete_anime(anime_id: str):
    if anime_id not in animes_db:
        raise HTTPException(status_code=404, detail="Anime not found")
    del animes_db[anime_id]
    return {"detail": "Anime deleted"}
