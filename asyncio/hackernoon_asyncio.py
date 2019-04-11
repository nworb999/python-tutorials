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
