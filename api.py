from flask import Flask, jsonify, request
from data_collection.rest_api_utils import get_user_info
# from model.model import train, load_model, predict
import json

app = Flask(__name__)

@app.route('/recommend/<int:userid>', methods = ['GET'])
def get_recommendations_for_user(userid):
    # return jsonify({"movies": [userid, userid+5, userid+309]})
    # checking we can access the util functions in data_collection
    return json.dumps(get_user_info(userid))
    # model = load_model()
    # random.seed(int(time.time()))
    # print(predict(userid="1", model=model))

# driver function
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=8083)