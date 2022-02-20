import os
import scipy.io
import scipy.signal as sig
import numpy as np
import re
import matplotlib.cm
import sys
from dataclasses import dataclass

"""
 Some basic python functions that use the same names and parameters as their matlab
 counterparts in order to expedite the process of converting matlab code to python.
    Liam McFadden - AUG 2021
"""

@dataclass
class dclass:
    pass

# Appends all members of args to the source string 'src' 
def strcat(src, *args):
    for s in args:
        src += s

    return src

# Converts a number to a string
def num2str(num):
    return str(num)

# Converts a string to a number
def str2num(string):
    return int(string) if string.find('.') == -1 else float(string)


# Returns the indices of all occurances of tgt in arr
def strfind(src, tgt):
    if type(src) is str:
        ret = [i.start() for i in re.finditer(tgt, src)]
    # assume that if we are not given a string it is a list (no error handling lol)
    else:
        ret = [i for i, e in enumerate(src) if e == tgt]

    return ret 

# checks if a file exists
# Note: only checks for valid files 
# returns 2 if a valid file name is provided, otherwise -1
def exist(name):
    return os.path.exists(os.path.join(os.getcwd(), name))

# loads a '.mat' file into a variable using scipy.io
# returns a dictionary 
def load(fname):
    return scipy.io.loadmat(fname)

# returns a dataclass to act as a struct
def struct():
    return dclass

# sets/creates a field in the struct tgt 
def setfield(tgt, field, val):
    setattr(tgt, field, val)
    return tgt

# exits the program with an error message
def error(msg):
    print(msg)
    sys.exit()

# calls scipy's group_delay function
# array of ones is used for denominators 
# very very minimal, only works for ETHEX use case
def grpdelay(arr):
    w, gd = sig.group_delay((arr.flatten(), np.ones(len(arr))))
    return [round(val) for val in gd]

# returns a colormap array for a given number of colors (num)
def hsv(num):
    hsv = matplotlib.cm.get_cmap()
    return hsv(num)

# converts a cell array into a normal array
def cell2mat(arr):
    arr = np.array(arr)
    return np.concatenate(arr).astype(arr[0].dtype)

# returns the linear indices of all non-zero values in arr
def find(arr):
    arr = np.array(arr).flatten('F')
    return [idx for idx, val in enumerate(arr) if val != 0]

# Compares s1 and s2 and returns true if they are identical.
# If s1 is an array/matrix, an array/matrix of the same shape
# will be returned with cooresponding 1s and 0s at each location
# depending on whether or not s2 exists at that spot in s1. 
# Note: assume s1 does not excede 2D
def strcmp(s1, s2): 
    if type(s1) is str:
        return s1 == s2
    
    s1 = np.array(s1)
    ret = np.zeros(s1.shape)

    if len(ret.shape) == 1:
        for idx, val in enumerate(s1):
            if val == s2:
                ret[idx] = 1

    else:
        for idx, row in enumerate(s1):
            for idy, val in enumerate(row):
                if val == s2:
                    ret[idx][idy] = 1

    return ret
