from typing import Optional
from tinydb import Query
from models import User
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    """
    User repository to manage user data in the database.
    """
    def __init__(self):
        super().__init__()
        self.user_table = self.get_table('users')
    
    def create_user(
        self,
        telegram_id: int,
        name: str,
        sex: str,
        age: int,
        height_cm: int,
        weight_kg: float,
        has_diabetes: bool,
        goal: str
    ) -> User:
        user = User(
            telegram_id=telegram_id,
            name=name,
            sex=sex,
            age=age,
            height_cm=height_cm,
            weight_kg=weight_kg,
            has_diabetes=has_diabetes,
            goal=goal
        )
        
        self.user_table.insert(user.model_dump())

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        """
        UserQuery = Query()
        result = self.user_table.get(UserQuery.id == user_id)
        
        return User(**result) if result else None
    
    def update_user(self, 
                    telegram_id: int,
                    name: str,
                    sex: str,
                    age: int,
                    height_cm: int,
                    weight_kg: float,
                    has_diabetes: bool,
                    goal: str
                ) -> None:
        """
        Update user information.
        """
        updated_user = {
            'telegram_id': telegram_id,
            'name': name,
            'sex': sex,
            'age': age,
            'height_cm': height_cm,
            'weight_kg': weight_kg,
            'has_diabetes': has_diabetes,
            'goal': goal
        }
        UserQuery = Query()
        self.user_table.update(updated_user, UserQuery.id == telegram_id)
    
    def delete_user(self, user_id: int) -> None:
        """
        Delete a user by ID.
        """
        UserQuery = Query()
        self.user_table.remove(UserQuery.id == user_id)
    
    def get_all_users(self) -> list[User]:
        """
        Get all users.
        """
        users = self.user_table.all()
        return [User(**user) for user in users] if users else []

    def get_user_by_telegram_id(self, telegram_id: str) -> Optional[User]:
        """
        Get a user by telegram_id.
        """
        user = self.table.get(Query().telegram_id == telegram_id)
        if user:
            return User(**user)
        return None