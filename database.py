from sqlalchemy.orm import declarative_base, sessionmaker,Session
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("DATABASE_URL")

Base = declarative_base()

engine = create_engine(URL)

goonsession = sessionmaker(bind=engine)
