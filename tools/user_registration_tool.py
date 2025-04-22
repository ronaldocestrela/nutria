from typing import Any, Dict, Type
from pydantic import BaseModel
from langchain.tools import BaseTool
from repositories.user import UserRepository
from models import User

class UserRegistrationTool(BaseTool):
    name: str = "user_registration"
    description: str = (
    "Use esta ferramenta para registrar um novo usuário ou atualizar as informações de um usuário existente. "
    "Esta ferramenta requer os seguintes dados do usuário: "
    "telegram_id, name (nome), sex (sexo), age (idade como um int), height_cm (altura em centímetros como um float), weight_kg (peso em quilogramas como um float), "
    "has_diabetes (se tem diabetes: bool onde true para sim e false para não) e goal (objetivo: perder peso, ganhar peso, ganhar massa muscular). "
    "Forneça esses dados no formato de um dicionário python com as seguintes chaves: "
    "'name', 'sex', 'age', 'height_cm', 'weight_kg', 'has_diabetes', e 'goal'. "
    "Se algum dado estiver faltando, você deve primeiro coletar essas informações do usuário antes de usar esta ferramenta."
    )
    
    args_schema: Type[BaseModel] = User
    
    def __init__(self):
        super().__init__()
        self._user_repository = UserRepository()
    
    def _run(self, 
        telegra_id: int,
        name: str,
        sex: str,
        age: int,
        height_cm: int,
        weight_kg: float,
        has_diabetes: bool,
        goal: str,
    ) -> str:
        if not name:
            raise ValueError("Nome do usuário não pode ser vazio.")
        
        try:
            user_data = {
                "telegra_id": telegra_id,
                "name": name,
                "sex": sex,
                "age": age,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "has_diabetes": has_diabetes,
                "goal": goal
            }
            
            user = self._user_repository.get_user_by_id(telegra_id)

            if user:
                updated_user = self._user_repository.update_user(**user_data)
                return f"Usuário atualizado com sucesso: {updated_user}"
            
            new_user = self._user_repository.create_user(**user_data)
            return f"Usuário registrado com sucesso: {new_user}"
        except Exception as e:
            return f"Erro ao registrar o usuário: {str(e)}"

    async def _arun(self, 
        telegra_id: int,
        name: str,
        sex: str,
        age: int,
        height_cm: int,
        weight_kg: float,
        has_diabetes: bool,
        goal: str,
    ) -> str:
        """
        Asynchronous version of the run method.
        """
        raise NotImplementedError("Asynchronous run is not implemented.")