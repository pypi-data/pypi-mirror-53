import os
import time
import datetime
import json
import requests

from .configuration import Configuration

from .fetchs import fetch_modelNew
from .fetchs import fetch_recomms


# main_url = 'http://localhost:8000/rest/'
# website = 'https://tasteguru.ai/rest/'
# token = 'D6MgtEveYlQWWdUxOochJlElGrtYpF'

# url_modelNew = '{0}modelNew/'.format(main_url)
# url_recomms = '{0}recomms/'.format(main_url)
# url_encode_feedback = '{0}encode-feedback/'.format(main_url)
# url_feedback = '{0}feedback/'.format(main_url)
# url_feedbackInfo = '{0}feedbackInfo/'.format(main_url)
# url_cancelSub = '{0}cancelSub/'.format(main_url)


name = 'example_pkg_name'