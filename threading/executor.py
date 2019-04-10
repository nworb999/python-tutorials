import concurrent.futures
import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))

# There's an easier way to start up a group of threads, called
# ThreadPoolExecutor.  The easiest way is to create it as a context manager,
# using te with statement to manage the creation and destruction of the pool.

# The code creates a ThreadPoolExecutor as a context manager, telling
# it how many worker threads it wants in a pool.  It then uses .map() to
# step through an iterable of things, such as range(), passing each one to a
# thread in a pool.

# The end of the with block causes the ThreadPoolExecutor to do a 
# .join() on each of the threads in the pool.  It is very useful for
# never forgetting to .join() threads.
