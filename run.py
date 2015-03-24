#!/usr/local/bin/python
from app import app

from kiva_modules import modLoadData
from kiva_modules import modRandomForest

app.loans = modLoadData.fLoadLoans_CSV("~/kiva/insight_kiva/dfLoans_1_100_dict2.csv")
app.loans = modRandomForest.fRandomForest(app.loans)
app.run(debug = True)
