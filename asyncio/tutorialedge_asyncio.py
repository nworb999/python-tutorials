# The main component of any asyncio based Python program has to be the
# underlying event loop

# Within this event loop we can 
    # Register, execute and cancel calls
    # Launch subprocesses and the associated transports for communication with 
    # an external program
    # Delegate costly function calls to a pool of threads

# Essentially all an event loop does is wait for events to happen before matching
# each event to a function that we hvae explicitly matched with said type of event

# A classic example is a simple web server
    # Say tere is an endpoint in our server that serves our website which features a 
    # multitude of different pages

    # Our event loop essentially listens for requests to be made and then matches each
    # of these requests to its associated webpage

    # Each of the requests made to the server would be considered a separate event,
    # which would then be matched to a set function that we have predefined whenever a said event 
    # is triggered

# To define a very simple event loop, we will use asyncio.get_event_loop(), we'll then start a 
# try .. finally and within the body of our try we will specify that we want our newly instantiated 
# event loop to run until it has completed our myCoroutine() function

import asyncio
import time

# Define a coroutine that takes in a future
async def myCoroutine():
    print('My coroutine rules :)')

# Spin up a quick and simple event loop and run until completed
print('Initializing event loop!')
loop = asyncio.get_event_loop()
print('Sleeping for a sec!')
time.sleep(4)
try:
    loop.run_until_complete(myCoroutine())
finally:
    loop.close()
    print('Loop finished!')

