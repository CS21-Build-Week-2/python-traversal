"""
CREDIT TO CHARLES GODOY
"""

import json
import time
import requests

URL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/'
HEADERS = {'Authorization': 'Token 5859b714ecceab7b49085ecf1222f2adc318b86e', 'Content-Type': 'application/json'}
MAP = {}
CURRENT_ROOM = 0
ROOM_INFO = {}  # a dictionary of room info

def init():
    r = requests.get(URL + 'init/', headers=HEADERS)
    out = r.json()
    print(json.dumps(out, indent=2))
    current_room = out['room_id']
    MAP[current_room] = {e: '?' for e in out['exits']}
    global CURRENT_ROOM
    CURRENT_ROOM = current_room
    ROOM_INFO[current_room] = dict(out)

def move(direction):
    body = {'direction': direction}
    r = requests.post(URL + 'move/', data=json.dumps(body), headers=HEADERS)
    # r = requests.post(URL + 'fly/', data=json.dumps(body), headers=HEADERS)
    out = r.json()
    print(json.dumps(out, indent=2))
    global CURRENT_ROOM
    new_room = out['room_id']
    if MAP[CURRENT_ROOM][direction] == '?':  # not yet visited
        MAP[new_room] = {e: '?' for e in out['exits']}
    MAP[CURRENT_ROOM][direction] = new_room
    CURRENT_ROOM = new_room
    ROOM_INFO[new_room] = dict(out)
    return out

def take_or_pick_or_sell_treasure(cmd):
    body = {'name': 'treasure'}
    r = requests.post(URL + cmd + '/', data=json.dumps(body), headers=HEADERS)
    out = r.json()
    print(json.dumps(out, indent=2))

def sell():
    take_or_pick_or_sell_treasure('sell')
    body = {'name': 'treasure', 'confirm': 'yes'}
    r = requests.post(URL + 'sell/', data=json.dumps(body), headers=HEADERS)
    out = r.json()
    print(json.dumps(out, indent=2))

def status():
    r = requests.post(URL + 'status/', headers=HEADERS)
    out = r.json()
    print(json.dumps(out, indent=2))

def change_name():
    body = {'name': 'Joker'}
    r = requests.post(URL + 'change_name/', data=json.dumps(body), headers=HEADERS)
    out = r.json()
    print(json.dumps(out, indent=2))

def pray():
    r = requests.post(URL + 'pray/', headers=HEADERS)
    out = r.json()
    print(json.dumps(out, indent=2))

init()
time.sleep(1)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        out = move(cmds[0])
        print("cooldown for", out['cooldown'], 's')
        time.sleep(out['cooldown'])
    elif cmds[0] == 'm':
        print(MAP)
    elif cmds[0] == 't':
        take_or_pick_or_sell_treasure('take')
        print("cooldown for", out['cooldown'], 's')
        time.sleep(out['cooldown'])
    elif cmds[0] == 'd':
        take_or_pick_or_sell_treasure('drop')
    elif cmds[0] == 'sell':
        sell()
    elif cmds[0] == 'status':
        status()
    elif cmds[0] == 'name':
        change_name()
    elif cmds[0] == 'pray':
        pray()
    else:
        print("I did not understand that command.")