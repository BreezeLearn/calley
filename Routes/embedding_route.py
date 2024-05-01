from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models.models import Bot
from pydantic import BaseModel
from utils.generate_string import generate_random_string
from models.models import Embedding
from Agent.embeddings.gemini_embedding import gemini_embedding
from utils.get_embedding_text import get_text_from_url, get_text_from_pdf
from pydantic import validator


# was not able to fully implement embeddings so it;s not working, keaving the code for a rewrite after the hackathon




def generate_unique_id():
    import uuid
    return str(uuid.uuid4())


class EmbeddingsSchema(BaseModel):
    document_name: str
    unique_id: str
    bot_id: int
    doc_source: str
    doc_data: str

   

    @validator('unique_id', pre=True, always=True)
    def set_unique_id(cls, v):
        return v or generate_unique_id()


router = APIRouter()


@router.post("/embeddings")
def create_embedding(item: EmbeddingsSchema, db: Session = Depends(get_db)):
    try:
        embedding_data = item.dict()
        if embedding_data.get("doc_source") == "text":
            gemini_embedding(embedding_data.get("doc_data"))
        elif embedding_data.get("doc_source") == "url":
            text = get_text_from_url(embedding_data.get("doc_data"))
            gemini_embedding(text)
        # db_embedding = Embedding(**embedding_data)
        # db.add(db_embedding)
        # db.commit()
        # db.refresh(db_embedding)
        # return {"embedding": db_embedding}
        return {"message": "Embedding created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))