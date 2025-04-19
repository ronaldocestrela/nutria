from pydantic import BaseModel
class User(BaseModel):
    telegraId: int
    name: str
    sexo: str
    age: int
    height_cm: int
    weight_kg: float
    has_diabetes: bool
    goal: str