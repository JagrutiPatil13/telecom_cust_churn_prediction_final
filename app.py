from flask import Flask, render_template, request, escape

import numpy as np
import pickle
import bz2file as bz2
import _pickle as cPickle


dmodel = bz2.BZ2File("telco_pkl_comp.txt", 'rb')
model = cPickle.load(dmodel)


app = Flask(__name__)


@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':

        total_og_weightage = int(request.form.get('total_og_weightage'))
        roam_og_mou_8 = float(request.form.get('roam_og_mou_8'))
        days_since_last_rech = float(request.form.get('days_since_last_rech'))
        loc_og_t2m_mou_8 = float(request.form.get('loc_og_t2m_mou_8'))
        aon = int(request.form.get('aon'))
        total_rech_num_8 = int(request.form.get('total_rech_num_8'))
        arpu_8 = float(request.form.get('arpu_8'))
        max_rech_amt_8 = int(request.form.get('max_rech_amt_8'))
        fb_user_weightage = float(request.form.get('fb_user_weightage'))

        data = {'total_og_weightage': [total_og_weightage],
                'roam_og_mou_8': [roam_og_mou_8], 'days_since_last_rech': [days_since_last_rech],
                'loc_og_t2m_mou_8': [loc_og_t2m_mou_8], 'aon,total_rech_num_8': [aon, total_rech_num_8],
                'arpu_8':[arpu_8], 'max_rech_amt_8': [max_rech_amt_8], 'fb_user_weightage': [fb_user_weightage]}



        prediction = model.predict(np.array([total_og_weightage,roam_og_mou_8,days_since_last_rech,loc_og_t2m_mou_8,aon,total_rech_num_8,arpu_8,max_rech_amt_8,fb_user_weightage]).reshape(1,9))

        if prediction == 1:
            prediction = 'Customer will churn'
        else:
            prediction = 'Customer will not be churn'
        return render_template("prediction.html", prediction_text=prediction)

    else:
        return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=True)
