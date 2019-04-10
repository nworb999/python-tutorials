# Threading allows for different parts of your program 
# to run concurrently

    # A thread is a separate flow of execution.
    # For most python implementations, different threads
    # merely appear to execute at the same time
    # The threads may be running on different porcessors,
    # but they will only be running one at a time.

    # The Python Global Interpreter Lock, or GIL,
    # is a mutex that allows only one thread to hold
    # control of the python interpreter.

    # Tasks that spend much of their time waiting for 
    # external events are generally good candidates for 
    # threading.  Problems that require heavy CPU computation
    # and spend little time waiting for external events 
    # might not run faster at all.

    # If your threads are written in C they have the ability 
    # to release the GIL and run concurrently.  Architecting
    # your program to use threading can also provide gains in design clarity.

import logging
import threading
import time

def thread_function(name):
    """ Logs some messages with a 2s sleep in between.
    """
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)
    
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    threads = list()
    for index in range(3):
        logging.info("Main    : create and start thread %d.", index)
        # When you create a Thread, you pass it a function and a list
        # containing the arguments to that function
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        # There is threading.get_ident() which returns a unique name
        # for each thread, but these are usually neither short nor easily 
        # readable
        x.start()
    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index) 
        thread.join()
        logging.info("Main    : thread %d done.", index)

# In computer science, a daemon is a process that runs in the background

# In python threading, a daemon thread will shut down immediately when the 
# program exits
    
    # One way to think about it is to consider the daemon thread
    # a thread that runs in the background without worrying about shutting it down.
    # If a program is running non-daemon threads, the program will
    # wait for those threads to complete before it terminates.  Threads that
    # are daemons, however, are just killed wherever they are when the program
    # is exiting.
    
    # threading._shutdown() walks through all of the running threads
    # and calls .join() on every one that does not have the daemon flag
    # set.  Your program waits to exit because the thread itself is waiting
    # in a sleep -- as soon as it has completed and printed the message,
    # .join() will return and the program can exit

    # What about when you want to wait for a thread to finish?
    # To tell one thread to wait for another to finish, you call .join()
    # If you .join() a thread, that statement will wait until either kind
    # of thread is finished.

# All three threads get started in the order you expect, but they can finish
# in the opposite order.  The order in which threads are run is determined
# by the operating system and can be quite hard to predict.
