# CONCURRENCY -- like having two threads running on a single core CPU
# Instructions from each thread can be interleaved, but at any given time,
# only one of the two threads is actively making progress

# PARALLELISM -- like having two threads running simultaneously on
# different cores of a multi-core CPU

# Parallelism implies concurrency but not the other way around

# ASYNCHRONOUS -- a higher level programming concept, where you fire off
# some task, and decide that while you don't have the result of that task, you 
# are better off doing some other work instead of waiting

# When you do things asynchronously, you are by definition implying concurrency
# between those things

# The event loop is the orchestrator of the symphony -- it runs tasks
# one after the other

# The event loop time is precious -- if you are not making progress, you should
# step off the loop, so that someone else can

# The event loop is the measure of progress

# Coroutines are a key element of the symphony -- it is the coroutines,
# and their co-operative nature, that enables giving up control of the event loop,
# when the coroutine has nothing useful to do
    # A coroutine is a stateful generalization of the concept of subroutine

# A subroutine is your good old-fashioned function or method,
# you invoke the subroutine to perform a computation -- you make invole it again,
# but it does not hold state between the two invocations, so every invocation
# is a fresh one and the same computation is performed

# A coroutine, on the other hand, is a cute little stateful widget
# It looks like a subroutine, but it maintains state in between executions
    # In other words, when a coroutine 'returns' (yields control) it simply means
    # that it has paused its execution (with some saved stated)
    # So when you 'invoke' (give control to) the coroutine subsequently, it would
    # be correct to say that the coroutine has resumed its execution (from the saved state)

    # Coroutines look like a normal function, but in their behavior they are stateful
    # objects with resume() and pause() -- like methods

# In python, the way a coroutine pauses itself is using the await keyword
# Inside a coroutine, when you await on another coroutine, you step off the event loop
# and schedule the awaited coroutine to run immediately
    # That is, an await other_coroutine inside a coroutine will pause it,
    # and schedule the coroutine other_coroutine to run immediately

# For the below example, we will use a pre-defined coroutine asyncio.sleep
# to help us simulate blocking tasks

import asyncio

async def coroutine_1():
    print('coroutine_1 is active on the event loop')

    print('coroutine_1 yielding control. Going to be blocked for 4 seconds')
    await asyncio.sleep(4)

    print('coroutine_1 resumed. coroutine_1 exiting')

async def coroutine_2():
    print('coroutine_2 is active on the event loop')

    print('coroutine_2 yielding control. Going to be blocked for 5 seconds')
    await asyncio.sleep(5)

    print('coroutine_2 resumed. coroutine_2 exiting')

# this is the event loop
loop = asyncio.get_event_loop()

# schedule both the coroutines to run on the event loop
loop.run_until_complete(asyncio.gather(coroutine_1(), coroutine_2()))

# Important notes

    # Calling a coroutine definition does not execute it, it initializes a coroutine object
        # You await on coroutine objects, not coroutine definition

    # Event loop runs tasks, not coroutine objects directly -- tasks are a wrapper around coroutine
    # objects
        # When you await coroutine_object, you essentially schedule a wrapper task
        # to be run on the event loop immediately

    # asyncio.sleep is a coroutine as well, provided by the asyncio library
        # asyncio.sleep(2) initializes a coroutine object with a value of two seconds

