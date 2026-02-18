import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("postgresql://postgres:tIzRebfZKIkiiQwNziZAxuDWKGFKKjzn@postgres.railway.internal:5432/railway")

# Railway postgres:// ni postgresql:// ga o‘zgartiramiz
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
