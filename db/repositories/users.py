from db.models.users import User
from db.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = User