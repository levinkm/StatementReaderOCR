import base64
from typing import Optional
from src.api.schemas.schemas import BankStatementUploadModel
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
    BackgroundTasks
)

from src.api.utils.rabbitmq import publish_bank_statement_to_rabbitmq

background_tasks = BackgroundTasks()

router = APIRouter(tags=["bank-statements"], prefix="/bank-statements")

# router to upload bank statements pdfs and also get the stutus of the processing the file
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_bank_statement(
    request: Request,
    account_id: str,
    user_id: str,
    file: UploadFile = File(...),
):
    data1 = file.file.read()

    print(data1,file=open("file_decoded.txt","w"))
    
   
   

    # Call the function to publish data (assuming it's implemented)
    publish_bank_statement_to_rabbitmq({
        "account_id": account_id,
        "user_id": user_id,
        "file_content": base64.b64encode(data1).decode('utf-8'),
    }, "bank-statements")

    # Do something with the file content (optional)
    # ... your processing logic here ...

    return {"filename": file.filename}