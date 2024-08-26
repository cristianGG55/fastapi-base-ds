from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime
from src.example.models import TipoMascota, TipoVehiculo
from src.example.constants import ErrorCode
from src.example import exceptions

# Los siguientes schemas contienen atributos sin muchas restricciones de tipo.
# Podemos crear atributos con ciertas reglas mediante el uso de un "Field" adecuado.
# https://docs.pydantic.dev/latest/concepts/fields/


class PersonaBase(BaseModel):
    nombre: str
    email: EmailStr


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(PersonaBase):
    pass


class Persona(PersonaBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    mascotas: List["Mascota"]

    # from_atributes=True permite que Pydantic trabaje con modelos SQLAlchemy
    # más info.: https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.from_attributes
    model_config = {"from_attributes": True}


class VehiculoBase(BaseModel):
    patente: str
    tipo: TipoVehiculo  # solo permitiremos valores de este tipo.
    marca: str

    @field_validator("tipo", mode="before")
    @classmethod
    def is_valid_tipo_vehiculo(cls, v: str) -> str:
        if v.lower() not in TipoVehiculo:
            raise exceptions.TipoVehiculoInvalido(list(TipoVehiculo))
        return v.lower()

class VehiculoCreate(VehiculoBase):
    persona_id: int

class Vehiculo(VehiculoBase):
    id: int
    persona_id: int
    persona: Persona
    fecha_creacion: datetime
    fecha_modificacion: datetime

class VehiculoUpdate(VehiculoCreate):
    pass


class MascotaBase(BaseModel):
    nombre: str
    tipo: TipoMascota  # solo permitiremos valores de este tipo.

    @field_validator("tipo", mode="before")
    @classmethod
    def is_valid_tipo_mascota(cls, v: str) -> str:
        if v.lower() not in TipoMascota:
            raise exceptions.TipoMascotaInvalido(list(TipoMascota))
        return v.lower()


class MascotaCreate(MascotaBase):
    tutor_id: int






class Mascota(MascotaBase):
    id: int

    tipo: TipoMascota
    tutor_id: int
    nombre_tutor: str
    fecha_creacion: datetime
    fecha_modificacion: datetime
    
    model_config = {"from_attributes": True}


class MascotaUpdate(MascotaBase):
    pass


    

