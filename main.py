from flask import Flask, request, jsonify, redirect
from data_utils import seats_scraper,updated_time, time_difference, clean_dept_name
from pymongo import MongoClient
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# MongoDB Atlas connection

client = MongoClient(os.environ['MONGO_URL'])
db = client['extension']  # Replace with your database name
collection = db['class_data']  # Replace with your collection name
print('Connected to MongoDB Atlas')
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.json  # Clear the collection before storing new data
        data = seats_scraper(data)
        data = updated_time(data)
        data = clean_dept_name(data)

        #get previous data from mongodb and update seats for the crn if already there
        previous_data = list(collection.find({}, {'_id': 0}))
        for course in data:
            res=list(collection.find({"crn": course['crn']}))
            if len(res)>0:
                result=collection.update_one({"crn": course['crn']}, {"$set": {"seats": course['seats'],"time_updated": course['time_updated'],"availability":course['availability']},})
            else:
                result=collection.insert_one(course)

        return jsonify({"status": "success", "message": "Data stored successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/get_data', methods=['GET'])
def get_data():

    data = list(collection.find({}, {'_id': 0}))
    data = time_difference(data)
    return jsonify(data), 200

@app.route('/dept=<department>', methods=['GET'])
def get_department_data(department):
    try:
        data = list(collection.find({"department": department}, {'_id': 0}))
        data = time_difference(data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "Department not found"}), 404

@app.route('/crn=<crn>', methods=['GET'])
def get_crn_data(crn):
    try:
        data = list(collection.find({"crn": crn}, {'_id': 0}))[0]
        data = time_difference([data])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "CRN not found"}), 404

@app.route('/course_num=<course_num>', methods=['GET'])
def get_course_data(course_num):
    try:
        data = list(collection.find({"course_num": course_num}, {'_id': 0}))
        data = time_difference(data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "Course not found"}), 404

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": "error", "message": "Page not found"}), 404

@app.route('/')
def index():
    return redirect("/get_data", code=302) # Redirect to /get_data endpoint



if __name__ == '__main__':
    app.run(debug=True)
