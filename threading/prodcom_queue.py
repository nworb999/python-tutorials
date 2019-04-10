import logging
import threading
import time
import concurrent.futures
import queue
import random

# Producer-Consumer using queue -- if you want to be able to 
# handle more than one value in the pipeline at a time, you need
# a data structure from the pipeline that allows the number to grow
# and shrink as data backs up from the producer

    # We will change the Pipeline class to use a Queue class
    # instead of just a variable protected by a Lock

    # We will also use a different way to stop the worker threads
    # by using a different primitive from Python threading, 
    # an Event
    # The threading.Event object allows one thread to signal an event 
    # while many other threads can be waiting for that event to happen
    # The key usage in this code is that the threads that are waiting for
    # the event do not necesssarily need to stop what they are doing, they
    # can just check the status of the Event every once in a while

    # The triggering of the event can be many things
    # In this example, the main thread will simply sleep for a while and 
    # then .set() it

def producer(pipeline, event):
    """Retrieves number from the network.
    """
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")

    logging.info("Producer received EXIT event. Exiting")

def consumer(pipeline, event):
    """Saves a number in the database.
    """
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        logging.info(
            "Consumer storing message: %s (queue size=%s)",
            message,
            pipeline.qsize(),
        )

    logging.info("Consumer received EXIT event. Exiting")

# While the code related to the SENTINEL value has bene removed,
# the while condition got slightly more complicated.  It loops until the
# event is set, and until the pipeline has been emptied.

class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug("%s:about to get from queue", name)
        value = self.get()
        logging.debug("%s:got %d from queue", name, value)
        return value

    def set_message(self, value, name):
        logging.debug("%s:about to add %d to queue", name, value)
        self.put(value)
        logging.debug("%s:added %d to queue", name, value)

# Pipeline is a subclass of queue
# Maxsize blocks .put() until there are fewer than maxsize elements
# in the queue

# .get_message() and .set_message() got much smaller, they basically
# wrap .get() and .put() on the Queue -- Queue is thread-safe


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()


# Threads don't get blocked by the queue, but swapped out by 
# the OS -- different queue sizes and sleep sizes produce different
# results

# THREADING OBJECTS
# There are a few more primitives offered by the Python threading module

# SEMAPHORE
# The threading.Semaphore is a counter with a few special properties
# The first property is that counting is atomic, meaning that there is a 
# guarantee that the operating system will not swap out the thread in the middle 
# of incrementing or decrementing the counter
# The internal counter is incremented when you call .release()
# and decremented when you call .acquire()
# The next special property is that if a thread calls .acquire()
# when the counter is zero, that thread will block until a different
# thread calls .release() and increments the counter to one
# Semaphores are frequently used to protect a resource that has a limited 
# capacity -- an example would be if you have a pool of connections and want
# to limit the size of that pool to a specific number

# TIMER
# The threading.Timer is a way to schedule a function to be called
# after a certain amount of time has passed -- you create a timer by 
# passing in a number of seconds to wait and a function to call

t = threading.Timer(30.0, my_function)

# You start the Timer by calling .start(), and the function will be called
# on a new thread at some point after the specified time, but be aware
# that there is no promise that it will be called exactly at the time you want

# If you want to stop a Timer that you've already started, you can cancel it by
# calling a .cancel() -- it does not produce an exception

# A Timer can be used to prompt a user for action after a specific amount of time

# BARRIER
# A threading.Barrier can be used to keep a fixed number of threads in sync
# When creating a Barrier, the caller must specify how many threads will be
# synchronizing on it
# Each thread calls .wait() on the Barrier, and they all will remain blocked
# until the specified number of threads are waiting, and then they are all released
# at the same time

# One use for a Barrier is to allow a pool of threads to initialize themselves
# Having the threads wait on a Barrier after they are initialized will ensure
# that none of the threads start running before all of the threads are finished
# with their initialization
