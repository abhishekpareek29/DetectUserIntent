from flask_api import FlaskAPI
import clf
from flask import request

app = FlaskAPI(__name__)


@app.route('/lndl', methods=['GET'])
def result():
    return clf.DL_prediction_str(request.args.get('q'))
