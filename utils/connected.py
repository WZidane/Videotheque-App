from flask import request, jsonify
import requests

def isConnected():
    query = f"http://host.docker.internal:5001/api/isconnected/"

    token = request.cookies.get("filmotek_tk")

    if(token != None):
        response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        return response.json()
    else:
        return jsonify({"isConnected": False}), 200