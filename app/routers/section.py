from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

# we use router to divide path operations into different files
# use parameter prefix to remove the same path from decorators
# use parameter tags to divide path operations into docs page by groups
router = APIRouter(
    prefix="/sections",
    tags=["Sections"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Section)
def create_section(section: schemas.SectionCreate, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    # **post.dict() - to simplify classic way: title=post.title, content=post.content etc.
    new_section = models.Section(creator_id=current_user.id, editor_id=current_user.id, **section.dict())
    db.add(new_section)
    db.commit()
    db.refresh(new_section)
    return new_section
