from langchain.tools import BaseTool
from repositories.user import UserRepository
from repositories.weight_history import WeightHistoryRepository

class WeightUpdateTool(BaseTool):
    name: str = "weight_update"
    description: str = (
        "Use esta ferramenta para registrar o peso de um usuário. "
        "Entrada: telegram_id do usuário e weight_kg."
    )
    
    def __init__(self):
        super().__init__()
        self._user_repository = UserRepository()
        self._weight_history_repository = WeightHistoryRepository()
        
    def _run(self, telegram_id: str, weight_kg: float) -> str:
        try:
            user = self._user_repository.get_user_by_telegram_id(telegram_id)
            if not user:
                return "Usuário não encontrado. Pro favor, registre o usuário primeiro."
            
            # Create a new weight entry
            self._weight_history_repository.create_weight_history(user.id, weight_kg)
            return "Peso registrado com sucesso."
        
        except Exception as e:
            return f"Erro ao processar a solicitação: {str(e)}"
    
    async def _arun(self, telegram_id: str, weight_kg: float) -> str:
        raise NotImplementedError("WeightUpdateTool does not support async run.")