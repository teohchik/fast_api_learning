from src.db.models.users import User
from src.db.repositories.base import BaseRepository
from src.schemas.user import UserResponse


class UsersRepository(BaseRepository):
    model = User
    schema = UserResponse