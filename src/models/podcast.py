from sqlmodel import Field, SQLModel

class Podcast(SQLModel, table=True):
    nombre: str | None = Field(default=None, primary_key=True)
    autor: str = Field(index=True, max_length=50)
    duracion: int = Field(gt=0)

