from stack import Stack
from flip_dir import flip_dir

import requests
import time

endpoints = {
    'init': "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/",
    'move': "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
    'take': "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/",
    'drop': 'https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/'
}
