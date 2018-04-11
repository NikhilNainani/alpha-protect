from functools import wraps

def memoize(function):
    memo = {}
    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper
    
class CONST(object):    	
    def __setattr__(self, *_):
        pass
        
def get_formatted_id( int_id,  type_id ):
	if(type_id == "account"):
		size = 4
	elif(type_id == "sub-account"):
		size = 3
	return str(int_id).zfill(size)	        
	
def parse_id(client_id):
	return { "account": client_id[0:4], "sub-account": client_id[4:] }
	
	
