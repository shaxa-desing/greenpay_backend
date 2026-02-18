import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("postgresql://postgres:tIzRebfZKIkiiQwNziZAxuDWKGFKKjzn@postgres.railway.internal:5432/railway")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
