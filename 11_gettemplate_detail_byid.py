import requests
import json
from rmaruyam_def_3_template import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

auth_token = get_token(DNAC_URL, DNAC_USER, DNAC_PASSWORD)
get_template_detail_byid(auth_token, DNAC_URI)
