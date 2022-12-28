from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy.sql.expression import text
# from sqlalchemy.orm import relationship


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, nullable=False)
    currency = Column(String, nullable=False)
    country = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    editor_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True, nullable=False)
    section = Column(String)
    creator_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    editor_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class FamilyMember(Base):
    __tablename__ = 'members'

    # server_default - to have default argument when we create a table
    id = Column(Integer, primary_key=True, nullable=False)
    member = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Budget(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, nullable=False)
    creator_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    editor_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    date = Column(DATE, nullable=False, server_default=text('now()'))
    total = Column(Float, nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id', ondelete='CASCADE'))
    what_is = Column(String)
    section_id = Column(Integer, ForeignKey('sections.id', ondelete='CASCADE'))
    public = Column(Boolean, server_default='TRUE')
