TEMP_VALS = {
	"ohn":{
			"version" :1,
			"Data": {"Apple": { "USD" : -90000.0 },
				     "MPAX":  { "SGD": -1100.0, "HKD": -1000.0, "NZD": -400.0,  "AUD": -505.0 } }
	},
	"ot":{
			"version" :1,
			"Trades": [
				{"sec": "Apple", "ccy1": "USD", "ccy2": "EUR", "qty": -50000.0,"rate": 0.91, 
				 "cpid": "001", "setl date": "2018-03-26", "trade date": "2018-03-01", "fixing date": "",
				 "fixing ref": "" },
				{"sec": "Apple", "ccy1": "USD", "ccy2": "EUR", "qty": -40000.0,"rate": 0.91, 
				 "cpid": "001", "setl date": "2018-03-26", "trade date": "2018-03-01", "fixing date": "",
				 "fixing ref": "" },
				{"sec": "MPAX", "ccy1": "SGD", "ccy2": "EUR", "qty": -1100.0,"rate": 0.81, 
				 "cpid": "001", "setl date": "2018-03-26", "trade date": "2018-03-01", "fixing date": "",
				 "fixing ref": "" },
				{"sec": "MPAX", "ccy1": "HKD", "ccy2": "EUR", "qty": -1000.0,"rate": 0.1, 
				 "cpid": "001", "setl date": "2018-03-26", "trade date": "2018-03-01", "fixing date": "",
				 "fixing ref": "" },
				{"sec": "MPAX", "ccy1": "NZD", "ccy2": "EUR", "qty": -400.0,"rate": 0.59, 
				 "cpid": "001", "setl date": "2018-03-26", "trade date": "2018-03-01", "fixing date": "",
				 "fixing ref": "" },
				{"sec": "MPAX", "ccy1": "AUD", "ccy2": "EUR", "qty": -505.0,"rate": 0.63, 
				 "cpid": "001", "setl date": "2018-03-26", "trade date": "2018-03-01", "fixing date": "",
				 "fixing ref": "" },
			 ]     
	},
	"r":{
			"version" : 1,
			"type" : "liabilities",
			"bizdays" : "USD",
			"thresholds" : { 
				"$uniform$": {"$uniform$": {"long": 0.02, "short":0.02 } }
			},
			
			"cash_thresholds" : { 
				"$uniform$": {"$uniform$": {"long": 0.02, "short":0.02 } }
			},
			
			"settlement rule" :{
				"$uniform$": {"$uniform$": ["month", "last bizday"] } 
			},
			"roll offset" :{
				"$uniform$": {"$uniform$": 2 } 
			},
			"required cash": {"uniform":{ "USD": 100, "SGD": 100, "HKD": 100, "NZD":100, "AUD":100 }}, 
			"orderGranuality": "security", #security/currency
			"nav confirm delay": 2  
			#roll based parameters later
			#counterparty based split-up next up
	},
	"d":{
			"version": 1,
			"Data": {
				"Assets":{
					"Apple": { "USD": 100000.0 },
					"MPAX":  {"SGD": 1000.0, "HKD": 1000.0, "NZD":500.0, "AUD": 500.0 }
				},
				"Liabilities":{
					"$uniform$": { "USD": 100000.0 }
				},
				"Est S/R":{
					"$uniform$": { "USD": 1000.0 }
				},
				"Conf S/R":{
					"$uniform$": { "USD": 400.0 }
				},
				"Cash": {
					"start": { "USD": 1000, "SGD": 200, "HKD": 100 },
					"flow0": { "USD": 2500, "SGD": 300, "NZD": 200 },
					"flow1": { "AUD": 500 },
					"flow2": { "USD": 50  },
				}
			}
	} 
}

