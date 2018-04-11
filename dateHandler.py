import datetime as dt
from bizdays import Calendar
import utils as ut

#http://wilsonfreitas.github.io/python-bizdays/
#https://pypi.python.org/pypi/datedelta/1.2
@ut.memoize
def date_from_rule( freq, rule, date, cal, offset = 0 ):
	if( freq == "month" ):
		dateObj = dt.datetime.strptime( date, "%Y-%m-%d" )
		year  = dateObj.year
		month = dateObj.month + offset
		if( month > 12 ):
			month =  month % 12
			year += 1 
		
		return get_day_of_month( rule, year, month, cal ) 
		
@ut.memoize
def init_cal(cal_name):
	if( "|" in cal_name):
		cal_names = cal_name.split("|")
		cals = [ init_cal(c) for c in cal_names ]
		return( union_cal(cals))
	
	#----temporary-------------
	if( cal_name not in [ "USD", "GBP" ] ):
		cal_name = "USD"
			
	cal_file = "Holidays/" + cal_name + ".cal"
	cal = Calendar.load( cal_file )
	return(cal)
	
@ut.memoize	
def get_day_of_month( rule, year, month, cal_name ):
	cal = init_cal(cal_name)
	return( dt.datetime.strftime(cal.getdate( rule, year, month ), "%Y-%m-%d" ) )
	
@ut.memoize
def offset_date( offset, date, cal_name ):
	cal = init_cal(cal_name)
	return( cal.offset( date, offset ) )
	
def union_cal( cals ):
	holidays = []
	for cal in cals:
		holidays = list(set(holidays).union(cal.holidays))
	holidays = sorted(holidays)	
	union_cal = Calendar( holidays = holidays, startdate = holidays[0],\
						  enddate = holidays[-1], weekdays = ("sat","sun") )
	return(union_cal)
	
def spot_date( ccy1, ccy2, date, return_type = "string" ):
	cal_name = ccy1 + "|" + ccy2
	
	usd_cross = False
	if(ccy2 == "USD"):
		usd_cross = True
		other_ccy = ccy1
	elif(ccy1 == "USD"):
		usd_cross = True
		other_ccy = ccy2
		
	if( usd_cross ):
		if( other_ccy in [ "CAD", "PHP", "TRY", "RUB" ] ):
			spot_date = offset_date( 1, date, cal_name )
		else:
			spot_date = offset_date( 2, date, other_ccy )
			if( spot_date < offset_date( 1, date, "USD" ) ):
				spot_date = offset_date( 1, spot_date, cal_name )
				
	else:
		spot_date = offset_date( 2, date, cal_name )	
	
	if( return_type == "string" ):			
		return dt.datetime.strftime( spot_date, "%Y-%m-%d " )			 	
	else:
		return spot_date
		
def add_period( date, period ):
	offset = int( period[:-1] )
	if period.endswith("w"):
		return (date + dt.timedelta(days=7*offset))
	elif period.endswith("m"):
		return (dt.date( date.year + ( date.month + offset - 1 )/12,\
			   (date.month + offset -1) %12 + 1, date.day ) )
	elif period.endswith("y"):
		return (dt.date( date.year + offset, date.month, date.day ) )
	elif period.endswith("d"):
		return (date + dt.timedelta(days=offset))	
			
