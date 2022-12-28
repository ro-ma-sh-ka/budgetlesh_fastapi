from fastapi import status, Depends, APIRouter, HTTPException
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


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Section)
def update_section(id: int, updated_section: schemas.SectionCreate, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    # to improve - use current_user to check permissions (update, delete etc)
    section_query = db.query(models.Section).filter(models.Section.id == id)
    section = section_query.first()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'section with id {id} does not exist')
    section_query.update(updated_section.dict())
    db.commit()
    return {'message': 'section successfully updated'}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_section(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # to improve - use current_user to check permissions (update, delete etc)
    section_query = db.query(models.Section).filter(models.Section.id == id)
    section = section_query.first()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'section with id {id} does not exist')
    section_query.delete(synchronize_session=False)
    db.commit()
    return {'message': 'section successfully deleted'}
