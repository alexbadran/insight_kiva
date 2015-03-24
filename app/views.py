from flask import current_app, render_template, request, jsonify
from app import app
from unidecode import unidecode

import re
#import pymysql as mdb
import pandas as pd 

from kiva_modules import modLoadData
from kiva_modules import modRandomForest
from kiva_modules import modSearch
from kiva_modules import modFinancials

#db = mdb.connect(user="root", host="localhost", db="kiva_db", charset='utf8')

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)

@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
    )

@app.route("/Kiva", methods = ['POST', 'GET'])
def Kiva_home():
    return render_template('home.html')


@app.route("/Kiva_search")
def Kiva_search():

#    with db:
#         cur = db.cursor()
#         cur.execute("SELECT * FROM kiva_db LIMIT 10")
#         query_results = cur.fetchall()
    loans = []

    query_results = current_app.loans
    
    search_query = ""
    
    if request.args.get('search_query'): search_query = request.args.get('search_query')
    
    query_results = query_results[~query_results['description.texts.en'].isnull()]    
    query_results = modSearch.fSearch(query_results, search_query)

    for i in range(0,min(len(query_results),11)):
        result = query_results.iloc[i]
        desc = striphtml(result['description.texts.en'].decode('unicode_escape').encode('ascii','ignore'))
        desc = desc.replace("\n", " ")
        desc = desc.replace("\r", " ")
        #desc = desc.replace("", ",")
        
        loans.append(dict(name=unidecode(result['name']), activity=result['activity'], country=result['location.country'],  
                            id=result['id'],
                            desc=unidecode(desc), amount=result['terms.loan_amount'], 
                            search_score=round(result['search_score'],2), y_left=result['y_left']))

    return render_template('kiva_index.html', loans=loans)

@app.route("/Kiva_get_coupons", methods = ['POST', 'GET'])
def Kiva_get_coupons():
    
    loanid = request.args.get('loanid',0,int)
    query_results = current_app.loans
    
    coupons = []
    result = query_results[query_results['id']==loanid].iloc[0]
    coupons.extend(modFinancials.fGetCoupons(result))

    return jsonify(coupons=coupons)

