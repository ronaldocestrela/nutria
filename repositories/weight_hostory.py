from typing import List, Optional
from tinydb import Query
from datetime import datetime
from base_repository import BaseRepository
from models import WeightHistory

class WeightHistoryRepository(BaseRepository):
    """
    WeightHistory repository to manage weight history in the database.
    """
    def __init__(self) -> None:
        super().__init__()
        self.weight_history_table = self.get_table('weight_history')
    
    def create_weight_history(
        self,
        user_id: int,
        weight_kg: float,
        body_fat_percentage: Optional[float] = None,
        muscle_mass_kg: Optional[float] = None,
        water_percentage: Optional[float] = None,
        bone_mass_kg: Optional[float] = None,
    ) -> WeightHistory:
        """
        Create a new weight history entry.
        """
        new_weight_history = WeightHistory(
            user_id=user_id,
            weight_kg=weight_kg,
            body_fat_percentage=body_fat_percentage,
            muscle_mass_kg=muscle_mass_kg,
            water_percentage=water_percentage,
            bone_mass_kg=bone_mass_kg,
        )
        
        self.weight_history_table.insert(new_weight_history.model_dump())
        return new_weight_history
    
    def get_weight_history_by_user_and_date(self, user_id: int, date: datetime) -> List[WeightHistory]:
        """
        Get weight history by user ID and date.
        """
        start_date = datetime.combine(date.date(), datetime.min.time())
        end_date = datetime.combine(date.date(), datetime.max.time())
        
        WeightHistoryQuery = Query()
        results = self.weight_history_table.search(
            (WeightHistoryQuery.user_id == user_id) & 
            (WeightHistoryQuery.timestamp >= start_date) &
            (WeightHistoryQuery.timestamp <= end_date)
        )
        sorted_results = sorted(results, key=lambda x: x['timestamp'], reverse=True)
        
        return [WeightHistory(**entry) for entry in sorted_results] if results else []
    
    def get_weight_entry_by_id(self, weight_entry_id: int) -> Optional[WeightHistory]:
        """
        Get a weight entry by ID.
        """
        WeightHistoryQuery = Query()
        result = self.weight_history_table.get(WeightHistoryQuery.id == weight_entry_id)
        
        return WeightHistory(**result) if result else None
    
    def delete_weight_entry(self, weight_entry_id: int) -> None:
        """
        Delete a weight entry.
        """
        WeightHistoryQuery = Query()
        self.weight_history_table.remove(WeightHistoryQuery.id == weight_entry_id)
        return None
    
    def get_all_weight_entries(self) -> List[WeightHistory]:
        """
        Get all weight entries.
        """
        results = self.weight_history_table.all()
        
        return [WeightHistory(**entry) for entry in results] if results else []