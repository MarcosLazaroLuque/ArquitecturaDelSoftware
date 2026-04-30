from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Coche
from database import engine
from database import Base
from dependencies import get_db
from pydantic import BaseModel

app = FastAPI()

class CocheCreate(BaseModel):
    marca: str
    modelo: str
    matricula: str

class CocheResponse(CocheCreate):
    id: int

    class Config:
        orm_mode = True

@app.get("/coches/{coche_id}", response_model=CocheResponse)
async def get_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return coche

@app.post("/coches/", response_model=CocheResponse)
async def create_coche(coche: CocheCreate, db: AsyncSession = Depends(get_db)):
    db_coche = Coche(**coche.dict())
    db.add(db_coche)
    await db.commit()
    await db.refresh(db_coche)
    return db_coche

@app.put("/coches/{coche_id}", response_model=CocheResponse)
async def update_coche(coche_id: int, coche: CocheCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    db_coche = result.scalar_one_or_none()
    if not db_coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    for key, value in coche.dict().items():
        setattr(db_coche, key, value)
    await db.commit()
    await db.refresh(db_coche)
    return db_coche


@app.delete("/coches/{coche_id}")
async def delete_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    await db.delete(coche)
    await db.commit()
    return {"mensaje": "Coche eliminado"}
