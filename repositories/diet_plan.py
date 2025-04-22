from typing import Optional, List
from tinydb import Query
from repositories.base_repository import BaseRepository
from models import DietPlan
import json

class DietPlanRepository(BaseRepository):
    """
    DietPlan repository to manage diet plans in the database.
    """
    def __init__(self):
        super().__init__()
        self.diet_plan_table = self.get_table('diet_plans')
    
    def create_diet_plan(
        self,
        telegram_id: int,
        details: str,
    ) -> DietPlan:
        new_diet_plan = DietPlan(
            user_id=telegram_id,
            details=details
        )
        
        self.diet_plan_table.insert(json.loads(new_diet_plan.model_dump_json()))
        return new_diet_plan
    
    def get_dite_plan_by_id(self, diet_plan_id: int) -> Optional[DietPlan]:
        """
        Get a diet plan by ID.
        """
        DietPlanQuery = Query()
        result = self.diet_plan_table.get(DietPlanQuery.id == diet_plan_id)
        
        return DietPlan(**result) if result else None
    
    def get_diet_plans_by_user_id(self, user_id: int) -> List[DietPlan]:
        """
        Get all diet plans for a specific user.
        """
        DietPlanQuery = Query()
        results = self.diet_plan_table.search(DietPlanQuery.user_id == user_id)
        
        return [DietPlan(**result) for result in results] if results else []
    
    def get_latest_diet_plan_by_user_id(self, telegram_id: int) -> Optional[DietPlan]:
        """
        Get the latest diet plan for a specific user.
        """
        DietPlanQuery = Query()
        diet_plans = self.diet_plan_table.search(DietPlanQuery.telegram_id == telegram_id)
        
        if diet_plans:
            latest_diet_plan = sorted(diet_plans, key=lambda x: x['created_at'], reverse=True)[0]
            return DietPlan(**latest_diet_plan)
        
        return None
    
    def update_diet_plan(self, plan_id: int, details: str) -> None:
        """
        Update a diet plan.
        """
        DietPlanQuery = Query()
        self.diet_plan_table.update({'details': details}, DietPlanQuery.id == plan_id)
        
        updated_diet_plan = self.diet_plan_table.get(DietPlanQuery.id == plan_id)
        return DietPlan(**updated_diet_plan) if updated_diet_plan else None
    
    def delete_diet_plan(self, plan_id: int) -> None:
        """
        Delete a diet plan.
        """
        DietPlanQuery = Query()
        self.diet_plan_table.remove(DietPlanQuery.id == plan_id)
        
    def get_all_diet_plans(self) -> List[DietPlan]:
        """
        Get all diet plans.
        """
        results = self.diet_plan_table.all()
        
        return [DietPlan(**result) for result in results] if results else []    