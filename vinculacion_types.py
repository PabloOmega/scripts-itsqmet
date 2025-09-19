from pydantic import BaseModel

class Actividad(BaseModel):
    actividad: str
    objetivo: str

class ActividadRespuesta(BaseModel):
    actividades: list[Actividad]