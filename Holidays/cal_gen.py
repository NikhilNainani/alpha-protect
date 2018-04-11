import workalendar.canada as we
import datetime as dt

cal = we.Canada()

years = [ 2012+w for w in range(0,9) ]
hols = ["Saturday", "Sunday" ]

for y in years:
	hols_raw = cal.get_calendar_holidays(y)
	hols     = hols + [ dt.datetime.strftime( d[0], "%Y-%m-%d" ) for d in hols_raw ]
	if(y==2018):
		print hols_raw

for h in hols:
	print h

