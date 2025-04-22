from langchain.tools import BaseTool
from typing import Optional, Dict, Any
from repositories.meal_entry import MealEntryRepository
from repositories.user import UserRepository

class MealEntryTool(BaseTool):
    name: str = "meal_entry"
    description: str = (
        "Ferramenta para toda vez que o usuario quiser que você registre uma refeição que ele fez no dia"
        "se você nao tiver todos os dados para registrar uma refeição, pergunte a ao usuario até que tenha todas as informações necessarias"
        "Use esta ferramenta para registrar uma refeição de um usuário. "
        "Entrada: como meal_description, calories, carbs, proteins, fats."
        "Você deve se basear nas informações que o usuario passou para gerar as informações de calories, carbs, proteins, fats"
    )
    
    def __init__(self):
        super().__init__()
        self._meal_entry_repository = MealEntryRepository()
        self._user_repository = UserRepository()
    
    def _run(self, 
        telegram_id: str, 
        meal_description: str, 
        image_path: Optional[str] = None, 
        calories: Optional[float] = None, 
        carbs: Optional[float] = None, 
        proteins: Optional[float] = None, 
        fats: Optional[float] = None
    ) -> str:
        try:
            user = self._user_repository.get_user_by_telegram_id(telegram_id)
            if not user:
                return "Usuário não encontrado. Pro favor, registre o usuário primeiro."
            
            # Create a new meal entry
            self._meal_entry_repository.create_meal_entry(
                telegram_id=user.telegram_id,
                meal_description=meal_description,
                image_path=image_path,
                calories=calories,
                carbs=carbs,
                proteins=proteins,
                fats=fats
            )
            return "Refeição registrada com sucesso."
        except Exception as e:
            return f"Erro ao processar a solicitação de registro de refeição: {str(e)}"
    
    async def _arun(self, telegram_id: str, meal_description: str, calories: Optional[float] = None, carbs: Optional[float] = None, proteins: Optional[float] = None, fats: Optional[float] = None) -> str:
        raise NotImplementedError("MealEntryTool does not support async run.")