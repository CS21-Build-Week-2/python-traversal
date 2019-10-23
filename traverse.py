from stack import Stack
from flip_dir import flip_dir

import requests
import time
import os
import random

endpoints = {
    'init': "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/",
    'move': "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
    'take': "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/",
    'drop': 'https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/',
    'sell': 'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/'
}

token = 'Token 5859b714ecceab7b49085ecf1222f2adc318b86e'

# Goal is to visit all 500 rooms
# We need to store room information somewhere. With python, we can use the open() function
# use the stack to back-track in the graph. when we move in a direction, push the opposite direction to the stack
# keep track of the cooldown as well, use time.sleep() for that

r = requests.get(url=endpoints['init'], headers={
                 "Authorization": "Token "})

data = r.json()

room = f"Room_ID: {data['room_id']}, Coordinates: {data['coordinates']}, Title: {data['title']}, Description: {data['description']}, Messages: {data['messages']}, Items: {data['items']}"

# with open('rooms.txt', 'a+') as f:
#     f.write(f"{room}\n")

cooldown = 15
visited_rooms = {}
moves = Stack()
room_x = int(f"{data['coordinates'][1]}{data['coordinates'][2]}")
room_y = int(f"{data['coordinates'][4]}{data['coordinates'][5]}")
# room_coords = (room_x, room_y)

visited_rooms[f"({room_x},{room_y})"] = room

# Amount of rooms is confirmed to be 500
while len(visited_rooms) < 500:
    # time.sleep(cooldown)
    # print(visited_rooms)
    room_x = int(f"{data['coordinates'][1]}{data['coordinates'][2]}")
    room_y = int(f"{data['coordinates'][4]}{data['coordinates'][5]}")
    exit_directions = data['exits']
    items = data['items']
    cooldown = data['cooldown']

    # We want to pick up items if there are some
    if len(items) > 0:
        for item in items:
            r = requests.post(url=endpoints['take'], headers={
                              'Authorization': token}, json={"name": f'{item}'})
            print(f"Picked up item {item}")
            time.sleep(30)

    directions = []
    for exit in exit_directions:
        if exit is 'n':
            if f"({room_x},{room_y+1})" not in visited_rooms:
                directions.append('n')

        elif exit is 's':
            if f"({room_x},{room_y-1})" not in visited_rooms:
                directions.append('s')

        elif exit is 'w':
            if f"({room_x-1},{room_y})" not in visited_rooms:
                directions.append('w')

        elif exit is 'e':
            if f"({room_x+1},{room_y})" not in visited_rooms:
                directions.append('e')

    visited_rooms[data['coordinates']] = room

    if len(directions) is 0:
        time.sleep(30)
        d = moves.pop()
        r = requests.post(url=endpoints['move'], headers={
                          "Authorization": token}, json={'direction': d})
        data = r.json()
        room = f"Room_ID: {data['room_id']}, Coordinates: {data['coordinates']}, Title: {data['title']}, Description: {data['description']}, Messages: {data['messages']}, Items: {data['items']}"
        continue

    random.shuffle(directions)
    d = directions.pop()
    r = requests.post(url=endpoints['move'], headers={
                      "Authorization": token}, json={'direction': d})
    data = r.json()
    cooldown = data['cooldown']

    if len(data['errors']) > 0:
        for error in data['errors']:
            print(error)

        time.sleep(cooldown)
        r = requests.post(url=endpoints['move'], headers={
                          "Authorization": token}, json={'direction': d})
        data = r.json()
        room = f"Room_ID: {data['room_id']}, Coordinates: {data['coordinates']}, Title: {data['title']}, Description: {data['description']}, Messages: {data['messages']}, Items: {data['items']}"
        moves.push(flip_dir(d))
    else:
        time.sleep(cooldown)

    # data = r.json()
    # room = f"Room_ID: {data['room_id']}, Coordinates: {data['coordinates']}, Title: {data['title']}, Description: {data['description']}, Messages: {data['messages']}, Items: {data['items']}"
