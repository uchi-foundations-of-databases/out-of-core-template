from core import *
from ooc import *

"""
Get the dataset first, download title.csv put it in the pa1 folder
https://www.dropbox.com/s/zl7yt8cl0lvajxg/title.csv?dl=0

Count the number of times each symbol shows up in an iterator
with limited memory. Your program should work for any limit 
> 20.
"""

class Count:
    """
    In this assignment, you will implement an out-of-core count 
    operator which for all distinct strings in an iterator returns
    the number of times it appears (in no particular order). 
    For example,

    In: "the", "cow", "jumped", "over", "the", "moon"
    Out: ("the",2), ("cow",1), ("jumped",1), ("over",1), ("moon",1)

    Or,

    In: "a", "b", "b", "a", "c"
    Out: ("c",1),("b",2), ("a", 2) 

    The catch is that you CANNOT use a list, dictionary, or set from 
    python. We provide a general purpose data structure called a 
    MemoryLimitedHashMap (see ooc.py). You must maintain the iterator
    state using this data structure. 
    """

    def __init__(self, input, memory_limit_hashmap):
        '''
        The constructor takes in an input iterator and
        a MemoryLimitedHashMap. You will use these objects
        in your implementation.
        '''
        self.in1 = input
        self.hashmap = memory_limit_hashmap
        
    def __iter__(self):
        raise NotImplemented("You must implement an initializer")


    def __next__(self):
        raise NotImplemented("You must implement a next function")




