import flask
import flask_restful
from flask_cors import CORS
import os


if __name__ == "__main__":
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)
    CORS(app)
    
    class RunHAS(flask_restful.Resource):
        def post(self):
            data = flask.request.get_json()
            if data:
                config_path = data.get("config")
                if config_path:
                    status = os.system("python /home/has/src/has_controller.py --config {}".format(config_path))
                    if status:
                        return 500, "Errors while running this command."
                    return 200, "Done Successfully"
                else:
                    return 400, "No config Specified."
            else:
                return 400, "No Data."
    api.add_resource(RunHAS, "/run")
    app.run(host=host, port=7000)
