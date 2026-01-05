
import time
import random

def consumer(buffer, mutex, empty, full):
    """
    Consumer thread:
    - removes two particles at a time
    - packages and ships them
    """
    while True:
        # Wait until two particles exist
        full.acquire()
        full.acquire()

        # Critical section
        mutex.acquire()
        P1 = buffer.pop(0)
        P2 = buffer.pop(0)
        print(f"[Consumer] Packaged {P1}, {P2}")
        mutex.release()

        # Signal two empty slots
        empty.release()
        empty.release()

        time.sleep(random.uniform(0.2, 0.6))
