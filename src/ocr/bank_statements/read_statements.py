import os
import io
import shutil
import tempfile

import camelot
import asyncio


#---------------------------------------------------------------------------------------------------------------------------------------
# Reading Data
#---------------------------------------------------------------------------------------------------------------------------------------
class ReadPdf:

    """
    Class to read tables from a PDF file using Camelot.
    """
    
    @staticmethod
    async def read_file(file, flavour,strip_text,pages, password=None):
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
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(file)
                temp_file_path = temp_file.name
            # Close the file to ensure data is flushed to disk
            temp_file.close()

       
            print(f"Reading tables from {temp_file_path} using {flavour} flavor...")
            tables = await asyncio.to_thread(camelot.read_pdf, temp_file_path, flavor=flavour, strip_text=strip_text, pages=pages, password=password)
            return tables
        finally:
            # Delete the temporary file
            os.unlink(temp_file.name)
           
    @classmethod
    async def process_file(cls,file_path,password=None)-> tuple :
        """
        Process a PDF file to extract tables in stream and lattice flavors in parallel.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            tuple: Tables read from the PDF file in stream and lattice flavors.

        """
    
        stream_task = cls.read_file(file_path, flavour='stream', strip_text=' .\n', pages='1-end',password=password)
        lattice_task = cls.read_file(file_path, flavour='lattice', strip_text=' .\n', pages='1-end',password=password)
        
        stream_tables, lattice_tables = await asyncio.gather(stream_task, lattice_task)
        
        return stream_tables, lattice_tables

    @staticmethod
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

    @classmethod
    def get_result(cls,lattice_result,stream_result):
        """
        Determine the result to be returned (either lattice or stream) based on accuracy average and whitespace average.

        Args:
            lattice_result: Result from lattice extraction.
            stream_result: Result from stream extraction.

        Returns:
            list: Result from extraction (either 'lattice' or 'stream').

        """
        
        laccuracy,lwhitespace = cls.calc_accuracy_and_whitespaces(lattice_result)
        saccuracy,swhitespace = cls.calc_accuracy_and_whitespaces(stream_result)

        if laccuracy > saccuracy or lwhitespace < swhitespace:
            return lattice_result
        
        elif saccuracy > laccuracy or swhitespace < lwhitespace:
            return stream_result
        
    @classmethod
    async def main(cls,file_path,password=None):
        
        stream_tables, lattice_tables = await cls.process_file(file_path,password=password)

        return cls.get_result(lattice_tables, stream_tables)


    @classmethod
    async def read_pdf(cls,file_path:str | io.BytesIO ,password =None) :
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
        return  await cls.main(file_path=file_path, password=password)#

