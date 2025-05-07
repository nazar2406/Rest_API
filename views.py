from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from marshmallow import ValidationError

from .models import library
from .schemas import LibraryItemSchema

router = APIRouter()
schema = LibraryItemSchema()

@router.get("/library")
async def fetch_all_items():
    return JSONResponse(content=library)

@router.get("/library/{uid}")
async def fetch_item(uid: int):
    for item in library:
        if item["uid"] == uid:
            return JSONResponse(content=item)
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/library")
async def create_item(request: Request):
    data = await request.json()
    try:
        validated = schema.load(data)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.messages)

    for item in library:
        if item["uid"] == validated["uid"]:
            raise HTTPException(status_code=400, detail="Item with this UID already exists")

    library.append(validated)
    return JSONResponse(content=validated, status_code=201)

@router.delete("/library/{uid}")
async def delete_item(uid: int):
    for item in library:
        if item["uid"] == uid:
            library.remove(item)
            return JSONResponse(content={"message": "Item deleted"})
    raise HTTPException(status_code=404, detail="Item not found")
