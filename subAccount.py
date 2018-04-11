import datetime as dt
import dateHandler
from temp_data import TEMP_VALS
from orderGenerator import orderGenerator,ruleExtractor
		 
#can have customized generators like orderGeneratorOdey etc
class subAccount:
	def init_client_data(self, time = dt.datetime.now(), version = -1 ):
		self.client_data = TEMP_VALS["d"]

	def init_open_hedges(self, time = dt.datetime.now(), version = -1 ):
		self.open_hedges = TEMP_VALS["ohn"]
		
	def init_open_trades(self, time = dt.datetime.now(), version = -1 ):
		self.open_trades = TEMP_VALS["ot"]	

	def init_hedging_rules(self, time = dt.datetime.now(), version = -1 ):
		self.hedging_rules = TEMP_VALS["r"]
				
	def __init__(self, subAccount_id, time = dt.datetime.now(), version = -1 ):
		self.subAccount_id = subAccount_id
		self.base_ccy = "EUR"
		self.date = time.strftime("%Y-%m-%d")
		self.ccys = [ "USD", "SGD", "HKD", "NZD", "AUD" ]
		self.init_client_data(time, version)
		self.init_open_hedges(time, version)
		self.init_hedging_rules(time, version)
		self.init_open_trades(time, version)
		
	def aggregate_security_data(self ):
		if(self.hedging_rules["type"] == "portfolio"):
			tag = "Assets"
		else:
			tag = "Liabilities"

		data = self.client_data["Data"][tag]
		aggregated_data = {}
		for sec, sec_data in data.items():
			for ccy, exposure in sec_data.items():
				aggregated_data[ccy] = aggregated_data.get(ccy,0) + exposure
			
		self.client_data["Data"][tag] = {"$uniform$": aggregated_data }
		
	def init_orders(self):
		generator = orderGenerator(self)
		orders = generator.generate()
		return orders
		
	def settle_date( self, security, ccy ):
		rule_extractor = ruleExtractor(self)
		setl_date_rule = rule_extractor.extract( "settlement rule", security, ccy )
				
		#TODO verify
		setl_cal	   = ccy + "|" + self.base_ccy
	
		setl_date 	   = dateHandler.date_from_rule(setl_date_rule[0],\
							setl_date_rule[1],self.date, ccy )
							
		roll_date      = self.roll_date(security, ccy, setl_date)		
		offset 		   = 1
		curr_date 	   = dt.datetime.strptime( self.date, "%Y-%m-%d" ).date()

		while( roll_date < curr_date ):
			print roll_date
			setl_date 	   = dateHandler.date_from_rule(setl_date_rule[0],\
								setl_date_rule[1],self.date, ccy, offset )
			roll_date      = self.roll_date(security, ccy, setl_date)
			offset 		  += 1
		return( setl_date )
		
	def version_info( self ):
		data_ver  = self.client_data["version"]
		ohn_ver   = self.open_hedges["version"]
		rules_ver = self.hedging_rules["version"]
		
		version_info = { "data":data_ver,"ohn":ohn_ver,"rules":rules_ver }
		return( version_info )
		
	def roll_date(self, security, ccy, date ):
		rule_extractor = ruleExtractor(self)
		roll_offset    = rule_extractor.extract( "roll offset", security, ccy )
		#TODO verify
		roll_cal	   = ccy + "|" + self.base_ccy
		roll_date      = dateHandler.offset_date( -1*roll_offset, date, roll_cal )		
		return(roll_date)
		
	def nav_est_date( self ):
		offset = self.hedging_rules["nav confirm delay"]
		cal    = self.hedging_rules["bizdays"]
		return dateHandler.offset_date( -1*offset, self.date, cal ) 		

	def get_prev_data( self,data_type, date ):
		return( { "$uniform$": { "USD": 390.0 } } )		  									 
		
