import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sklearn.linear_model as skllm
from sklearn.metrics import classification_report as sklcr
from sklearn.ensemble import RandomForestClassifier as sklrfc
from sklearn import preprocessing as sklpp
from sklearn import metrics as sklm

def fRandomForest(dfLoans):
	
	dfLoans = pd.DataFrame(dfLoans)
	y = dfLoans['status']
	y = pd.DataFrame(y =="paid")
	print y
	#X = pd.DataFrame(dfLoans[['lender_count','journal_totals.entries']])
	x = pd.DataFrame(dfLoans[['terms.loan_amount','partner_id','journal_totals.entries','lender_count','sector']])
	#X = pd.DataFrame(dfLoans[['funded_amount','lender_count','journal_totals.entries]])
	#print Y

	is_train = pd.Series(np.random.uniform(0, 1, len(y.index)) <= .80)

	x = pd.concat([x,pd.get_dummies(x['sector']),pd.get_dummies(x['partner_id'])],axis=1)
	#x = pd.concat([x,pd.get_dummies(x['partner_id']),pd.get_dummies(x['location.country'])],axis=1)
	x= x.drop('partner_id',1)
	x= x.drop('sector',1)
	#x= x.drop('location.country',1)

	x_train, x_test = x[is_train == True], x[is_train == False]
	y_train, y_test = y[is_train == True], y[is_train == False]

	clf = sklrfc(n_jobs=2)
	clf.fit(x_train, y_train)

	#y_pred = clf.predict(x_test)
	y_pred = clf.predict_proba(x_test)
	#pd.crosstab(np.ravel(y_test), np.ravel(y_pred), rownames=['actual'], colnames=['preds']) 

	#y_pred = clf.predict(x_test)
	#scores = []
	#for a in y_pred: scores.extend([a[1]]) #scores.extend(a[1])
	#scores = np.array(scores)
	y_left = []
	y_right = []
	for a in y_pred: y_left.append(a[0]), y_right.append(a[1])

	scored_Loans = dfLoans[is_train==False]
	scored_Loans['y_left'] = y_left
	scored_Loans['y_right'] = y_right
	#fpr, tpr, thresholds = sklm.roc_curve(y_test,scores)

	#pd.crosstab(np.ravel(y_test), np.ravel(y_pred), rownames=['actual'], colnames=['preds']) 
	return scored_Loans

def fFeatureImportance(clf):
	from sklearn.ensemble import ExtraTreesClassifier

	# Build a forest and compute the feature importances
	#forest = ExtraTreesClassifier(n_estimators=250, random_state=0)
	#forest.fit(x_train,np.ravel(y_train))

	importances = clf.feature_importances_
	std = np.std([tree.feature_importances_ for tree in clf.estimators_],
	             axis=0)
	indices = np.argsort(importances)[::-1]

	# Print the feature ranking
	print("Feature ranking:")

	for f in range(10):
	    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

	# Plot the feature importances of the forest
	rng = len(indices)

	plt.figure()
	plt.title("Feature importances")
	plt.bar(range(rng), importances[indices], color="r", yerr=std[indices], align="center")
	plt.xticks(range(rng), indices)
	plt.xlim([-1, 10])
#	plt.show()
	return 

def fConfusionMatrix(y_pred, y_test):
	cm = sklm.confusion_matrix(y_test, y_pred, labels=None)
	plt.matshow(cm)
	plt.title('Confusion matrix')
	plt.colorbar()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.show()
