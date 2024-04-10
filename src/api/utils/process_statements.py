import camelot.core
from src.ocr.bank_statements import clean_statements,read_statements
import io
import os
import tempfile
from fastapi import HTTPException
import camelot


def send_notification(message):
    # Placeholder function to send notification (e.g., email, push notification, etc.)
    print("Notification:", message)

async def process_file(file, password=None):

   

    try:
        # Validate file format (replace with your validation logic)
        # ...

        # Extract tables from the PDF using Camelot
        tables = await read_statements.ReadPdf.read_pdf(file, password=password)
        statements = await clean_statements.CleanData.clean_data(tables)

        send_notification("Tables extracted successfully")

        return statements

 
    except Exception as e:
        # Catch other unexpected exceptions
        raise HTTPException(status_code=500, detail=f"Error extracting tables: {e}")
    
    
