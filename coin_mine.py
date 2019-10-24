"""
POST Mine endpoint:  https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/
BODY: {"proof":new_proof}'

GET Last proof endpoint: https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/
"""

import hashlib
import requests

token = "Token 5859b714ecceab7b49085ecf1222f2adc318b86e"