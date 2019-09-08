from flask import Flask,request,render_template
from Get_Distance import *
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("WebPage.html")

@app.route('/', methods=['POST'])
def my_form_post():
    processed_text = request.form['text']
    #processed_text = text.upper()
    lat,lng=map(float,processed_text.split(" "))
    busstop_data_path = './Data/Bus_Stops.csv'
    busstop_df = pd.read_csv(busstop_data_path)
    return render_template("OutputPage.html",distance=get_distance_next_stop(lat,lng,busstop_df))

@app.route("/details/")
def details():
    return "Hi"



if __name__ == "__main__":
    app.run(debug=True)