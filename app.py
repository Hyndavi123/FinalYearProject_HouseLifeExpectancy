from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
from sklearn import model_selection
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

import numpy as np
app = Flask(__name__)
app.debug = True

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/results", methods=['GET', 'POST'])    
def results():
    df = pd.read_csv('price.csv',names=['soilBearing', 'loadsActing','ironQuality', 'sandType', 'noOfRows', 'noOfCols', 'noOfStairs', 'earthquakeLoad', 'windLoad', 'concreteMix', 'years', 'price'])
    house_features = ['soilBearing', 'loadsActing','ironQuality', 'sandType', 'noOfRows', 'noOfCols', 'noOfStairs', 'earthquakeLoad', 'windLoad', 'concreteMix']
    house_features1 = ['noOfStairs', 'windLoad']
    df['soilBearing'].replace(to_replace = ['deep','shallow'],value = [1,2],inplace = True) 
    df['loadsActing'].replace(to_replace = ['dead','dead ','live'],value = [1,1,2],inplace = True) 
    df['ironQuality'].replace(to_replace = ['High','Medium', 'Low'],value = [1,2,3],inplace = True) 
    df['sandType'].replace(to_replace = ['concrete','pit','utility','fill'],value = [1,2,3,4],inplace = True) 
    df['earthquakeLoad'].replace(to_replace = ['prone','notProne'],value = [1,2],inplace = True) 
    X = df.loc[1:11233, house_features].values
    X1 = df.loc[1:11233, house_features1].values
    Y = df.loc[1:11233, ['years']].values
    Z = df.loc[1:11233, ['price']].values
    X_trainl, X_testl, Y_trainl, Y_testl = model_selection.train_test_split (X, Y, test_size=0.3, random_state=0)
    X_trainl1, X_testl1, Z_trainl, Z_testl = model_selection.train_test_split (X1, Z, test_size=0.3, random_state=0)
    lm = linear_model.LinearRegression()
    lm.fit(X_trainl, Y_trainl)
    y_predl = lm.predict(X_testl)
    r2_score = lm.score(X_testl, Y_testl)
    print(r2_score*100,'%')
    lm1 = linear_model.LinearRegression()
    lm1.fit(X_trainl1, Z_trainl)
    y_predl1 = lm1.predict(X_testl1)
    r2_score1 = lm1.score(X_testl1, Z_testl)
    print(r2_score1*100,'%')
    soilBearingCapacity = request.form.get('soil')
    soilBearingCapacity = str(soilBearingCapacity)
    soilBearingCapacity = soilBearingCapacity.lower()
    print(soilBearingCapacity)
    loadsAct = request.form.get('load')
    loadsAct = str(loadsAct)
    loadsAct = loadsAct.lower()
    print(loadsAct)
    iron = request.form.get('iron')
    iron = str(iron)
    iron = iron.lower()
    print(iron)
    sand = request.form.get('sand')
    sand = str(sand)
    sand = sand.lower()
    print(sand)
    rows = request.form['rows']
    print(rows)
    cols = request.form['cols']
    print(cols)
    stairs = request.form['stairs']
    print(stairs)
    earthquake = request.form.get('earth')
    earthquake = str(earthquake)
    earthquake = earthquake.lower()
    print(earthquake)
    wind = request.form['wind']
    print(wind)
    mixRatio = request.form.get('mix')
    print(mixRatio)

    if soilBearingCapacity == "deep":
        capacity = 1
    elif soilBearingCapacity == "shallow":
        capacity = 2
    else:
        return "No entry such as " + soilBearingCapacity + " in soil bearing capacity"
    if loadsAct == "dead":
        loads = 1
    elif loadsAct == "live":
        loads = 2
    else:
        return "No entry such as " + loadsAct + " in loads acting"
    if iron == "high":
        ironQua = 1
    elif iron == "medium":
        ironQua = 2
    elif iron == "low":
        ironQua = 3
    else:
        return "No entry such as " + iron + " in iron quality"
    if sand == "concrete":
        sandType = 1
    elif sand == "pit":
        sandType = 2
    elif sand == "utility":
        sandType = 3
    elif sand == "fill":
        sandType = 4
    else:
        return "No entry such as " + sand + " in sand type"
    if earthquake == "prone":
        earthprone = 1
    elif earthquake == "notprone":
        earthprone = 2
    else:
        return "No entry such as " + earthquake + " in earthquake prone attribute"

    x = [capacity, loads, ironQua, sandType, rows, cols, stairs, earthprone, wind, mixRatio]
    x1 = [stairs, wind]
    x = np.array(x)
    x1 = np.array(x1)
    x = x.reshape(1, -1)
    x1 = x1.reshape(1, -1)
    predictionValue = lm.predict(x)
    predictionValue1 = lm1.predict(x1)
    print("years: ", predictionValue) 
    print("price: ", predictionValue1) 
    s = int(predictionValue)
    s1 = int(predictionValue1)
    print(s1)
    return render_template('show.html', s=s, s1=s1)
 