from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    member: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    member: str
    email: EmailStr
    created_at: datetime

    # to read a data even it isn't a dict
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CurrencyBase(BaseModel):
    currency: str


class CurrencyCreate(CurrencyBase):
    pass


class Currency(CurrencyBase):
    id: int
    creator_id: int

    # to read a data even it isn't a dict
    class Config:
        orm_mode = True


class SectionBase(BaseModel):
    section: str


class SectionCreate(SectionBase):
    pass


class Section(SectionBase):
    id: int
    creator_id: int

    # to read a data even it isn't a dict
    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    # date: datetime
    total: float
    # currency: str
    what_is: str
    # section: str
    public: bool = True


class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    created_at: datetime
    owner_id: int
    # all information about user which we allow into UserOut schema
    owner: UserOut

    # to read a data even it isn't a dict
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


# schema for data which we embedded into access_token
class TokenData(BaseModel):
    id: Optional[str] = None
