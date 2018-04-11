import datetime as dt
from subAccount import subAccount

x = subAccount(1, dt.datetime.strptime( "2018-03-26", "%Y-%m-%d" ) )
x.aggregate_security_data()
print x.init_orders()
