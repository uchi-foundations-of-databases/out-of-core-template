from countD import *
from core import *
from ooc import *
import json

test_file = open('years.json','r')
expected = json.loads(test_file.read())

for l in range(80, 140, 10):
    m = MemoryLimitedHashMap(limit = l)
    actual = {k:v for k,v in Count(imdb_years(), m)}

    try:
    	assert(expected == actual)
    except:
    	print("[#1] Failed for Memory Limit", l)


