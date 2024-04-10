

from typing import List, Optional

from fastapi import File, UploadFile
from pydantic import BaseModel, constr, validator

class Transaction(BaseModel):
    category_id: int
    name: str
    wallet_id: str
    transaction_id: str
    amount: float
    charges: float
    type: str

    class Config:
        # Allow both camelCase and snake_case for field names
        alias_generator = lambda s: s
        populate_by_name = True
    
class BankStatementModel(BaseModel):
    account_id: str
    transactions: List[Transaction]
    balance: float
    currency: str


# bank statement file upload model
class BankStatementUploadModel(BaseModel):
    
    name: str
    description: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            'datetime': lambda v: v.isoformat()
            }

class BankStatementUploadRequest(BaseModel):
    bank_statement_data: BankStatementUploadModel