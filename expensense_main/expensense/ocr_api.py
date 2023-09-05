import json
import requests
import re
from datetime import datetime

def read_ocr_key():
    """ Method to read OCR Key from the ocr_key file"""
    ocr_api_key = None
    try:
        with open('ocr.key', 'r') as f:
            ocr_api_key = f.readline().strip()
    except:
        try:
            with open('../ocr.key', 'r') as f:
                ocr_api_key = f.readline().strip()
        except:
            raise IOError('ocr.key file not found')
    
    if not ocr_api_key:
        raise KeyError('OCR Key not found')
    
    return ocr_api_key

def post_query_to_ocr(receipt, engine=1):
    """ Method to post the image to the API """
    api_key = read_ocr_key()
    is_table = True
    payload = {'istable': is_table,
               'apikey':api_key}
    endpoint = 'https://api.ocr.space/parse/image'

    if engine in [2,3]:
        payload['OCREngine']=engine

    with open(receipt, 'rb') as f:
        response = requests.post(endpoint,files={receipt: f},
                                 data=payload)
    return response.content.decode()


def find_amount(string):
    """ Method to find Amount from a string using regex """

    # "AMOUNT," "Amount," "amount," "Total," "total," or "TOTAL"
    amount_pattern = r'(?i)\b(?:AMOUNT|Amount|amount|Total|TOTAL|total)\s+(\d+(\.\d{1,2})?)\b'
    
    # Find the pattern using regular expression
    match = re.search(amount_pattern, string)

    if match:
        amount = float(match.group(1))
        return amount
    else:
        return None

def find_date(string):
    """ Method to find date from a string using regex """
    date_pattern_1 = r'(\b\d{2}[/-]\d{2}[/-]\d{4}\b)'  # DD/MM/YYYY or DD-MM-YYYY
    date_pattern_2 = r'(\b\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\b)'  # 01 Jan 2018 (e.g., 01 Jan 2018 or 1 Jan 2018)

    # Find dates using regular expressions
    match1 = re.findall(date_pattern_1, string)
    match2 = re.findall(date_pattern_2, string)

    #for pattern 1
    if match1:
        pattern = r'(\d{2})[/\-](\d{2})[/\-](\d{4})'
        match = re.search(pattern, match1[0])
        if match:
            # Extract day, month, and year from the regex match
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3))

            return day, month, year
    else:
        # Return None if no match is found
        return 0,0,0

    #for pattern 2
    if match2:
        date_format = "%d %b %Y"
        parsed_date = datetime.strptime(match2, date_format)
        day = parsed_date.day
        month = parsed_date.month
        year = parsed_date.year
        return day, month, year
    else:
        return 0,0,0

def process_data(data, engine):
        """ Method to process the amount and date data"""
        if data['OCRExitCode'] == 1:
            amt_data = data['ParsedResults'][0]['ParsedText']
            amount = find_amount(amt_data) or 0
            day, month, year = find_date(data['ParsedResults'][0]['ParsedText'])
            return {
                "amount": amount,
                "date": {
                    "day": day,
                    "month": month,
                    "year": year,
                }
            }
        else:
            print(f'Trying with OCREngine{engine}')
            return None

def results(receipt):
    """ Method to return result of the OCR API"""

    engines_to_try = [1, 2, 3]
    
    for engine in engines_to_try:
        #call the three engines is result is not found
        data = json.loads(post_query_to_ocr(receipt, engine))
        
        if data['OCRExitCode']:
            result = process_data(data, engine)
            if result:
                return json.dumps(result)

    return json.dumps({'error': 'partial parse'})


