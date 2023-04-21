from flask import Flask
from flask import request, jsonify
import urllib.request, json
import redis
r = redis.Redis(host='localhost', port=6379,charset="utf-8", decode_responses=True)

app = Flask(__name__)

@app.route('/summary', methods=['POST'])#Retona el due de los paises con amount de parametro
def total_orders():
    data = request.get_json()
    if not data:
        return jsonify(error="request body cannot be empty"), 400
    print(data)
    #orders = json.loads(data)
    total = 0
    for order in data:
        print(order['id'])    
        country = order['country']
        amount = int(order['amount'])
        tax = get_tax_from_api(country)
        print(amount, tax)
        total += amount * tax
    return jsonify(total_due=total), 200

def get_tax_from_api(country):
    url = "http://127.0.0.1:5000/tax?country={}".format(country)

    data = r.hgetall(country+"1")
    if data:
        print("With Redis")
        return int(data["Tax"])
        
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    data = r.hgetall(country+"1")
    if not data:#Guardar data primera llamada, verifica si existe en redis
        r.hset(country+"1", mapping={
            "Country": dict["Country"],
            "Tax": int(dict["Tax"]),
        })

    return int(dict["Tax"])

if __name__ == "__main__":
    app.run(debug=True, port=3000)


# TODO: Handle errors properly.