import requests
import json
from rmaruyam_def_4_comrun import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

auth_token = get_token(DNAC_URL, DNAC_USER, DNAC_PASSWORD)
command_runner(auth_token, DNAC_URI)
