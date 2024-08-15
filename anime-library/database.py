from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "sqlite:///./data/test.db"  # SQLite database URL

# Create a SQLAlchemy engine and database connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database = Database(DATABASE_URL)

# Define the Base class
Base = declarative_base()

# Define the Anime model
class AnimeModel(Base):
    __tablename__ = "animes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    release_year = Column(Integer)
    genre = Column(String)
    seasons = Column(Integer)
    episodes = Column(Integer)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
