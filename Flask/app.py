import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import random
app = Flask(__name__)
model = joblib.load("engine_model.sav")


app = Flask(__name__)

@app.route('/m_predict')
def predict():
    return render_template('Manual_predict.html')

@app.route('/s_predict')
def spredict():
    return render_template('Sensor_predict.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    x_test = [[int(x) for x in request.form.values()]]
   
    
    print(x_test)
    a = model.predict(x_test)
    pred = a[0]
    if(pred == 0):
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."
    
    return render_template('Manual_predict.html', prediction_text=pred)

@app.route('/sy_predict',methods=['POST'])
def sy_predict():
    inp1=[]
    inp1.append(random.randint(0,100)) #id
    inp1.append(random.randint(0,365)) #cycle
    for i in range(0,24):
        inp1.append(random.uniform(0,1))
    inp1.append(random.randint(0,365)) #ttf
    pred=model.predict([inp1])
    payload_scoring = {"input_data": 
			[{"field": [['id','cycle','setting1', 'setting2', 'setting3', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11',
                   's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21','ttf']], 
			"values": [[1,1,0.45977,0.166667,0,0,0.183735,0.406802,0.309757,0,1,0.726248,0.242424,0.109755,0,0.369048,0.633262,0.205882,0.199608,0.363986,0,0.333333,0,0,0.713178,0.724662,191]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7488912b-b6aa-4b62-a92b-8273bfcc6da6/predictions?version=2021-12-03', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions =response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    if(pred == 0):
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."
    return render_template('Sensor_predict.html', prediction_text=pred,data=inp1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
