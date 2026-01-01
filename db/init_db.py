from db.base import Base
from db.session import engine
import db.models.users
import db.models.expenses
import db.models.categories


def init_db():
    Base.metadata.create_all(bind=engine)
