from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

# we use router to divide path operations into different files
# use parameter prefix to remove the same path from decorators
# use parameter tags to divide path operations into docs page by groups
router = APIRouter(
    prefix="/currencies",
    tags=["Currencies"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Currency)
def create_currency(currency: schemas.CurrencyCreate, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # **post.dict() - to simplify classic way: title=post.title, content=post.content etc.
    new_currency = models.Currency(creator_id=current_user.id, editor_id=current_user.id, **currency.dict())
    db.add(new_currency)
    db.commit()
    db.refresh(new_currency)
    return new_currency
