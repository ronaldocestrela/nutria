from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class WeightHistory(BaseModel):
    user_id: int
    timestamp: datetime = datetime.now(timezone.utc)
    weight_kg: float
    body_fat_percentage: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    water_percentage: Optional[float] = None
    bone_mass_kg: Optional[float] = None