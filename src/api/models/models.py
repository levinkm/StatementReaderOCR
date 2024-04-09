import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, Integer, text
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID, ARRAY

import uuid

from database import Base
from sqlalchemy import ForeignKey


class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=text("now()"))

class Accounts(BaseModel):
    __tablename__ = "accounts"

    name = Column(String)
    currency = Column(String)
    balance = Column(Integer)
    transactions = relationship("Transactions", back_populates="account")


class Transactions(BaseModel):
    __tablename__ = "transactions"

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    amount = Column(Integer)
    currency = Column(String)
    category = Column(String)
    account = relationship("Accounts", back_populates="transactions")
    transaction_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    narration = Column(String)

    
class Users(BaseModel):

    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    first_name = Column(String)
    last_name = Column(String)
    accounts = relationship("Accounts", back_populates="user")
    transactions = relationship("Transactions", back_populates="user")

class AppAuth(BaseModel):
    __tablename__ = "app_auth"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    token = Column(String)
    user = relationship("Users", back_populates="app_auth")