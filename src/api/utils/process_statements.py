from ocr.bank_statements import clean_statements,read_statements
import io
import os
import tempfile
from fastapi import HTTPException

async def process_file(file,password=None):

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        contents = await file.read() 
        tmp_file.write(contents)
        tmp_file_path = tmp_file.name

    try:
        # Extract tables from the PDF using Camelot
        tables = read_statements.ReadPdf.read_pdf(tmp_file_path,password=password)
        statements = clean_statements.CleanData.clean_data(tables)

        return statements
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting tables: {e}")
    finally:
        # Delete the temporary file
        if tmp_file_path:
            os.unlink(tmp_file_path)
    
