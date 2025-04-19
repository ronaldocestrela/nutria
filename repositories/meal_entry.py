from typing import List, Optional
from tinydb import Query
from datetime import datetime
from models import MealEntry
from base_repository import BaseRepository

class MealEntryRepository(BaseRepository):
    """
    MealEntry repository to manage meal entries in the database.
    """
    def __init__(self):
        super().__init__()
        self.meal_entry_table = self.get_table('meal_entries')

    def create_meal_entry(
        self,
        user_id: int,
        meal_description: str,
        image_path: Optional[str] = None,
        calories: Optional[float] = None,
        carbs: Optional[float] = None,
        proteins: Optional[float] = None,
        fats: Optional[float] = None,
    ) -> MealEntry:
        new_meal_entry = MealEntry(
            user_id=user_id,
            meal_description=meal_description,
            image_path=image_path,
            calories=calories,
            carbs=carbs,
            proteins=proteins,
            fats=fats,
        )
        
        self.meal_entry_table.insert(new_meal_entry.model_dump())
        return new_meal_entry
    
    def get_meal_entry_by_user_and_date(self, user_id: int, date: datetime) -> List[MealEntry]:
        """
        Get a meal entry by user ID and date.
        """
        start_date = datetime.combine(date.date(), datetime.min.time())
        end_date = datetime.combine(date.date(), datetime.max.time())
        
        MealEntryQuery = Query()
        results = self.meal_entry_table.search(
            (MealEntryQuery.user_id == user_id) & 
            (MealEntryQuery.timestamp >= start_date) &
            (MealEntryQuery.timestamp <= end_date)
        )
        
        return [MealEntry(**entry) for entry in results] if results else []
    
    def update_meal_entry(self, meal_entry_id: id, **kwargs) -> Optional[MealEntry]:
        """
        Update a meal entry.
        """
        MealEntryQuery = Query()
        self.meal_entry_table.update(kwargs, MealEntryQuery.id == meal_entry_id)

    def delete_meal_entry(self, meal_entry_id: int) -> None:
        """
        Delete a meal entry.
        """
        MealEntryQuery = Query()
        self.meal_entry_table.remove(MealEntryQuery.id == meal_entry_id)
    
    def get_all_meal_entries(self) -> List[MealEntry]:
        """
        Get all meal entries.
        """
        results = self.meal_entry_table.all()
        
        return [MealEntry(**entry) for entry in results] if results else []