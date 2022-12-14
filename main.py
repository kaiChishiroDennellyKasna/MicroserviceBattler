
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
from flask import Flask, request
import random
import logging
import os
request = """{
    "_links": {
        "self": {
            "href": "https://YOUR_SERVICE_URL"
        }
    },
    "arena": {
        "dims": [4, 3], // width, height
        "state": {
            "https://A_PLAYERS_URL": {
                "x": 0,
                "y": 0,
                "direction": "N"
                "wasHit": false,
                "score": 0
            }
        }
    }
}"""


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']


@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"


@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)
    return moves[random.randrange(len(moves))]


if __name__ == "__main__":
    gameState = json.loads(request)
    print(gameState)
    # app.run(debug=False, host='0.0.0.0',
    #         port=int(os.environ.get('PORT', 8080)))
