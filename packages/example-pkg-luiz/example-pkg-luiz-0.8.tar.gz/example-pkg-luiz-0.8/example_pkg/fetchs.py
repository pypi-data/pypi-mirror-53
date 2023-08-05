import os
import datetime
import time
import json
import requests
from .configuration import Configuration

# main_url = 'http://localhost:8000/rest/'
main_url = 'https://tasteguru.ai/rest/'

url_modelNew = '{0}modelNew/'.format(main_url)
url_recomms = '{0}recomms/'.format(main_url)
url_encode_feedback = '{0}encode-feedback/'.format(main_url)
url_feedback = '{0}feedback/'.format(main_url)
url_feedbackInfo = '{0}feedbackInfo/'.format(main_url)
url_cancelSub = '{0}cancelSub/'.format(main_url)

def fetch_modelNew(token):
    ## url_modelNew
    values = {}
    values['sour'] = 1
    values['carbonation'] = 0
    values['first'] = 0
    values['second'] = 1
    values['third'] = 2
    values['activity'] = 0 
    values['nonbeer'] = 0
    values['travel'] = 0
    values['stay'] = 0
    values['prefer'] = 0
    values['frequency'] = 0
    values['style'] = 0
    values['firstName'] = 'Luiz'
    values['lastName'] = 'Sato'
    values['email'] = 'luiz.sato@icloud.com'
    values['newsletter'] = True
    
    headers = {"Authorization": "Bearer {0}".format(token)}

    
    response = requests.post(url=url_modelNew, headers=headers, json=values)
    responseCode = response.status_code
    
    if responseCode == 200:
        return json.loads(response.content.decode('utf-8'))
    elif responseCode == 201:
        return json.loads(response.content.decode('utf-8'))
        # return '201'
    elif responseCode == 401:
        return 'Wrong Authentication'
    elif responseCode == 403:
        return 'Please contact Tasteguru, to get access to this URL'
    elif responseCode == 404:
        return 'NOT FOUND'
    elif responseCode == 405:
        return 'Method is not allowed'
    else:
        return None

def fetch_recomms():
    
    response = requests.post(url=url_recomms, headers=headers, json=values)
    responseCode = response.status_code
    
    if responseCode == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None