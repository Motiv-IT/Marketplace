from schemas import CategoryBase
from db.model import DbCategory
from sqlalchemy.orm import Session

# create category
def create_category(db:Session, request: CategoryBase):
    new_category = DbCategory(
        title = request.title,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
