from flask import Flask, render_template, request, Response
import waitress
from configparser import ConfigParser
import psycopg2
import threading
import time


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


class GalleryServer(threading.Thread):
    """Class for the Gallery server."""

    APP = 'GALLERY_SERVER'

    def __init__(self, host="localhost", port=8000, psql_config=None):
        self.host = host
        self.port = port
        self.psql_config = psql_config
        self._metadata = self._configure_metadata()
        self._app = self._configure_app()
        self._server = self._configure_server()
        super().__init__(target=self._server.run)

    def _configure_metadata(self):
        """Collect the metadata from the database."""
        query = '''SELECT id, name, description, small_data, medium_data FROM photos;'''
        results = database_query(self.psql_config, query)
        return {
            int(entry[0]) : {
                "name": str(entry[1]),
                "description": str(entry[2]),
                "small_data": bytes(entry[3]),
                "medium_data": bytes(entry[4])
            }
            for entry in results[0]
        }

    def _configure_app(self):
        """Setup the app."""

        app = Flask(self.APP)
        app.config['JSON_ADD_STATUS'] = False

        @app.route('/', methods=['GET', 'POST'])
        def home():
            document = render_template('index.html')
            document = document.replace("METADATA", self._javascript_metadata())
            return document

        @app.route('/photo/name', methods=['GET'])
        def name_photo_data():
            id = int(request.args.get("id"))
            resp = Response(self._metadata[id]["name"])
            resp.headers['Content-Type'] = 'text/plain'
            return resp

        @app.route('/photo/description', methods=['GET'])
        def desc_photo_data():
            id = int(request.args.get("id"))
            resp = Response(self._metadata[id]["description"])
            resp.headers['Content-Type'] = 'text/plain'
            return resp

        @app.route('/photo/small', methods=['GET'])
        def small_photo_data():
            id = int(request.args.get("id"))
            resp = Response(self._metadata[id]["small_data"])
            resp.headers['Content-Type'] = 'image/jpg'
            return resp

        @app.route('/photo/medium', methods=['GET'])
        def medium_photo_data():
            id = int(request.args.get("id"))
            resp = Response(self._metadata[id]["medium_data"])
            resp.headers['Content-Type'] = 'image/jpg'
            return resp

        return app

    def _configure_server(self):
        """Setup the server."""
        return waitress.create_server(self._app, host=self.host, port=self.port)

    def shutdown(self):
        """Graceful shutdown of the server."""
        if self.is_alive:
            self._server.close()
        self.join(timeout=2)

    def _javascript_metadata(self):
        """Arranges the metadata in a javascript array."""
        if not self._metadata.items():
            return "[]"
        js_data = ""
        for id, data in self._metadata.items():
            js_data += "{id:%i,name:'%s',description:'%s'}," % (id, data["name"], data["description"])
        return "[" + js_data[0:-1] + "]"


def main(config_file):
    """Read the config and start the server."""

    # Get server and postgresql config
    config = ConfigParser()
    config.read(config_file)
    server_config = dict(config.items("server"))
    (host, port) = server_config["host"], server_config["port"]
    psql_config = dict(config.items("postgresql"))

    # Start the server
    print("Starting server, host %s on port %s" % (host, port))
    server = GalleryServer(host, port, psql_config)
    server.start()

    # Stop the server
    flag = False
    while not flag:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down server.")
            flag = True
            server.shutdown()


if __name__ == "__main__":
    main(config_file="config.ini")
