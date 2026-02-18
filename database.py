import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

# None bo‘lmasligi uchun
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found")

# postgres:// → postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# oxiridagi bo‘sh joylarni olib tashlaymiz
DATABASE_URL = DATABASE_URL.strip()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
