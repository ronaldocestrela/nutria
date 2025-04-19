from pydantic import BaseModel, Field
class User(BaseModel):
    telegra_id: int = Field(..., description="Telegram ID do usuário")
    name: str = Field(..., description="Nome completo do usuário")
    sex: str = Field(..., description="Sexo do usuário (masculino ou feminino)")
    age: int = Field(..., description="Idade do usuário. Exemplo : 25")
    height_cm: int = Field(..., description="Altura do usuário em centímetros. Exemplo : 175") 
    weight_kg: float = Field(..., description="Peso do usuário em quilogramas. Exemplo : 70.5")
    has_diabetes: bool = Field(..., description="Se o usuário tem diabetes ou não. Exemplo : True ou False")
    goal: str = Field(..., description="Objetivo do usuário (perder peso, ganhar peso, ganhar massa muscular)")