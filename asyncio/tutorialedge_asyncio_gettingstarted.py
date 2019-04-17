# Asyncio allows you to easily write single-threaded concurrent programs that utilize something called
# coroutines, which are stripped down threads that don't come with the same inherit performance issues 
# that your full-fat threads would typically come with

# Abstracts away the complexity of things such as multiplexing I/O access over sockets and it also 
# simplifies tasks by providing an arsenal of synchronization primitives that enable us to make our 
# programs thread-safe

# All asyncio-based systems require an event loop, which schedules our asyncio.coroutines and handles all
# the heavy lifting

# Futures in asyncio are very similar to ThreadPoolExecutors or ProcessPoolExecutors in Future objects
# They allow you to perform other tasks in your Python program whilst you are waiting for your Future to return a result

# Thankfully working with Futures in asyncio is relatively easy thanks to the ensure_future() method which 
# takes in a coroutine and returns the Future version of that coroutine

import asyncio
import random

async def myCoroutine(id):
    process_time = random.randint(1,5)
    await asyncio.sleep(process_time)
    print("Coroutine: {}, has successfully completed after {} seconds".format(id, process_time))

async def main():
    tasks = []
    for i in range(10):
        tasks.append(asyncio.ensure_future(myCoroutine(i)))

    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()

