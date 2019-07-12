import requests
import json
from rmaruyam_def_1_deviceconfigbyid_text import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

auth_token = get_token(DNAC_URL, DNAC_USER, DNAC_PASSWORD)
get_deviceconfigbyid(auth_token, DNAC_URI)
