
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# EXAMPLE REquest
import json
from re import S
from flask import Flask, request
import random
import logging
import os
# request = """{
#     "_links": {
#         "self": {
#             "href": "https://A_PLAYERS_URL1"
#         }
#     },
#     "arena": {
#         "dims": [4, 3],
#         "state": {
#             "https://A_PLAYERS_URL1": {
#                 "x": 0,
#                 "y": 1,
#                 "direction": "E",
#                 "wasHit": false,
#                 "score": 0
#             },
#              "https://A_PLAYERS_URL2": {
#                 "x": 1,
#                 "y": 1,
#                 "direction": "W",
#                 "wasHit": false,
#                 "score": 0
#             },
#              "https://A_PLAYERS_URL3": {
#                 "x": 2,
#                 "y": 2,
#                 "direction": "W",
#                 "wasHit": false,
#                 "score": 0
#             }
#         }
#     }
# }"""

arenaDims = None

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

# app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']


@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"


@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)
    return moves[random.randrange(len(moves))]


def calulateDangermap(dangerMap, xLocation, yLocation, direction):
    height = len(dangerMap)-1
    width = len(dangerMap[0])-1
    if direction == "N":
        dangerMap[xLocation][yLocation] = "D"
        oneAbove = yLocation-1
        twoAbove = yLocation-2
        threeAbove = yLocation-3
        fourAbove = yLocation-3
        if oneAbove >= 0:
            dangerMap[oneAbove][xLocation] = "D"
        if twoAbove >= 0:
            dangerMap[twoAbove][xLocation] = "D"
        if threeAbove >= 0:
            dangerMap[threeAbove][xLocation] = "D"
        if fourAbove >= 0:
            dangerMap[fourAbove][xLocation] = "P"
    if direction == "S":
        dangerMap[xLocation][yLocation] = "D"
        oneAbove = yLocation+1
        twoAbove = yLocation+2
        threeAbove = yLocation+3
        fourAbove = yLocation+4

        if oneAbove <= height:
            dangerMap[oneAbove][xLocation] = "D"
        if twoAbove <= height:
            dangerMap[twoAbove][xLocation] = "D"
        if threeAbove <= height:
            dangerMap[threeAbove][xLocation] = "D"
        if fourAbove <= height:
            dangerMap[fourAbove][xLocation] = "P"
    if direction == "E":
        dangerMap[xLocation][yLocation] = "D"
        oneAbove = xLocation+1
        twoAbove = xLocation+2
        threeAbove = xLocation+3
        fourAbove = xLocation+4
        if oneAbove <= width:
            dangerMap[yLocation][oneAbove] = "D"
        if twoAbove <= width:
            dangerMap[yLocation][twoAbove] = "D"
        if threeAbove <= width:
            dangerMap[yLocation][threeAbove] = "D"
        if fourAbove <= width:
            dangerMap[yLocation][fourAbove] = "P"
    if direction == "W":
        dangerMap[xLocation][yLocation] = "D"
        oneAbove = xLocation-1
        twoAbove = xLocation-2
        threeAbove = xLocation-3
        fourAbove = xLocation-4
        if oneAbove >= 0:
            dangerMap[yLocation][oneAbove] = "D"
        if twoAbove >= 0:
            dangerMap[yLocation][twoAbove] = "D"
        if threeAbove >= 0:
            dangerMap[yLocation][threeAbove] = "D"
        if fourAbove >= 0:
            dangerMap[yLocation][fourAbove] = "P"
    return dangerMap


def getGameInfo(request):
    player1ID = gameState["_links"]["self"]["href"]
    arenaDims = gameState["arena"]["dims"]
    dangerMap = [[0]*arenaDims[0] for _ in range(arenaDims[1])]
    arena = [[0]*arenaDims[0] for _ in range(arenaDims[1])]
    print(arena)
    for player in gameState["arena"]["state"]:
        # print(gameState["arena"]["state"][player])
        Xcoord = gameState["arena"]["state"][player]["x"]
        Ycoord = gameState["arena"]["state"][player]["y"]
        if player != player1ID:
            arena[Xcoord][Ycoord] = gameState["arena"]["state"][player]["direction"]
            calulateDangermap(dangerMap, Xcoord, Ycoord,
                              gameState["arena"]["state"][player]["direction"])
        else:
            playerDetails = [Xcoord, Ycoord, gameState["arena"]
                             ["state"][player]["direction"]]

    return arena, dangerMap, playerDetails


