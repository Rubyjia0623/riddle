from flask import Flask, render_template, request, make_response, jsonify


import firebase_admin
import random
from firebase_admin import credentials, firestore
cred = credentials.Certificate("riddle.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req.get("queryResult").get("action")
    if(action == "keywordchoice"):
        keyword = req.get("queryResult").get("parameters").get("keyword");
        info = "您選擇的電影分級是:"+ keyword
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    return make_response(jsonify({"fulfillmentText": info}))



if __name__ == "__main__":
    app.run()

