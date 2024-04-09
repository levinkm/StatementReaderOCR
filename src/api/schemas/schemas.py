

from typing import List, Optional

from fastapi import UploadFile
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
        allow_population_by_field_name = True
    
class BankStatementModel(BaseModel):
    account_id: str
    transactions: List[Transaction]
    balance: float
    currency: str


# bank statement file upload model

class BankStatementUploadModel(BaseModel):
    file: UploadFile
    account_id: str
    user_id: str
    file_password: Optional[str] = None
    file_name: Optional[str] = None

    @validator('file')
    def file_must_be_pdf(cls, value):
        if value.content_type != 'application/pdf':
            raise ValueError('File must be a PDF')
        return value