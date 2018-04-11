import pandas as pd

def parse_sec_data( files, transform_rules, ccys, misc_rules, date ):
	#parse security wise portfolio data
	#parse security wise ohn
	ccys = map(str.lower, ccys )
	weights = pd.read_csv( files["wts"] )
	weights.columns = map(str.lower, weights.columns)
	
	#transform input into parsable output
	for key, rule in transform_rules["wts"].items():
		weights[key] = eval(rule)		
	
	exposures = pd.read_csv( files["exp"] )
	exposures.columns = map(str.lower, exposures.columns)
	
	#transform input into parsable output
	for key, rule in transform_rules["exp"].items():
		exposures[key] = eval(rule)	
	
	data =  weights.merge( exposures, how = 'inner' )
	data = data[ eval(misc_rules["filter"]) ]

	dict_data = dict( (sec, {}) for sec in list(data["security"]) )
	for idx,row in data.iterrows():
		for key, val in row.items():
			if key in ccys and val != 0:
				dict_data[row.security][key] = val*row["exposure"]	

	return dict_data

def parse_agg_assets( files, transform_rules, misc_rules, ccys, date ):	
	# pasre portfolio data for subaccounts which do not have security breakdown
	#parse share-class data
	#parse ohn on an aggregate basis
	ccys = map(str.lower, ccys ) 
	exposures = pd.read_csv( files["exp"] )
	exposures.columns = map(str.lower, exposures.columns)
	
	#transform input into parsable output
	for key, rule in transform_rules["exp"].items():
		exposures[key] = eval(rule)
	
	exposures = exposures[ eval(misc_rules["filter"]) ]
	
	data = { }
	for idx, row in exposures.iterrows():
		if( str.lower(row.ccy) in ccys ):
			data[str.lower(row.ccy)] = data.get(row.ccy, 0 ) + row.exposure
	
	return{ "$uniform$": data }							

def parse_open_trades( files, transform_rules, misc_rules, ccys, date ):	
	#parse open_trades
	ccys = map(str.lower, ccys ) 
	rows = pd.read_csv( files["trades"] )
	rows.columns = map(str.lower, rows.columns)
	
	rows = rows[ eval(misc_rules["filter"]) ]
	#transform input into parsable output
	for key, rule in transform_rules["trades"].items():
		rows[key] = eval(rule)
	
	data = []
	for idx, row in rows.iterrows():
		print row.ccy1, row.ccy2, ccys
		if str.lower(row.ccy1) not in ccys and str.lower(row.ccy2) not in ccys:
			continue
		trade = {}
		trade["ccy1"] 	     = row.ccy1
		trade["ccy2"] 	     = row.ccy2
		trade["qty"]  	     = row.qty
		trade["rate"] 	     = row.rate
		trade["setl date"]   = row["setl date"]
		trade["trade date"]  = row["trade date"]
		trade["cpid"] 		 = row.get("cpid", "")
		trade["fixing date"] = row.get("fixing date", "")
		trade["fixing ref"]  = row.get("fixing ref", "")
		data.append(trade)
			
	return{ "Trades": data }		

files = {"wts": "try/try.csv", "exp": "try/try2.csv" }
ccys = [ "USD", "AUD", "HKD", "SGD", "NZD" ]
tform_rules = {"wts": { "usd": "weights[\"usd\"]*2" }, "exp" :{} }
misc = {"filter": "data['date'] == date"}

print parse_sec_data(files, tform_rules,ccys,misc, "2018-03-27" )	

files = {"exp": "try/try3.csv" }
ccys = [ "USD", "AUD", "HKD", "SGD", "NZD" ]
tform_rules = { "exp" : {"exposure": "exposures[\"long\"] + -1*exposures[\"short\"]" } }
misc = {"filter": "exposures['date'] == date"}
print parse_agg_assets( files, tform_rules, misc, ccys, "2018-03-26" )

files = {"trades": "try/try4.csv" }
ccys = [ "USD", "AUD", "HKD", "SGD", "NZD" ]
tform_rules = { "trades" : {"ccy2": "str(\"eur\")" } }
misc = {"filter": "rows['date'] == date"}
print parse_open_trades( files, tform_rules, misc, ccys, "2018-03-26" )
