# Out-of-Core Group By Aggregate

*Due Wed June 1, 11:59 pm*

In this assignment, you will implement an out-of-core
version of the group by aggregate (aggregation by key)
seen in lecture. You will have a set memory limit and 
you will have to count the number of times a string shows 
up in an iterator. Your program should work for any limit 
greater than 20.

## Getting Started
Now, you will need to fetch the data used in this assignment. Download title.csv put it in the hw5 folder:

https://www.dropbox.com/s/zl7yt8cl0lvajxg/title.csv?dl=0

DO NOT ADD title.csv to the git repo! After downloading the 
dataset, there is a python module provided for you called `core.py`, which reads the dataset. This module loads the data in as
an iterator in two functions `imdb_years()` and `imdb_title_words()`:
```
>> for i in imdb_years():
... print(i)

1992
1986
<so on>
```
Play around with both `imdb_years()` and `imdb_title_words()` to get a feel for how the data works. 

## MemoryLimitedHashMap
In this project, the main data structure is the `MemoryLimitedHashMap`. This is a hash map that has an explicit limit on the number of keys it can store. To create one of these data structure, you can import it from core module:
```
from core import *
#create a memory limited hash map
m = MemoryLimitedHashMap()
```
To find out what the limit of this hash map is, you can:
```
print("The max size of m is: ", m.limit)
```
The data structure can be constructed with an explicit limit (the default is 1000), e.g., `MemoryLimitedHashMap(limit=10)`.
Adding data to this hash map is like you've probably seen before in a data structure class. There is a `put` function that takes in a key and assigns that key a value:
```
# put some keys
m.put('a', 1)
m.put('b', 45)
print("The size of m is: ", m.size())
```
You can fetch the data using the `get` function and `keys` function:
```
# get keys
for k in m.keys():
    print("The value at key=", k, 'is', m.get(k))    

# You can test to see if a key exists
print('Does m contain a?', m.contains('a'))
print('Does m contain c?', m.contains('c'))
```
When a key does not exist in the data structure the `get` function will raise an error:
```
#This gives an error: 
m.get('c')
```
Similarly, if you assign too many unique keys (more than the limit) you will get an error:
```
for i in range(0,1001):
    m.put(str(i), i)
```
The `MemoryLimitedHashMap` allows you to manage this limited storage with a `flush` function that allows you to persist a key and its assignment to disk. When you flush a key it removes it from the data structure and decrements the limit. Flush takes a key as a parameter.
```
m.flushKey('a')
print("The size of m is: ", m.size())
```
Note that the disk is not intelligent! If you flush a key multiple times it simply appends the flushed value to a file on disk:
```
m.flushKey('a')
<some work...>
m.flushKey('a')
```
Once a key has been flushed it can be read back using the `load` function (which takes a key as a parameter). This loads back *all* of the flushed values:
```
#You can also load values from disk
for k,v in m.load('a'):
    print(k,v)
```
If you try to load a key  that has not been flushed, you will get an error:
```
#Error!!
for k,v in m.load('d'):
	print(k,v)
```

If you want multiple flushes of the same key to be differentiated, you can set a *subkey*:
```
#first flush
m.flushKey('a', '0')

<some work...>

#second flush
m.flushKey('a', '1')
```
The `load` function allows you to selectively pull 
certain subkeys:
```
# pull only the first flush
m.load('a', '0')
```

We can similarly iterate over all of the flushed data (which optionally takes a subkey as well!):
```
for k,v in m.loadAll():
    print(k,v)
```
It also takes in an optional parameter that includes the in memory keys as well:
```
for k,v in m.loadAll(subkey='myskey', inMemory=True):
    print(k,v)
```

Since there are some keys in memory and some flushed to disk there are two commands to iterate over keys.
```
m.keys() #returns all keys that are in memory
```
There is also a way to iterate over all of the flushed keys (will strip out any subkeys):
```
m.flushed() #return keys that are flushed.
```

## Count Per Group
In this assignment, you will implement an out-of-core count operator which for all distinct strings in an iterator returns
the number of times it appears (in no particular order). 
For example,
```
In: "the", "cow", "jumped", "over", "the", "moon"
Out: ("the",2), ("cow",1), ("jumped",1), ("over",1), ("moon",1)
```
Or,
```
In: "a", "b", "b", "a", "c"
Out: ("c",1),("b",2), ("a", 2) 
```
The catch is that you CANNOT use a list, dataframe,  dictionary, or set from 
Python. We provide a general purpose data structure called a MemoryLimitedHashMap (see ooc.py). You must maintain the iterator
state using this data structure. 

The class that you will implement is called Count (in countD.py).
The constructor is written for you, and ittakes in an input iterator and a MemoryLimitedHashMap. You will use these objects
in your implementation. You will have to implement `__next__` and `__iter__`. Any solution using a list, dictionary, or set inside `Count` will recieve 0 points.

The hint is to do this in multiple passes and use a subkey to track keys flushed between different passes.

## Testing and Submission
 We have provided a series of basic tests in `auto_grader.py`, these tests are incomplete and are not meant to comprehensively grade your assignment. There is a file `years.json` with an expected output. After you finish the assignment you can submit your code with:
```
$ git push
```
