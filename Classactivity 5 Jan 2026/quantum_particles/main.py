
import threading
from buffer import buffer, BUFFER_SIZE
from producer import producer
from consumer import consumer

# Semaphores
mutex = threading.Semaphore(1)          # mutual exclusion
empty = threading.Semaphore(BUFFER_SIZE)  # empty slots
full  = threading.Semaphore(0)          # filled slots

if __name__ == "__main__":
    producers = []
    NUM_PRODUCERS = 3

    # Start producer threads
    for i in range(NUM_PRODUCERS):
        t = threading.Thread(
            target=producer,
            args=(i, buffer, mutex, empty, full),
            daemon=True
        )
        producers.append(t)
        t.start()

    # Start consumer thread
    consumer_thread = threading.Thread(
        target=consumer,
        args=(buffer, mutex, empty, full),
        daemon=True
    )
    consumer_thread.start()

    # Keep main thread alive
    for t in producers:
        t.join()
    consumer_thread.join()
