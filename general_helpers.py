import time
import datetime
import numpy as np

#-----Function definitions-----#
def date_str():
    '''
    Return a date-string to add to e.g. filename
    '''
    # src timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
    time_stamp = time.time()
    time_stamp_str = str(datetime.datetime.fromtimestamp(time_stamp).isoformat())
    time_stamp_str = time_stamp_str.split(':',1)[0]
    return time_stamp_str
# #
# #
def save_np_data(np_data,folder='',info_str='data'):
    '''
    Save numpy list np_data to a given (relative) folder
    '''
    np.savetxt(folder+info_str+'.txt',np_data)
# #
# #
