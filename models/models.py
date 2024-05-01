import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, ARRAY
from config.database import Base
import json

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, index=True)
    token_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tokens")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    tokens = relationship("Token", back_populates="user")
    bots = relationship("Bot", back_populates="user")


class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, unique=False, index=True)
    unique_id = Column(String, unique=True, index=True)
    web_search = Column(Boolean, unique=False, index=True)
    instruction = Column(String, unique=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="bots")

    _tools = Column("tools", String)  # Serialized list stored as string

    @property
    def tools(self):
        return json.loads(self._tools) if self._tools else []

    @tools.setter
    def tools(self, value):
        self._tools = json.dumps(value)

    embeddings = relationship("Embedding", back_populates="bot")


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, unique=True, index=True)
    
    unique_id = Column(String, unique=True, index=True)

    bot_id = Column(Integer, ForeignKey("bots.id"))

    bot = relationship("Bot", back_populates="embeddings")