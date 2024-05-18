import os
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


sql_db_path = os.path.join(pathlib.Path(__file__).parent.parent, "database.db")
sql_db_link = f"sqlite:///{sql_db_path}"

engine = create_engine(sql_db_link, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    with SessionLocal as session:
        yield session


# Base class for database models
Base = declarative_base()

# This will create the database tables
Base.metadata.create_all(bind=engine)
