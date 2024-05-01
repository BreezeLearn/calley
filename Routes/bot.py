from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models.models import Bot
from pydantic import BaseModel
from Agent.langchain_agent import invoke_agent
from Agent.main import gemini_agent
from auth.auth_bearer import get_current_user
from typing import List


def generate_unique_id():
    import uuid
    return str(uuid.uuid4())


class Item(BaseModel):
    name: str
    description: str | None = None
    web_search: bool
    unique_id: str
    instruction: str
    tools: List[str]
    user_id: int


class InvokeBot(BaseModel):
    input: str
    unique_id: str



router = APIRouter()


@router.get("/bots")
def get_bots(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    bots = db.query(Bot).filter(Bot.user_id == current_user.id).all()
    return bots


@router.post("/bots")
def create_bot(item: Item, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        unique_id = generate_unique_id()
        bot_data = item.dict()
        bot_data["unique_id"] = unique_id
        bot_data["user_id"] = current_user.id

        db_bot = Bot(**bot_data)
        db.add(db_bot)
        db.commit()
        db.refresh(db_bot)
        return {db_bot}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bots/invoke")
def invoke_bot(item: InvokeBot, db: Session = Depends(get_db)):
    try:
        

        bot = db.query(Bot).filter(Bot.unique_id == item.unique_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        res = gemini_agent(bot, item.input, item.unique_id)
        return {"bot": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
