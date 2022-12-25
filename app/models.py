from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
# from sqlalchemy.orm import relationship


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, nullable=False)
    currency = Column(String)

    def __str__(self):
        return self.currency


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True, nullable=False)
    section = Column(String)

    def __str__(self):
        return self.section


class FamilyMember(Base):
    __tablename__ = 'members'

    # server_default - to have default argument when we create a table
    id = Column(Integer, primary_key=True, nullable=False)
    member = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    def __str__(self):
        return self.member


class Budget(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, nullable=False)
    creator = Column(Integer, ForeignKey('members.id', ondelete='CASCADE', related_name='creators'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    editor = Column(Integer, ForeignKey('members.id', ondelete='CASCADE', related_name='editors'))
    updated_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    date = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    currency = Column(String, ForeignKey('currencies.id', ondelete='CASCADE'))
    what_is = Column(String)
    section = Column(String, ForeignKey('sections.id', ondelete='CASCADE'))
    public = Column(Boolean, server_default='TRUE')
