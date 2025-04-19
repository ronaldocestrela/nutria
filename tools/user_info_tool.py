from typing import Any, Dict, Type
from pydantic import BaseModel
from langchain.tools import BaseTool
from repositories.user import UserRepository
from models import User

class UserInfoTool(BaseTool):
    name: str = "user_info"
    description: str = (
        "Use esta ferramenta para buscar informações de um usuário existente. "
        "Ela requer o telegram_id do usuário como entrada para recuperar os dados."
    )
    
    def __init__(self):
        super().__init__()
        self._user_repository = UserRepository()
    
    def _run(self, telegram_id: int) -> str:
        """
        Retrieve user information by telegram_id.
        """
        try:
            user = self._user_repository.get_user_by_telegram_id(telegram_id)
            
            if not user:
                return "Usuário não encontrado."

            user_info = (
                f"Nome: {user.name}\n"
                f"Sexo: {user.sex}\n"
                f"Idade: {user.age}\n"
                f"Altura: {user.height_cm} cm\n"
                f"Peso: {user.weight_kg} kg\n"
                f"Diabetes: {'Sim' if user.has_diabetes else 'Não'}\n"
                f"Objetivo: {user.goal}\n"
            )
            return user_info
        
        except Exception as e:
            return f"Erro ao buscar informações do usuário: {str(e)}"
    
    async def _arun(self, telegram_id: int) -> str:
        raise NotImplementedError("Asynchronous run is not implemented.")