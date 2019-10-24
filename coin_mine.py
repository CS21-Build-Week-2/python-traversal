"""
POST Mine endpoint:  https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/
BODY: {"proof":new_proof}'

GET Last proof endpoint: https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/
"""


"""
    What last proof returns:

{
    "proof": 42424410090804,
    "difficulty": 6,
    "cooldown": 1.0,
    "messages": [],
    "errors": []
}
"""

import hashlib
import requests
import random

endpoints = {
    "mine": "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/",
    "proof": "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/"
}

token = "Token 5859b714ecceab7b49085ecf1222f2adc318b86e"
proof = 0
r = requests.get(url=endpoints['proof'], headers={"Authorization": token})
data = r.json()

last_proof = data['proof']
difficulty_zeros = data['difficulty']

guess = f"{last_proof}{proof}".encode()
# print(guess)

guess_hash = hashlib.sha256(guess).hexdigest()
print(guess_hash)

zeros = "0" * difficulty_zeros
# print(zeros)
# print(type(zeros))

while guess_hash[:difficulty_zeros] != zeros:
    proof = random.randint(1, 99000000000000)
    new_guess = f"{last_proof}{proof}".encode()
    guess_hash = hashlib.sha256(new_guess).hexdigest()

r = requests.post(url=endpoints['mine'], json={"proof": proof}, headers={"Authorization": token})
data = r.json()
print(proof)
print(f"\n{data}")