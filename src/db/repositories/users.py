from src.db.models.users import User
from src.db.repositories.base import BaseRepository
from src.db.repositories.mappers.mappers import UserDataMapper


class UsersRepository(BaseRepository):
    model = User
    mapper = UserDataMapper