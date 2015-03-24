import pandas as pd
import json

def fLoadLoans_JSON(intStartFile, intFinishFile):
	# Load 'intNoLoans' from JSON
	dfAll = pd.DataFrame()

	for i in range(intStartFile,intFinishFile):
	    f = open('/home/alexb/Dropbox/Insight/Kiva/data/kiva_ds_json/loans/' + str(i) + '.json')
	    dataLoans = json.load(f)
	    dfLoans = json_normalize(dataLoans['loans'])
	    f.close()
	    dfAll = pd.concat([dfAll,dfLoans])
	    if i % 10 == 0: print ("Loading file: " + str(i))
	return dfAll

def fLoadLoans_Lenders_JSON():
	return 

def fCleanLoanData(dfLoans):

	# Clean data
	dfLoans = dfLoans.drop('basket_amount',1)
	dfLoans = dfLoans.drop('bonus_credit_eligibility',1)
	dfLoans = dfLoans.drop('image.id',1)
	dfLoans = dfLoans.drop('image.template_id',1)
	dfLoans = dfLoans.drop('journal_totals.bulkEntries',1)
	dfLoans = dfLoans.drop('currency_exchange_loss_amount',1)
	dfLoans = dfLoans.drop('location.country_code', 1)
	dfLoans = dfLoans.drop('tags',1)
	dfLoans = dfLoans.drop('theme',1)
	dfLoans = dfLoans.drop('translator',1)
	dfLoans = dfLoans.drop('video',1)

	# Remove non-English descriptions
	dfLoans = dfLoans[["en" in a for a in dfLoans['description.languages']]]
	dfLoans = dfLoans.drop('description.languages',1)

	# Remove deleted or blank status entries - 'refunded'  omitted
	dfLoans = dfLoans[[a in ['paid','defaulted','fundraising','funded'] for a in dfLoans['status']]]

	# Add features
	buckets = pd.cut(dfLoans['funded_amount'], 10)#labels = ['a','b','c','d','e'])
	dfLoans['funded_buckets'] = buckets
	buckets = pd.cut(dfLoans['lender_count'], 20,precision=0)#labels = ['a','b','c','d','e'])
	dfLoans['lender_buckets'] = buckets

def fSaveLoan(dfLoans, file_name):
	# Output to CS
	dfLoans.to_csv(file_name, encoding="utf-8") 

def fLoadLoans_CSV(file_name):
	dfLoans = pd.DataFrame(pd.read_csv(file_name))
	try:
		dfLoans = dfLoans.drop('Unnamed 0:',1)
	except Exception:
		pass

	return dfLoans
	
