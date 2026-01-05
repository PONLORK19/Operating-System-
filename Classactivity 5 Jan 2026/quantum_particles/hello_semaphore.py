import threading

# Semaphores (initial values)
a = threading.Semaphore(1)   # Process 1 starts
b = threading.Semaphore(0)   # Process 2 waits
c = threading.Semaphore(0)   # Process 3 waits


def process1():
    # Loop1
    a.acquire()          # wait(a)
    print("H", end="")
    print("E", end="")
    b.release()          # signal(b)


def process2():
    # Loop2
    b.acquire()          # wait(b)
    print("L", end="")
    print("L", end="")
    c.release()          # signal(c)


def process3():
    # Loop3
    c.acquire()          # wait(c)
    print("O", end="")


if __name__ == "__main__":
    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    t3 = threading.Thread(target=process3)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print()  # newline
