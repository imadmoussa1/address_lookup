from pydantic import BaseModel, Json
from typing import Optional, Dict


class Msg(BaseModel):
  msg: Optional[str]

class Address(BaseModel):
  index: Optional[int] = 0
  LON: Optional[float] = None
  LAT: Optional[float] = None
  NUMBER: Optional[str] = None
  STREET: Optional[str] = None
  UNIT: Optional[str] = None
  CITY: Optional[str] = None
  DISTRICT: Optional[str] = None
  REGION: Optional[str] = None
  POSTCODE: Optional[int] = None
