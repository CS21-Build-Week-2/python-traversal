from stack import Stack
from flip_dir import flip_dir

import requests
import time
import os

endpoints = {
    'init': "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/",
    'move': "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
    'take': "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/",
    'drop': 'https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/'
}


# Goal is to visit all 500 rooms
# We need to store room information somewhere. With python, we can use the open() function
# use the stack to back-track in the graph. when we move in a direction, push the opposite direction to the stack
# keep track of the cooldown as well, use time.sleep() for that

r = requests.get(url=endpoints['init'], headers={
                 "Authorization": "Token 5859b714ecceab7b49085ecf1222f2adc318b86e"})

data = r.json()

room = f"Room_ID: {data['room_id']}, Coordinates: {data['coordinates']}, Title: {data['title']}, Description: {data['description']},"

f = open('rooms.txt', 'a+')
f.write(f"\n{room}")
f.close()

cooldown = data['cooldown']
