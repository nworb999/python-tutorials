# Race conditions can occur when two or more threads access
# a shared piece of data or resource.

import time
import logging
import threading
import concurrent.futures

class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    database = FakeDatabase()
    logging.info("Testing update.  Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info("Testing update. Ending value is %d.", database.value)

# This program creates a ThreadPoolExecutor with two threads and then calls 
# .submit() on each of them, telling them to run database.update()

# .submit() has a signature that allows both positional and named arguments to 
# be passed to the function running in the thread

    # .submit(function, *args, **kwargs)

# In the usage above, index is passed as the first and only positional argument 
# to database.update()

# Each of the threads in the pool will call database.update(index)
# Note that database is a reference to the one FakeDataBase object created
# in __main__.  Calling .update() on that object calls an instance method
# on that object.  

    # Each thread is going to have a reference to the same
    # FakeDatabase object, database.  Each thread will also have a unique 
    # value, index, to make the logging statements a bit easier to read.

    # When the thread starts running .update(), it has its own
    # version of all the data local to the function (local_copy)
    # This means that all variables scoped to a function are thread-safe.

# There are a number of ways to avoid or solve race conditions, starting 
# with Lock.
    
    # For the above code, only one thread at a time must be allowed into the
    # read-modify-write section of your code.
    # A Lock is an object that acts like a hall pass, only one thread
    # at a time may bear one.  The basic functions to do this are 
    # .acquire() and .release()
    # A tread will call my_lock.acquire() to get a lock.  If one
    # thread gets the lock but never gives it back, your program will be stuck.

    # Python's lock also operates as a context manager, so you can 
    # use it in a with statement and it gets release automatically when the with
    # block exits for any reason.

# A Lock provides mutual exclusion.
# Deadlocks happen from one of two subtle things:
    # 1. An implementation bug where a Lock is not released properly
    # 2. A design issue where a utility function needs to be called by
    # functions that might or might not already have the Lock

# Context managers avoid 1 because they help to avoid situations
# where an exception skips over the .release() call

# Python threading has a second object, called RLock, that is designed
# for just this situation.  It allows a thread to .acquire() an RLock 
# multiple times before it calls .release()
# That thread is still required to call .release() the same number
# of times it called a .acquire(), but it should be doing that anyway

