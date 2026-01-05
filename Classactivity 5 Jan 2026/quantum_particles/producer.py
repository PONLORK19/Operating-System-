
import time
import random

def producer(pid, buffer, mutex, empty, full):
    """
    Producer thread:
    - produces particle pairs
    - inserts two consecutive particles into the buffer
    """
    while True:
        # Produce particle pair
        P1 = f"P{pid}-A"
        P2 = f"P{pid}-B"

        # Wait for two empty slots
        empty.acquire()
        empty.acquire()

        # Critical section
        mutex.acquire()
        buffer.append(P1)
        buffer.append(P2)
        print(f"[Producer {pid}] Produced {P1}, {P2}")
        mutex.release()

        # Signal two filled slots
        full.release()
        full.release()

        time.sleep(random.uniform(0.1, 0.5))
