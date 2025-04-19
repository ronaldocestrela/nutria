from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class MealEntry(BaseModel):
    user_id: int
    timestamp: datetime = datetime.now(timezone.utc)
    meal_description: str
    image_path: Optional[str] = None
    calories: Optional[float] = None
    carbs: Optional[float] = None
    proteins: Optional[float] = None
    fats: Optional[float] = None