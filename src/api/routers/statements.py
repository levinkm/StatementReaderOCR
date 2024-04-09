from typing import Optional
from schemas.schemas import BankStatementUploadModel
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
    BackgroundTasks
)


background_tasks = BackgroundTasks()

router = APIRouter(tags=["bank-statements"], prefix="/bank-statements")

# router to upload bank statements pdfs and also get the stutus of the processing the file
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_bank_statement(
    bank_statement_data: BankStatementUploadModel,
    
):
    # Process the uploaded file
    content = await bank_statement_data.file.read()
    
    #TODO:  publish the file , userid and accountid to rabbitMQ queue
   



    # Do something with the file content, such as saving it to disk or processing it further
    # You can access other form fields (account_id, user_id, file_password, file_name) through bank_statement_data
    return {"filename": bank_statement_data.file.filename}