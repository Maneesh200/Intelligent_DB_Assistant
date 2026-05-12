from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///inventory.db"

engine = create_engine(DATABASE_URL, echo=True)