from flask import render_template

from app import app

import pymysql as mdb

db = mdb.connect(user="root", host="localhost", db="dbKiva_Loans", charset='utf8')

@app.route('/')
@app.route('/index')

def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')

def cities_page():
    with db:
        cur = db.cursor()
        cur.execute("SELECT Name FROM City LIMIT 15;")
        query_results = cur.fetchall()

    cities = ""

    for result in query_results:
        cities += result[0]
        cities += "<br>"

    return cities

@app.route("/db_fancy")

def cities_page_fancy():

    with db:
        cur = db.cursor()
        cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population LIMIT 15;")
        query_results = cur.fetchall()

    cities = []

    for result in query_results:
        cities.append(dict(name=result[0], country=result[1], population=result[2]))

    return render_template('cities.html', cities=cities) 


@app.route("/db_Kiva")

def Kiva_page_fancy():

    with db:
        cur = db.cursor()
        cur.execute("SELECT * FROM dfTest LIMIT 15")
        query_results = cur.fetchall()

    loans = []

    for result in query_results:
        loans.append(dict(name=result[2], country=result[3], population=result[4]))

    return render_template('index_db.html', loans=loans) 
