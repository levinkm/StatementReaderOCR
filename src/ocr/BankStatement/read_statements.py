import os

import camelot
import asyncio


#---------------------------------------------------------------------------------------------------------------------------------------
# Reading Data
#---------------------------------------------------------------------------------------------------------------------------------------

async def read_pdf(file_path, flavour,strip_text,pages):
    """
    Read tables from a PDF file using Camelot in a separate thread.

    Args:   
        file_path (str): Path to the PDF file.
        flavour (str): Flavor of the PDF extraction method ('stream' or 'lattice').
        strip_text (str): Characters to strip from text.
        pages (str): Page range to extract tables from.

    Returns:
        list: Tables read from the PDF file.

    """
    tables = await asyncio.to_thread(camelot.read_pdf, file_path, flavor=flavour, strip_text=strip_text, pages=pages)
    return tables

async def process_file(file_path)-> tuple :
    """
    Process a PDF file to extract tables in stream and lattice flavors in parallel.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        tuple: Tables read from the PDF file in stream and lattice flavors.

    """
   
    stream_task = read_pdf(file_path, flavour='stream', strip_text=' .\n', pages='1-end')
    lattice_task = read_pdf(file_path, flavour='lattice', strip_text=' .\n', pages='1-end')
    
    stream_tables, lattice_tables = await asyncio.gather(stream_task, lattice_task)
    
    return stream_tables, lattice_tables


def calc_accuracy_and_whitespaces(tables)-> tuple:
    """
    Calculates average accuracy and average whitespace from a list of pandas DataFrames.

    Args:
        tables (list of pandas.DataFrame): List of pandas DataFrames representing tables.

    Returns:
        tuple: Tuple containing the average accuracy and average whitespace.

    """
    accuracy = 0
    whitespace=0
    for table in tables:
            
            parsing_report = table.parsing_report
            accuracy+=parsing_report['accuracy']
            whitespace+=parsing_report['whitespace']

    accuracy =  accuracy/len(tables)

    whitespace = whitespace/len(tables)

    return accuracy, whitespace


def get_result(lattice_result,stream_result):
    """
    Determine the result to be returned (either lattice or stream) based on accuracy average and whitespace average.

    Args:
        lattice_result: Result from lattice extraction.
        stream_result: Result from stream extraction.

    Returns:
        list: Result from extraction (either 'lattice' or 'stream').

    """
    
    laccuracy,lwhitespace = calc_accuracy_and_whitespaces(lattice_result)
    saccuracy,swhitespace = calc_accuracy_and_whitespaces(stream_result)

    if laccuracy > saccuracy or lwhitespace < swhitespace:
        return lattice_result
    
    elif saccuracy > laccuracy or swhitespace < lwhitespace:
        return stream_result
    

async def main(file_path):
    
    stream_tables, lattice_tables = await process_file(file_path)

    return get_result(lattice_tables, stream_tables)


file_path = f"{os.getcwd()}/Account_statement.pdf"

def readPdf(file_path):
    """
    Read a PDF file asynchronously and return the extracted text.

    This function uses asyncio to asynchronously read the text content of a PDF file
    located at the given file path.

    Args:
        file_path (str): The path to the PDF file to be read.

    Returns:
        str: The extracted text content of the PDF file.

    Raises:
        FileNotFoundError: If the specified file cannot be found.
        RuntimeError: If there is an issue with reading the PDF file.
    """
    return asyncio.run(main(file_path))
