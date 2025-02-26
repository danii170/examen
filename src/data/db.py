from sqlmodel import create_engine, SQLModel, Session
from src.models.podcast import Podcast

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "localhost" 
db_port: int = 3306  
db_name: str = "podcastdb"  

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Podcast(nombre="cancion1", autor="Autor1 ", duracion=5))
        session.add(Podcast(nombre="cancion2", autor="Autor2 ", duracion=10))
        session.add(Podcast(nombre="cancion3", autor="Autor3 ", duracion=4))
        session.commit()
        