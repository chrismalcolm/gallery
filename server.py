from flask import Flask, render_template, request, Response
import waitress
from configparser import ConfigParser
import psycopg2


def database_query(psql_config, query):
    """Executes the PostgreSQL database query and returns the results and any
    database errors."""
    results = None
    errors = list()
    try:
        conn = psycopg2.connect(**psql_config)
        cur = conn.cursor()

        cur.execute(query)
        results = cur.fetchall()
        cur.close()

    except psycopg2.DatabaseError as err:
        errors.append(str(err))

    finally:
        if conn is not None:
            conn.close()

    return results, errors


# Get postgresql config
config_file="config.ini"
config = ConfigParser()
config.read(config_file)
postgresql_config = dict(config.items("postgresql"))

query = '''SELECT id, name, description, small_data, medium_data FROM photos;'''
results = database_query(postgresql_config, query)


app = Flask(__name__)

metadata = dict()

for entry in results[0]:
    id = int(entry[0])
    metadata[id] = {
        "name": str(entry[1]),
        "description": str(entry[2]),
        "small_data": bytes(entry[3]),
        "medium_data": bytes(entry[4])
    }


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/photo/name', methods=['GET'])
def name_photo_data():
    id = int( request.args.get("id") )
    resp = Response(metadata[id]["name"])
    resp.headers['Content-Type'] = 'text/plain'
    return resp

@app.route('/photo/description', methods=['GET'])
def des_photo_data():
    id = int( request.args.get("id") )
    resp = Response(metadata[id]["description"])
    resp.headers['Content-Type'] = 'text/plain'
    return resp

@app.route('/photo/small', methods=['GET'])
def small_photo_data():
    id = int( request.args.get("id") )
    resp = Response(metadata[id]["small_data"])
    resp.headers['Content-Type'] = 'image/jpg'
    return resp

@app.route('/photo/medium', methods=['GET'])
def medium_photo_data():
    id = int(request.args.get("id"))
    resp = Response(metadata[id]["medium_data"])
    resp.headers['Content-Type'] = 'image/jpg'
    return resp

@app.route('/danger', methods=['GET'])
def okay():
    print(request.args)
    print(request.args.get("filename"))
    return render_template('upload.html')

server = waitress.create_server(app, host="localhost", port=8080)
server.run()
