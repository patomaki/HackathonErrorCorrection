import time
import datetime
import numpy as np

#-----Function definitions-----#
def date_str():
    '''
    Return a date-string to add to e.g. filename
    '''
    # src timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
    # formatting stackoverflow.com/questions/13890935/does-pythons-time-time-return-the-local-or-utc-timestamp
    time_stamp = time.time()
    time_stamp_str = str(datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d__%H-%M-%S'))
    return time_stamp_str
# #
# #
def save_np_data(np_data,folder='',name_str='data',header_str=''):
    '''
    Save numpy list np_data to a given (relative) folder
    '''
    np.savetxt(folder+name_str+'.txt',np_data, header=header_str)
# #
# #
