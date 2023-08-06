#!/usr/bin/env python


import sys

try:
    from _thread import start_new_thread, allocate_lock
except ImportError:
    from thread import start_new_thread, allocate_lock

import subprocess
import time
import os

# Configs
totalLen = 0
max_threads = 1
command = ["ls"]

# Initiate
lock = allocate_lock()
devnull = open(os.devnull, 'w')
active_threads = 0
spawns = 0


def print_process(message):
    global totalLen

    sys.stdout.write("\r")
    if (len(message) < totalLen):
        sys.stdout.write('%s' % (" " * totalLen))
        totalLen = len(message)

    sys.stdout.write(message)
    sys.stdout.flush()




def worker():
    global active_threads, lock, command, spawns

    lock.acquire()
    active_threads += 1
    spawns += 1
    lock.release()

    subprocess.run(command, stdout=devnull)

    lock.acquire()
    active_threads -= 1
    lock.release()

def run(cmd, threads):
    global max_threads, command

    max_threads = threads
    command = cmd

    print("Enter ctrl+c to stop...")
    print("Command: ", command)
    while True:
        print_process("Status: %s/%s active threads (%s spawns)" % (active_threads, max_threads, spawns))
        if active_threads < max_threads:
            start_new_thread(worker, ())
        time.sleep(1)
