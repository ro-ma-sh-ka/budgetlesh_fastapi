from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

# we use router to divide path operations into different files
# use parameter prefix to remove the same path from decorators
# use parameter tags to divide path operations into docs page by groups
router = APIRouter(
    prefix="/expenses",
    tags=['Expenses']
)


# we use type List from typing to adjust our schema Post showing list of data
@router.get("/", response_model=List[schemas.Expense])
def get_expenses(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                 limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # query parameters#
    # limit = how many results will have a user, we use method limit
    # skip = how many results query will skip, we use method offset. We can use it for pagination
    # search - search key words, We use method filter
    expenses = db.query(models.Budget).all()
    return expenses


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Expense)
def add_expenses(expense: schemas.ExpenseCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # **post.dict() - to simplify classic way: title=post.title, content=post.content etc.
    new_expense = models.Budget(creator_id=current_user.id, editor_id=current_user.id, **expense.dict())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/{id}", response_model=schemas.Expense)
def get_expenses(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    expense_query = db.query(models.Budget).filter(models.Budget.id == id)

    expense = expense_query.first()

    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} was not found')
    return expense


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    expense_query = db.query(models.Budget).filter(models.Budget.id == id)

    expense = expense_query.first()

    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} was not found')

    if expense.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to delete this post')

    # synchronize_session - read documentation
    expense_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Expense)
def update_expense(id: int, updated_post: schemas.ExpenseCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    expense_query = db.query(models.Budget).filter(models.Budget.id == id)
    expense = expense_query.first()
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} was not found')

    if expense.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to update this post')

    expense_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return expense
