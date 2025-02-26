from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, func

from src.models.podcast import Podcast
from src.data.db import init_db, get_session


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.get("/podcasts", response_model=list[Podcast])
def lista_podcasts(session: SessionDep):
    podcasts = session.exec(select(Podcast)).all()
    return podcasts


@app.delete("/podcasts/{nombre}")
def borrar_serie(nombre: str, session: SessionDep):
    podcast_encontrado = session.get(Podcast, nombre)
    if not podcast_encontrado:
        raise HTTPException(status_code=404, detail="Podcast no encontrado")
    session.delete(podcast_encontrado)
    session.commit()
    return {"mensaje": "Podcast eliminado"}


@app.get("/podcasts/{nombre}", response_model=Podcast)
def buscar_podcast(nombre: str, session: SessionDep):
    podcast_encontrado = session.get(Podcast, nombre)
    if not podcast_encontrado:
        raise HTTPException(status_code=404, detail="Podcast no encontrado")
    return podcast_encontrado



@app.patch("/podcasts/{nombre}", response_model=Podcast)
def actualiza_podcast(nombre: str, podcast: Podcast, session: SessionDep):
    podcast_encontrado = session.get(Podcast, nombre)
    if not podcast_encontrado:
        raise HTTPException(status_code=404, detail="podcast no encontrado")
    podcast_data = podcast.model_dump(exclude_unset=True)
    podcast_encontrado.sqlmodel_update(podcast_data)
    session.add(podcast_encontrado)
    session.commit()
    session.refresh(podcast_encontrado)
    return podcast_encontrado

