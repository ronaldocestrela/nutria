from langchain.tools import BaseTool
from typing import Optional
from repositories.diet_plan import DietPlanRepository
from repositories.user import UserRepository

class DietPlanTool(BaseTool):
    name: str = "diet_plan"
    description: str = (
        "Use esta ferramenta para criar um plano de dieta de um usuário. "
        "Entrada: telegram_id do usuário e, e plan_details para criar um novo plano ou buscar um plano já existente."
        "A regra para essa Tool é quando o usuario gostar do plano montado por você ai você está autorizado a usar essa tool para salvar o plano"
    )
    
    def __init__(self):
        super().__init__()
        self._diet_plan_repository = DietPlanRepository()
        self._user_repository = UserRepository()

    def _run(self, telegram_id: str, plan_details: Optional[str] = None) -> str:
        try:
            user = self._user_repository.get_user_by_telegram_id(telegram_id)
            if not user:
                return "Usuário não encontrado. Pro favor, registre o usuário primeiro."

            if plan_details:
                # Create a new diet plan
                self._diet_plan_repository.create_diet_plan(user.id, plan_details)
                return "Plano de dieta criado com sucesso."

            # Fetch the existing diet plan
            last_plan_diet = self._diet_plan_repository.get_latest_diet_plan_by_user_id(user.telegra_id)
            if last_plan_diet:
                return f"Plano de dieta para {user.name}: {last_plan_diet.details}"
            else:
                return f"Nenhum plano de dieta encontrado para {user.name}."

        except Exception as e:
            return f"Erro ao processar a solicitação: {str(e)}"

    async def _arun(self, telegram_id: str, plan_details: Optional[str] = None) -> str:
        raise NotImplementedError("DietPlanTool does not support async run.")