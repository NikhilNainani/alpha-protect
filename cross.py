import datetime as dt
import dateHandler as dh

class cross:
	def __init__( self, ccy1, ccy2 ):
		self.ccy1 = ccy1
		self.ccy2 = ccy2
		self.cross = ccy1 + "/" + ccy2
		
	def spot_rate( self, date ):
		return 0.82
	
	def fwd_rate( self, date, setl_date ):
		spot_date = dh.spot_date( self.ccy1, self.ccy2, date, return_type = date )
		gap = (setl_date - spot_date).days
		
		offsets    = [ "0d", "1w", "1m", "2m", "3m", "6m", "9m", "1y" ]
		cal 	   = self.ccy1 + "|" + self.ccy2
		setl_dates = map( lambda x: dh.offset_date( 0, dh.add_period( spot_date, x ), cal ), offsets )

		for i in range(0, len(setl_dates)-1 ):
			if( setl_dates[i] <= setl_date and setl_dates[i+1] >= setl_date ):
				near_date = setl_dates[i]
				far_date  = setl_dates[i+1]
				break
		
		dcf = float( (far_date - setl_date).days )/ float( (far_date - near_date).days ) 
		

c = cross( "USD", "GBP" )
c.fwd_rate( "2018-03-01", dt.datetime.strptime( "2018-03-30", "%Y-%m-%d" ).date() )		
		
			
				
