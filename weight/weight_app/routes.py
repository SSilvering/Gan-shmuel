
from weight_app import weight_app, requests, GETweight
from time import gmtime, strftime
from datetime import datetime
from flask import request, jsonify, render_template
import mysql.connector
from . import weight_app
from .GETweight import GETweight
from .db_module import DB_Module
import csv,json


@weight_app.route('/')
@weight_app.route('/index')
def index():
    return render_template('index.html')


@weight_app.route('/health', methods=['GET'])
def health_check():
    #a tuple of the all the apis that will be used in the project 
    api_tuple = ("index","batch-weight","unknown","item","session","post","weight")
    for item in api_tuple:
        uri = f"http://localhost:8080/{item}"
        req = requests.get(uri)
        print(req.status_code)
        if req.status_code < 200 or req.status_code > 299:
            res = f"APP Status is {req.status_code}"
            return res
    return f"APP status is {req.status_code}"
    

@weight_app.route('/session')
@weight_app.route('/session/<id>')
def get_session(id="<id>"):
    if id is not None:
        #select_query = f"SELECT id, trucks_id, bruto, neto FROM sessions where trucks_id={id}"
         
        select_query = f"SELECT t1.id, t1.trucks_id, t1.bruto, t1.neto, t2.weight FROM sessions t1, trucks t2 WHERE t1.trucks_id = {id} and t1.trucks_id = t2.truckid"
        tags = ('id', 'trucks_id', 'bruto', 'neto')
        db = DB_Module ()
        data = db.fetch_new_data(select_query)
        print(type(data))
        session = dict()
        for ind in range(0, len(data)):
            session[tags[ind]] = data[ind]
        return json.dumps(session)
    return "provide a truck ID"


@weight_app.route('/weight', methods=['GET'])
def GETweight_startup():
    currenttime = strftime("%Y%m%d%H%M%S", gmtime())
    start_of_day = strftime("%Y%m%d000000", gmtime())
    from_time = request.args.get('from', default = start_of_day, type = str)
    to_time = request.args.get('to', default = currenttime, type = str)
    filter_type = request.args.get('filter', default = '*', type = str)
    db_name = db #needs assignment
    get_weight(from_time,to_time,filter_type,db_name)
    return GETweight(from_time,to_time,filter_type,db_name)
    #return "Hello from GET/weight!"



@weight_app.route('/item')
def get_only_item():
    return "Hello from Item!"
@weight_app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):

    from_time = request.args.get('from')
    to_time = request.args.get('to')

    data = []
    session = { #basic mold for the return object
        "id":int(item_id),
        "tara":0,
        "sessions":[]
    }

    if not from_time: #default cases for time 
        from_time = datetime.now().strftime("%Y%m01000000")
    if not to_time:
        to_time = datetime.now().strftime("%Y%m%d%H%M%S")

    query = f"SELECT bruto,neto,id,date FROM sessions WHERE id={item_id} AND date BETWEEN {from_time} AND {to_time}"

    try:
        db = DB_Module ()
        data = db.fetch_new_data(query)
    except:
        print ("mysql has failed to reach the server..")

    
    if not data: #error case 
        session["id"] = 404,
        session["tara"] = 'N/A'

    for ind in range(0, len(data)):
        session["tara"] += float(data[ind]["bruto"]) - float(data[ind]["neto"])
        session["sessions"].append(data[ind]["id"])

    return jsonify(session)

@weight_app.route('/batch-weight', methods=['POST'])
def batch_weight():

    filepath = '/home/niv/Documents/Gan-Shmuel/weight/weight_app/in/containers2.csv'
    # filepath = '/home/niv/Documents/Gan-Shmuel/weight/weight_app/in/containers3.json'
    query_list = []
    data = []
    is_csv = False
    
    try: 
        db = DB_Module ()
        data = db.fetch_new_data(query)
    except:
        return "Failed to connect to database"

    with open(filepath,'r') as my_file: #case if it's JSON
        try:
            data = json.load(my_file)
        except:
            is_csv = True

    
    if is_csv: #case if it's CSV
        with open(filepath,'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:
                _id = list(line.values())[0]
                weight = list(line.values())[1]
                unit = list(line.keys())[1]

                query = f"INSERT INTO containers (id,weight,unit) VALUES ({_id},{weight},{unit})"
                query_list.append(query)
    
    #execute queries

    return "FUCK"
    
