'''
Created on Apr 20, 2014

@author: antipro
'''
import time

class TimeoutException(Exception):
    pass

def until(method, timeout=10, message='', ignored_exceptions=True, interval=0.5):
    """Calls the method provided with the driver as an argument until the \
    return value is not False."""
    end_time = time.time() + timeout
    while(True):
        try:
            value = method()
            if value or value is None:
                return value
        except:
            pass
        time.sleep(0.5)
        if(time.time() > end_time):
            break
    raise TimeoutException(message)

def until_pass(timeout=10):
    def decorator(func):
        def decorator(*args, **kwargs):
            until(func, timeout=timeout)
        return decorator
    return decorator
