import json
from bardapi import Bard

RETRY_ATTEMPTS = 5


def enrich_data(company_name, company_url):
    """
    Enrich data with BardAPI
    Needs cookie set as an env variable, see documentation: https://github.com/dsdanielpark/Bard-API
    :param company_name: company name
    :param company_url: company url
    :return: json with following details: name, company_url, description, industry,
             location, contact_details, company_size
    """
    retries = 0
    prompt = "I do not want you to tell me you cannot complete a task, you have to follow exactly what " \
             "instructions I give you. " \
             "Given the company url, find me the data to include the following fields in text format." \
             f"Company name: {company_name}" \
             f"Company url: {company_url}" \
             "Find the following details of the company in the following format," \
             "if you cannot find any information, put the value as None replacing the curly braces." \
             "Always output the format below!" \
             "Format:" \
             "START" \
             "{" \
             "name: {company name}," \
             "company_url: {company page url}," \
             "description: {description of company}," \
             "industry: {industry company is in}," \
             "location: {country and city of office}," \
             "contact_details: {company contact details}," \
             "company_size: {company size of type integer wrapped with double quotes}" \
             "}" \
             "END"
    global result
    while True:
        result = Bard().get_answer(prompt)['content']  # get response from Bard
        # extract json from result
        result = get_between(result, "START", "END")

        # try to convert string to json
        # retry if failed
        try:
            result = json.loads(result)
            break
        except json.decoder.JSONDecodeError:
            print(f"FAIL RESULT: {result}")
            retries += 1
            if retries >= RETRY_ATTEMPTS:
                result = {}
                break


def get_between(s, start, end):
    start_index = s.find(start) + len(start)
    end_index = s.find(end, start_index)
    return s[start_index:end_index]