def checkForTarget(arenaState, playerDetails):
    targetAhead = False
    targetDistance = 0
    height = len(arenaState)-1
    width = len(arenaState[0])-1
    direction = playerDetails[2]
    xLocation = playerDetails[0]
    yLocation = playerDetails[1]
    if direction == "N":
        oneAbove = yLocation-1
        twoAbove = yLocation-2
        threeAbove = yLocation-3
        if oneAbove >= 0:
            if arenaState[oneAbove][xLocation] != 0:
                targetAhead = True
                targetDistance = 1
        if twoAbove >= 0:
            if arenaState[twoAbove][xLocation] != 0:
                targetAhead = True
                targetDistance = 2
        if threeAbove >= 0:
            if arenaState[threeAbove][xLocation] != 0:
                targetAhead = True
                targetDistance = 3
    if direction == "S":
        oneAbove = yLocation+1
        twoAbove = yLocation+2
        threeAbove = yLocation+3
        if oneAbove <= height:
            if arenaState[oneAbove][xLocation] != 0:
                targetAhead = True
                targetDistance = 1
        if twoAbove <= height:
            if arenaState[twoAbove][xLocation] != 0:
                targetAhead = True
                targetDistance = 2
        if threeAbove <= height:
            if arenaState[threeAbove][xLocation] != 0:
                targetAhead = True
                targetDistance = 3
    if direction == "E":
        oneAbove = xLocation-1
        twoAbove = xLocation-2
        threeAbove = xLocation-3
        if oneAbove >= 0:
            if arenaState[yLocation][oneAbove] != 0:
                targetAhead = True
                targetDistance = 1
        if twoAbove >= 0:
            if arenaState[yLocation][twoAbove] != 0:
                targetAhead = True
                targetDistance = 2
        if threeAbove >= 0:
            if arenaState[yLocation][threeAbove] != 0:
                targetAhead = True
                targetDistance = 3
    if direction == "W":
        oneAbove = xLocation+1
        twoAbove = xLocation+2
        threeAbove = xLocation+3
        if oneAbove <= width:
            if arenaState[yLocation][oneAbove] != 0:
                targetAhead = True
                targetDistance = 1
        if twoAbove <= width:
            if arenaState[yLocation][twoAbove] != 0:
                targetAhead = True
                targetDistance = 2
        if threeAbove <= width:
            if arenaState[yLocation][threeAbove] != 0:
                targetAhead = True
                targetDistance = 3
    # print(targetAhead, targetDistance)
    return targetAhead, targetDistance


def calcNextMove(arenaState, dangerState, playerDetails):
    inDanger = False
    inFutureDanger = False
    targetAvailable = False
    targetDistance = 0
    # print(dangerState[playerDetails[1]][playerDetails[0]])
    if dangerState[playerDetails[1]][playerDetails[0]] == "D":
        inDanger = True
    if dangerState[playerDetails[1]][playerDetails[0]] == "P":
        inFutureDanger = True
    targetAvailable, targetDistance = checkForTarget(arenaState, playerDetails)

    return inFutureDanger, inDanger, targetAvailable, targetDistance


def calcSafeMove(inFutureDanger, inDanger, arenaState, dangerState, playerDetails):
    print("Hauling ass")
    height = len(arenaState)-1
    width = len(arenaState[0])-1
    # print(playerDetails[2])
    safeMove = False
    facingEdge = False
    # South
    # print(dangerState)
    # dangerstate and arena state are y, x
    # print(playerDetails)
    # South
    if playerDetails[2] == "S":
        if playerDetails[1]+1 <= height:
            if dangerState[playerDetails[1]][playerDetails[0]] == 0:
                # print("South safe")
                safeMove = True

        if playerDetails[1] == height:
            # print("South Edge")
            facingEdge = True
    # North
    if playerDetails[2] == "N":
        if playerDetails[1]-1 >= 0:
            if dangerState[playerDetails[1]-1][playerDetails[0]] == 0:
                print("North safe")
                safeMove = True
        if playerDetails[1] == 0:
            # print("North Edge")
            facingEdge = True
    # East
    if playerDetails[2] == "E":
        if playerDetails[0]+1 <= width:
            if dangerState[playerDetails[1]][playerDetails[0]+1] == 0:
                # print("East safe")
                safeMove = True

        if playerDetails[0] == 0:
            # print("East Edge")
            facingEdge = True

    # West
    if playerDetails[2] == "W":
        if playerDetails[0]-1 >= 0:
            if dangerState[playerDetails[1]][playerDetails[0]-1] == 0:
                # print("West safe")
                safeMove = True
        if playerDetails[0] == width:
            # print("East Edge")
            facingEdge = True

    return safeMove, facingEdge


if __name__ == "__main__":

    gameState = json.loads(request)
    arenaState, dangerState, playerDetails = getGameInfo(gameState)
    inFutureDanger, inDanger, targetAvailable, targetDistance = calcNextMove(
        arenaState, dangerState, playerDetails)
    isMoveSafe, onEdge = calcSafeMove(inFutureDanger, inDanger,
                                      arenaState, dangerState, playerDetails)

    print("Am I in Danger: ", inDanger)
    print("Will moving make me safe: ", isMoveSafe)
    print("Am I facing an edge: ", onEdge)

    print("Is there a target: ", targetAvailable)
    if targetAvailable:
        print("Target is ", targetDistance, " distance away")

    # If in danger move?
    # Check which surrounding squares are safe
    # Calculate potential moves?
# if __name__ == "__main__":
#     gameState = json.loads(request)
#     print(gameState)
#     app.run(debug=False, host='0.0.0.0',
#             port=int(os.environ.get('PORT', 8080)))