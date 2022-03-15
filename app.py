from flask import Flask,jsonify
import json
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_serialize import FlaskSerialize

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
fs_mixin = FlaskSerialize(db)

class Insertdata(fs_mixin,db.Model):
	timestamp = db.Column(db.String, default = datetime.utcnow)
	value = db.Column(db.Integer,primary_key = True)

	__fs_create_fields__ = __fs_update_fields__ = ['timestamp', 'value']

	def __repr__(self):
		return f"Insertdata('{self.timestamp}','{self.value}')"

@app.route('/')
def index():
    return 'Warm Welcome'

@app.route('/api/insert', methods = ['GET'])
def para():
	timestamp = request.args.get('timestamp',type= str)
	value = request.args.get('value',type = int)
	data = Insertdata(timestamp = timestamp, value=value)
	db.create_all()
	db.session.add(data)
	db.session.commit()
	return '200'

@app.route('/api/graph')
def apires():
		result = Insertdata.query.order_by(Insertdata.timestamp).all()
		return jsonify(Insertdata.fs_dict_list(result))



	#print(timestamp,value)	

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

