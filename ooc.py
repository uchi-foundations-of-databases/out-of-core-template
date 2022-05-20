import os
import json

class MemoryLimitedHashMap(object):
  '''
  A MemoryLimitedHashMap simulates a hardware memory limit for a 
  key-value data structure. It will raise an exception if the 
  limit is exceeded.

  Keys must be strings
  '''

  def __init__(self, diskfile='disk.file', limit=1000):
    '''
    The constructor takes a reference to a persistent file
    and a memory limit.
    '''

    if os.path.exists(diskfile):
        print("[Warning] Overwriting the Disk File", diskfile)

        import shutil
        shutil.rmtree(diskfile) 

    os.mkdir(diskfile)
    self.diskfile = diskfile
    self._data = {}
    self.limit = limit

  def size(self):
    return len(self._data)

  def put(self, k, v):
    '''
    Basically works like dict put
    '''

    if not self.contains(k) and len(self._data) == self.limit:
      raise ValueError("[Error] Attempting to Insert Into a Full Map: " + str((k,v)))
    else:
      self._data[k] = v


  def get(self, k):
    '''
    Basically works like dict get
    '''

    return self._data[k]


  def contains(self, k):
    '''
    Basically works like hash map contains
    '''

    return (k in self._data)


  def keys(self):
    '''
    Returns a set of keys (in memory). Tuple
    is (key, location)
    '''

    return set([k for k in self._data])


  def flushed(self, returnSubKeys=False):
    '''
    Returns a set over keys that have been flushed. 
    Tuple is (key, location)
    
    if returnSubKeys=True
    The tuple is ((key,subkey), location), if no subkey is provided it's just 
    (key)
    '''
    
    if not returnSubKeys:    
        return set([self.path2Key(k) for k in os.listdir(self.diskfile)])
    else:
        return set([self.path2Subkey(k) for k in os.listdir(self.diskfile)])

  def keyPath(self, k, subkey):
    return self.diskfile+"/"+str(k)+ "_" + subkey

  def path2Key(self, k):
    key = k.split("_")[0]
    return key

  def path2Subkey(self, k):
    key = tuple(k.split("_"))
    return key

  def flushKey(self, k, subkey=""):
    '''
    Removes the key from the dictionary and 
    persists it to disk.
    '''
    if not self.contains(k):
        raise ValueError("[Error] Map Does Not Contain " + k)

    f = open(self.keyPath(k, subkey), 'a')
    f.write(json.dumps(self.get(k)) + "\n")
    f.close()

    del self._data[k] #free up the space


  def load(self, k, subkey=""):
    '''
    Streams all of the data from a persisted key 
    '''
    fname = self.keyPath(k, subkey)

    if not os.path.exists(fname):
        raise ValueError("[Error] Disk Does Not Contain " + k)

    f = open(fname, 'r')
    
    line = f.readline()

    while line != "":
        yield (k, json.loads(line.strip()))
        line = f.readline()

  
  def loadAll(self, subkey="", inMemory=False):
    '''
    Streams all of the data from all keys
    '''

    if inMemory:
        for k in self.keys():
            yield (k, self.get(k))

    for k in self.flushed():
        for _,v in self.load(k, subkey):
            yield (k,v)