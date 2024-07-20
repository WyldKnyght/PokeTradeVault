from fastapi import APIRouter
from pydantic import BaseModel
from src.nlp.load_model import load_model, process_text

router = APIRouter()
nlp = load_model()

class Message(BaseModel):
    message: str

@router.get("/chat")
async def root():
    return {"message": "Welcome to PokéDealFinder Chat!"}

@router.post("/chat")
async def chat(message: Message):
    result = process_text(nlp, message.message)
    response = {
        "original_message": message.message,
        "entities": result["entities"]
    }
    return {"response": response}