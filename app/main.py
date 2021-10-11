from flask import Flask,jsonify,request
from flask.templating import render_template
from werkzeug.wrappers import response
from util.data import loadNewData,findData,getAllData
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = "util"
  
@app.route("/find-Data",methods=["POST"])
def home_view():
    email = request.get_json()
    if not email:
        return {"message" : "Data not found"},400
    if "email" not in email:
        return {"message" : "Data not found"},400

    response = findData(email["email"])
    
    if response == None :
        return {"message" : "Email not found"},400
    
    response["email"] = email["email"]
    response["message"] = "fetched success"

    return jsonify(response),200


@app.route("/update-data",methods=["GET","POST"])
def updateData():
    if request.method == "GET":
        return render_template("update.html")
    if request.method == "POST":
        
        if not request.form or not request.files:
            return {"message":"pass or file missing"},400

        if "password" not in request.form or "file" not in request.files:
            return {"message":"pass or file missing"},400

        if os.environ["password"] != request.form["password"]:
             return {"message":"password incorrect try again"},400

        if "file" in request.files:
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],"data.csv"))
    
        return jsonify(loadNewData()),200
    

@app.route("/awake",methods=["GET"])
def keepDynoAlive():
    return jsonify({"msg":"jago"}),200


@app.route("/getAll",methods=["POST"])
def getLeadrboard():
    return jsonify(getAllData())