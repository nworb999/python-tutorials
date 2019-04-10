# The Producer-Consumer Problem is a standard computer science
# problem used to look at threading or process synch issues

# Basically, we are writing to a database at a pace that is sometimes
# slower than the bursts the messages/content are often received in.

# In between the producer of messages and the consumer of data, a
# Pipeline is created that will be the part that changes as you learn
# about different synchronization objects

import threading
import logging
import concurrent.futures
import random

SENTINEL = object()


def producer(pipeline):
    """ Receives message from the network.
    """
    for index in range(10):
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")

    # Send a sentinel message to tell consumer we're done
    pipeline.set_message(SENTINEL, "Producer")
    # Producer uses a SENTINEL value to signal the consumer to stop after
    # it has sent ten values


def consumer(pipeline):
    """ Saves number in the database.
    """
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Consumer storing message: %s", message)

    # The consumer reads a message from the pipeline and 'reads
    # it to a fake database', which is just printing it to the display.
    # If it gets the SENTINEL value, it returns from the function,
    # which will terminate the thread.


class Pipeline:
    """ Allows a single element pipeline between producer and consumer.
    """

    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        # Lock object that restricts access to the message by the
        # producer thread
        self.consumer_lock = threading.Lock()
        # Lock object that restricts access to the message by the
        # consumer thread
        self.consumer_lock.acquire()
        # Above is the state you want to start in -- the producer is
        # allowed to add a new message, but the consumer needs to wait
        # until a message is present

    def get_message(self, name):
        # calls .acquire() on the consumer_lock -- this is the call
        # that will make the consumer wait until a message is ready
        logging.debug("%s:about to acquire getlock", name)
        self.consumer_lock.acquire()
        logging.debug("%s:have getlock", name)
        message = self.message
        # This copy ensures that if the producer starts running
        # before the lock is released, the next message is not generated,
        # which would overwrite the first message
        logging.debug("%s:about to release setlock", name)
        self.producer_lock.release()
        # Releasing this lock is what allows the producer to insert
        # the next message into the pipeline
        logging.debug("%s:setlock released", name)
        return message

    def set_message(self, message, name):
        # the producer will call this function with a message, it will
        # acquire the .producer_lock, set the .message, and then call
        # .release() on the consumer_lock, wich will allow the consumer
        # to read that value
        logging.debug("%s:about to acquire setlock", name)
        self.producer_lock.acquire()
        logging.debug("%s:have setlock", name)
        self.message = message
        logging.debug("%s:about to release getlock", name)
        self.consumer_lock.release()
        logging.debug("%s:getlock release", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)
