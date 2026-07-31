# from sqlalchemy.orm import Session

# # from app.models.user import User 

# # class UserRepository:

# #     def __init__(self, db: Session):
# #         self.db = db

# #     def get_by_email(self, email: str):
# #         return (
# #             self.db.query(User)
# #             .filter(User.email == email)
# #             .first()
# #         )

# #     # def create(self, user: User):
# #     #     self.db.add(user)
# #     #     self.db.commit()
# #     #     self.db.refresh(user)
# #     #     return user

from sqlalchemy import select 
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.orm import Session 

from app.models.user import User 
from app.repositories.base_repository import BaseRepository 

class UserRepository(BaseRepository[User]):

    def __init__(self, db: Session):

        super().__init__(db, User)

    def get_by_email(self, email: str):

        statement = select(User).where(
            User.email == email 
        )

        return self.db.scalar(statement)

    def get_users(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ):

        query = select(User)

        if search:
            query = query.where(
                or_(
                    User.name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )

        sort_column = getattr(User, sort_by)

        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        total = self.db.scalar(
            select(func.count()).select_from(query.subquery())
        )

        users = self.db.scalars(
            query.offset((page - 1) * limit).limit(limit)
        ).all()

        return users, total