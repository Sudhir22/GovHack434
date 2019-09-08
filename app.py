from flask import Flask,request,render_template
from Get_Distance import *
from Model.Inference import *
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
    build_or_not=""
    if test_predict[0]==-1:
        build_or_not="cannot build"
    else:
        build_or_not = "can build"
    print(list(test_data.iloc[0,:].values))
    return render_template("OutputPage.html",test_data=list(test_data.iloc[0,:].values),build_or_not=build_or_not)

@app.route("/details/")
def details():
    return "Hi"



if __name__ == "__main__":
    app.run(debug=True)