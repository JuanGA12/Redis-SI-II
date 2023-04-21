from flask import Flask
from flask import request, jsonify
from flask_mongoengine import MongoEngine

import redis
r = redis.Redis(host='localhost', port=6379,charset="utf-8", decode_responses=True)

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'taxes',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

@app.route('/tax')
def tax_by_country():
    country_arg = request.args.get('country')
    #print(country_arg)
    #for tax in Tax.objects:
    #    print(tax.country)
    #   print(tax.value)

     
    data = r.hgetall(country_arg)
    if data:
        print("With Redis")
        return{
            "Country":data["Country"],
            "Tax":data["Tax"]
        }

    db_tax = Tax.objects(country=country_arg).first()
    if not db_tax:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(db_tax.to_json())

class Tax(db.Document):
    country = db.StringField()
    value = db.StringField()
    def to_json(self):
        data = r.hgetall(self.country)
        if not data:#Guardar data primera llamada, verifica si existe en redis
            r.hset(self.country, mapping={
                "Country": self.country,
                "Tax": self.value,
            })
        return {"Country": self.country,
                "Tax": self.value}

if __name__ == "__main__":
    app.run(debug=True, port=5000)

# readme 
# pip install flask
# pip install flask-mongoengine
###
#Schema MongoDB:
#{
#  "_id": {
#    "$oid": "644093d44100e8d352e8ee06"
#  },
#  "country": "BR",
#  "value": 11
#}
###