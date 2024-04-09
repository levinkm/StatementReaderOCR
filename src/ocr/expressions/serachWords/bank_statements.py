
class SearchKeywords:
    ''' 
    A class containing lists of keywords for searching titles in the DataFrame.
    '''
    date_keywords = ["date", "time"]
    description_keywords = ["desc", "details", "description", "info", "summary", "Details"]
    reference_keywords = ["ref", "reference", "receiptno", "transaction_id", "invoice_no"]
    debit_keywords = ["debit", "withdraw", "expense", "outflow","out"]
    credit_keywords = ["credit", "deposit", "income", "inflow","in"]
    balance = ['balance']