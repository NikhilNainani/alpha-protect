import datetime as dt
import dateHandler as dh

class ruleExtractor:
	def __init__(self, subAccount ):
		self.subAccount = subAccount
	#add default	
	def extract(self, param, sec, ccy, default = None ):
		rules = self.subAccount.hedging_rules
		if not( param in rules ):
			return default
		param_rules = rules[param]
		
		if not( sec in param_rules ): 
			if not "$uniform$" in param_rules:
				return default
			else:
				sec_param_rules = param_rules["$uniform$"]
		else:
			sec_param_rules = param_rules[sec]
					
		if not ccy in sec_param_rules:
			if not "$uniform$" in sec_param_rules:
				return defaults
			else:
				return sec_param_rules["$uniform$"]
		else:
			return sec_param_rules[ccy]	

class orderGenerator:
	def __init__(self, subAccount ):
		self.subAccount = subAccount
		
	def enhance(self, orders):
		subAcc_id = self.subAccount.subAccount_id
		for order in orders:
			order["subAccount_id"] = subAcc_id
		return(orders)
				
	def roll_orders(self):
		subAcc = self.subAccount
		open_trades = subAcc.open_trades["Trades"]
		roll_orders = []
		for trade in open_trades:
			if( trade["ccy1"] in subAcc.ccys ):
				local_ccy = trade["ccy1"]
			else:
				local_ccy = trade["ccy2"]
			#print type(dt.date.strptime(subAcc.date, "%Y-%m-%d" )), type(subAcc.roll_date( trade["sec"], local_ccy, trade["setl date"] ) )
			if( subAcc.roll_date( trade["sec"], local_ccy, trade["setl date"] )\
				== dt.datetime.strptime(subAcc.date, "%Y-%m-%d" ).date()):
				
				far_setl_date = subAcc.settle_date( trade["sec"], local_ccy )
				version_info  = subAcc.version_info()
				
				near_leg = {
					"security"			: trade["sec"], 
					"ccy1"				: trade["ccy1"], 
					"ccy2"				: trade["ccy2"], 
					"ohn"				: None, 
					"exposure"			: None,
					"notional"			: -1*trade["qty"],
					"settlement date"	: trade["setl date"],
					"version_info"		: version_info,
					"notes"				: "roll:near leg"
				}
				
				far_leg = {
					"security"			: trade["sec"], 
					"ccy1"				: trade["ccy1"], 
					"ccy2"				: trade["ccy2"], 
					"ohn"				: None, 
					"exposure"			: None,
					"notional"			: trade["qty"],
					"settlement date"	: far_setl_date,
					"version_info"		: version_info,
					"notes"				: "roll:far leg"
				}
				
				roll_orders += [ near_leg, far_leg ]
		
		return( roll_orders )	

	def generate(self):
		all_orders = []
		all_orders = all_orders + self.generate_adjustments() + self.roll_orders() +\
					 self.generate_esr_orders() + self.generate_csr_orders()
					 
		enhanced_orders = self.enhance(all_orders)			 		
		return(enhanced_orders)
		
	def generate_adjustments(self):		
		subAcc 		   = self.subAccount
		if(subAcc.hedging_rules["type"] == "portfolio" ):
			data  		   = subAcc.client_data["Data"]["Assets"]
			multiplier 	   = 1
		else:
			data  		   = subAcc.client_data["Data"]["Liabilities"]
			multiplier     = -1
			
		ohn   		   = subAcc.open_hedges["Data"]		
		version_info   = subAcc.version_info()
		base_ccy 	   = subAcc.base_ccy
		
		rule_extractor  = ruleExtractor(subAcc)
		orders   		= []
		
		for security, sec_data in data.items():
			sec_ohn 	= ohn.get(security, {} )
			
			for ccy, exposure in sec_data.items():
				sec_ccy_ohn = sec_ohn.get(ccy, 0 )
				#add moe cases here
								
				notional  = ( -1*sec_ccy_ohn - exposure ) * multiplier
				deviation = float(float(notional)/float(exposure))				
				threshold = rule_extractor.extract( "thresholds", security, ccy )
				
				setl_date = subAcc.settle_date( security, ccy )
									
				if ( deviation > 0 and deviation < threshold["long"] ) or\
				   ( deviation < 0 and deviation > -1*threshold["short"] ):
					notional = 0
				
				if notional != 0:
					order = {"security"			: security, 
							"ccy1"				: ccy, 
							"ccy2"				: base_ccy, 
							"ohn"				: sec_ccy_ohn, 
							"exposure"			: exposure,
							"notional"			: notional,
							"settlement date"	: setl_date,
							"version_info"		: version_info,
							"notes"				: "adj" 
							}
					orders.append(order)
				
		return orders
		
	def generate_cash_orders(self):
		subAcc 		   = self.subAccount
		data   		   = subAcc.client_data["Data"]["Cash"]		
		version_info   = subAcc.version_info()
		base_ccy 	   = subAcc.base_ccy
		ccys 		   = subAcc.ccys
		
		rule_extractor  = ruleExtractor(subAcc)
		orders   		= [] 
		
		cash_balances 	= dict.fromkeys( ccys, 0 )
		
		scb = data.get("start", {})
		for ccy, val in scb.items():
			cash_balances[ccy] += val
		
		#t_o
		flow_0 = data.get("flow0", {})
		for ccy, val in flow_0.items():
			cash_balances[ccy] += val
			
		for ccy, val, in cash_balances.items():
			if( val != 0 ):
				thresholds = rule_extractor.extract( "cash_thresholds",\
													 "$uniform$",\
													  ccy )
				reqd_cash  = rule_extractor.extract( "required_cash",\
													 "$uniform$",\
													  ccy ) 									  			    				
				
		return(orders)
		
	def generate_esr_orders(self):
	#generate est s/r orders
		subAcc 		   = self.subAccount
		data  		   = subAcc.client_data["Data"].get("Est S/R", {})
		version_info   = subAcc.version_info()
		base_ccy 	   = subAcc.base_ccy
		
		rule_extractor  = ruleExtractor(subAcc)
		orders   		= []
		
		for security, sec_data in data.items():
			for ccy, s_r in sec_data.items():
				
				far_setl_date  = subAcc.settle_date( security, ccy )
				spot_setl_date = dh.spot_date( ccy, base_ccy, subAcc.date )					
				
				if s_r != 0:
					spot_order = {
							"security"			: security, 
							"ccy1"				: ccy, 
							"ccy2"				: base_ccy, 
							"ohn"				: None, 
							"exposure"			: s_r,
							"notional"			: -1*s_r,
							"settlement date"	: spot_setl_date,
							"version_info"		: version_info,
							"notes"				: "est s/r spot" 
							}
					orders.append(spot_order)
					
					far_order = {
							"security"			: security, 
							"ccy1"				: ccy, 
							"ccy2"				: base_ccy, 
							"ohn"				: None, 
							"exposure"			: s_r,
							"notional"			: s_r,
							"settlement date"	: far_setl_date,
							"version_info"		: version_info,
							"notes"				: "est s/r far" 
							}
					orders.append(far_order)
				
		return orders

	def generate_csr_orders(self):
		#generate conf-sr orders
		subAcc 		   = self.subAccount
		conf_data  	   = subAcc.client_data["Data"].get( "Conf S/R", {} )
		version_info   = subAcc.version_info()
		base_ccy 	   = subAcc.base_ccy
		
		est_date	   = subAcc.nav_est_date() 					 
		est_data 	   = subAcc.get_prev_data( "Est S/R", est_date ) 		 
		
		rule_extractor  = ruleExtractor(subAcc)
		orders   		= []
		
		for security, sec_csr in conf_data.items():
			for ccy, csr in sec_csr.items():
				
				sec_esr        = est_data.get( security, {} )
				esr            = sec_esr.get( ccy, 0 )
				far_setl_date  = subAcc.settle_date( security, ccy )
				notional       = csr - esr 
				
				if notional != 0:
					order = {
							"security"			: security, 
							"ccy1"				: ccy, 
							"ccy2"				: base_ccy, 
							"ohn"				: None, 
							"exposure"			: csr,
							"notional"			: notional,
							"settlement date"	: far_setl_date,
							"version_info"		: version_info,
							"notes"				: "conf s/r adj" 
							}
					orders.append(order)
				
		return orders				
