import requests
from fastapi import FastAPI, Path, Request, status, Query
from fastapi.responses import JSONResponse
from typing import Optional, Any, List

from app import schemas
from pymongo import errors
from bootstrap import mongodb

app = FastAPI()
mongodb.install(app)

class CepNotFoundException(Exception):
  pass

async def save_address(address: dict):
  app.db.insert_one(address)

@app.exception_handler(CepNotFoundException)
async def cep_not_found_handler(request: Request, exc: CepNotFoundException):
  return JSONResponse(status_code=404, content={"message": "CEP not found"})

@app.get("/address", response_model=List[schemas.AddressOutput])
async def search_address(uf: Optional[str] = Query(None, max_length=2, min_length=2)):
  print("asd")
  if uf:
    return list(app.db.find({"uf": uf}))

  return list(app.db.find({}))

@app.get("/address/{cep}", response_model=schemas.AddressOutput)
async def search_address_by_cep(cep: str = Path(default=Any, max_length=9, min_length=9)):
  address = app.db.find_one({"cep": cep})

  if not address:
    response = requests.get(f"http://viacep.com.br/ws/{cep}/json/")
    address = response.json()

    if "erro" in address:
      raise CepNotFoundException()

    await save_address(address)

  return address

@app.post("/address", response_model=schemas.AddressOutput, status_code=201)
async def create_address(address: schemas.AddressInput):
  try:
    await save_address(address.dict()) 
    return address
  except errors.DuplicateKeyError:
    return JSONResponse(status_code=409, content={"message": "CEP has already exists"})

@app.put("/address/{cep}", response_model=schemas.AddressOutput, status_code=status.HTTP_200_OK)
async def update_address(cep: str, address: schemas.AddressInput):
  old_address = app.db.find_one({"cep": cep})
  update_address = {"$set": address.dict()}

  app.db.update_one(old_address, update_address)

  updated_address = app.db.find_one({"cep": cep})

  return updated_address