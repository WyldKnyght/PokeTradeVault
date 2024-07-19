from fastapi import APIRouter
from ..extensions import nlp

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to PokéDealFinder Chat!"}

@router.post("/")
async def chat(message: str):
    doc = nlp(message)
    # Basic NLP processing, to be expanded later
    return {"response": f"Received: {message}"}