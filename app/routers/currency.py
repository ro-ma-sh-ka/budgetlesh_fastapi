from fastapi import status, Depends, APIRouter, HTTPException
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


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Currency)
def update_currency(id: int, updated_currency: schemas.CurrencyCreate, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    # to improve - use current_user to check permissions (update, delete etc)
    currency_query = db.query(models.Currency).filter(models.Currency.id == id)
    currency = currency_query.first()
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'currency with id {id} does not exist')
    currency_query.update(updated_currency.dict(), synchronize_session=False)
    db.commit()
    return {'message': 'currency updated'}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_currency(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # to improve - use current_user to check permissions (update, delete etc)
    currency_query = db.query(models.Currency).filter(models.Currency.id == id)
    currency = currency_query.first()
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'currency with id {id} does not exist')
    currency_query.delete(synchronize_session=False)
    db.commit()
    return {'message': 'currency deleted'}
