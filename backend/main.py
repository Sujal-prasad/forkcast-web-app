from flask import Flask, render_template, url_for,request,jsonify
import os

from utlils.search_location import search_location
from utlils.user_location import current_location_user
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/process-address',methods=['post'])
def process_address():
    
    user_data=request.get_json()
    address=user_data.get("address")
    if not address:
        return jsonify({"error":"address not found"}),400
    else:
        try:
            result=current_location_user(address)
            return jsonify(result),200
        except Exception as e:
            return jsonify({"error":str(e)}),400


   

   
    

@app.route('/search',methods=['post','get'])
def search_address():
    if request.method=='POST':
        try:
            result=search_location()
            return jsonify(result),200
        except Exception as e:
            return jsonify({"error":str(e)}),400
   





    



app.run(debug=True)
