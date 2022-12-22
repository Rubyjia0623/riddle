from flask import Flask, render_template, request, make_response, jsonify
import random

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("riddle.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req.get("queryResult").get("action")
    info = ""
    if(action == "keywordchoice"):
        keyword = req.get("queryResult").get("parameters").get("keyword")
        collection_ref = db.collection("riddle")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if keyword in dict["sort"]:
                result += "題目：" + dict["Question"] + "\n"
                result += "答案：" + dict["Answer"] + "\n"
                result += "相關資料：" + dict["Explanation"] + "\n"
                result += "連結：" + dict["Link"] + "\n"
        info += result
    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run()
