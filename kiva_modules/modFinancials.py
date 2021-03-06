import pandas as pd
import ast

def fGetCoupons(loan):
	
	#obtain a list of coupon payments from the cashflows

	coupon_list = pd.DataFrame(ast.literal_eval(loan['payments'].replace('\r','').replace('\n','')))
		
	coupons = []

	for i in range(0,len(coupon_list)):
		result = coupon_list.iloc[i]
		coupons.append(dict(id=loan['id'], amount=result['amount'],date=result['processed_date']))
	
	return coupons
