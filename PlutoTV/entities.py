from typing import List, Optional
from pydantic import BaseModel, validator

"""
Se puede ajustar el modelo para que no sea obligatorio instanciar todos los campos,
más allá de que sean obligatorios o no. Esto ahorraría mucho espacio de código,
aunque tal vez quitaría visibilidad a la hora de armar un nuevo payload.
"""
class Payload(BaseModel):
    id       : str
    title    : Optional[str]
    genres   : List[str]
    synopsis : str
    rating   : str
    images   : List[dict]

    @validator('genres')#, check_fields=False)
    @classmethod
    def genres_check(cls, value):
        return value

class Movie(Payload):
    type : str = 'movie'

class Series(Payload):
    type : str = 'series'

class Episode(Payload):
    type : str = 'episode'