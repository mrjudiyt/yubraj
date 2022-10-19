# Global Interpreter Lock (GIL)
# 
# Python doesn't allow multi-threading in the truest sense of the word. It has a multi-threading package
# but if you want to multi-thread to speed your code up, then it's usually not a good idea to use it.
# Python has a construct called the Global Interpreter Lock (GIL).
# The GIL makes sure that only one of your 'threads' can execute at any one time.
# A thread acquires the GIL, does a little work, then passes the GIL onto the next thread.
# This happens very quickly so to the human eye it may seem like your threads are executing in parallel,
# but they are really just taking turns using the same CPU core.
# All this GIL passing adds overhead to execution.
# This means that if you want to make your code run faster then using the threading
# package often isn't a good idea.

# There are reasons to use Python's threading package.
# If you want to run some things simultaneously, and efficiency is not a concern,
# then it's totally fine and convenient.
# Or if you are running code that needs to wait for something (like some IO) then it could make a lot of sense.
# But the threading library won't let you use extra CPU cores.

# Multi-threading can be outsourced to the operating system (by doing multi-processing),
# some external application that calls your Python code (eg, Spark or Hadoop), or some code that your Python
# code calls (eg: you could have your Python code call a C function that does the expensive multi-threaded stuff).

# Why This Matters
# Because the GIL is an A-hole. Lots of people spend a lot of time trying to find bottlenecks in their fancy
# Python multi-threaded code before they learn what the GIL is.

# Once this is clear...
# Let's get our hands dirty :)

#!/bin/python
from multiprocessing.dummy import Pool
from subprocess import PIPE,Popen
import time
import os

__author__ = "Davide Nastri"
__version__ = "0.1.0"
__license__ = "MIT"

pool_size = 5

def do_ping(ip):
    if os.name == 'nt':
        print ("Using Windows Ping to " + ip)
        proc = Popen(['ping', ip], stdout=PIPE)
        return proc.communicate()[0]
    else:
        print ("Using Linux Ping to " + ip)
        proc = Popen(['ping', ip, '-c', '4'], stdout=PIPE)
        return proc.communicate()[0]


os.system('cls' if os.name=='nt' else 'clear')
print ("Running using threads\n")
start_time = time.time()
pool = Pool(pool_size)
website_names = ["www.davidenastri.it", "www.google.com","www.facebook.com","www.pinterest.com","www.microsoft.com"]
result = {}
for website_name in website_names:
    result[website_name] = pool.apply_async(do_ping, args=(website_name,))
pool.close()
pool.join()
print ("\n--- Execution took {} seconds ---".format((time.time() - start_time)))

# Now we do the same without threading, just to compare time
print ("\nRunning NOT using threads\n")
start_time = time.time()
for website_name in website_names:
    do_ping(website_name)
print ("\n--- Execution took {} seconds ---".format((time.time() - start_time)))

# Here's one way to print the final output from the threads
output = {}
for key, value in result.items():
    output[key] = value.get()
print ("\nOutput aggregated in a Dictionary:")
print (output)
print ("\n")

print ("\nPretty printed output:")
for key, value in output.items():
    print (key + "\n")
    print (value)