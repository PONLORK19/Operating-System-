import threading
import time

class BankAccount:
    """Represents a bank account with a balance and a lock"""
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Semaphore(1)  # Binary semaphore (acts as mutex)
    
    def __str__(self):
        return f"Account {self.account_id}: ${self.balance}"

# ============================================================================
# VERSION 1: DEADLOCK PROBLEM (Naive approach)
# ============================================================================

def transfer_with_deadlock(from_account, to_account, amount, thread_name):
    """
    PROBLEMATIC VERSION: This can cause deadlock!
    Locks are acquired in the order they are passed
    """
    print(f"\n[{thread_name}] Attempting transfer ${amount}: {from_account.account_id} → {to_account.account_id}")
    
    # Acquire first lock
    print(f"[{thread_name}] Waiting for lock on Account {from_account.account_id}...")
    from_account.lock.acquire()
    print(f"[{thread_name}] ✓ Acquired lock on Account {from_account.account_id}")
    
    time.sleep(0.1)  # Simulate processing to increase deadlock chance
    
    # Acquire second lock - DEADLOCK RISK HERE!
    print(f"[{thread_name}] Waiting for lock on Account {to_account.account_id}...")
    to_account.lock.acquire()
    print(f"[{thread_name}] ✓ Acquired lock on Account {to_account.account_id}")
    
    # Critical section
    if from_account.balance >= amount:
        from_account.balance -= amount
        to_account.balance += amount
        print(f"[{thread_name}] SUCCESS! Transfer completed.")
    else:
        print(f"[{thread_name}] FAILED! Insufficient funds")
    
    # Release locks
    to_account.lock.release()
    from_account.lock.release()
    print(f"[{thread_name}] Released all locks")

# ============================================================================
# VERSION 2: SOLUTION - Fixed Lock Ordering
# ============================================================================

def transfer_with_solution(from_account, to_account, amount, thread_name):
    """
    SOLUTION: Always acquire locks in a fixed global order!
    This prevents circular wait and eliminates deadlock.
    """
    print(f"\n[{thread_name}] Attempting transfer ${amount}: {from_account.account_id} → {to_account.account_id}")
    
    # SOLUTION: Determine lock order based on account ID (not parameter order)
    # Always lock the account with smaller ID first
    first_lock = min(from_account, to_account, key=lambda acc: acc.account_id)
    second_lock = max(from_account, to_account, key=lambda acc: acc.account_id)
    
    print(f"[{thread_name}] Lock order: {first_lock.account_id} → {second_lock.account_id}")
    
    # Acquire locks in fixed order
    print(f"[{thread_name}] Waiting for lock on Account {first_lock.account_id}...")
    first_lock.lock.acquire()
    print(f"[{thread_name}] ✓ Acquired lock on Account {first_lock.account_id}")
    
    time.sleep(0.1)  # Simulate processing
    
    print(f"[{thread_name}] Waiting for lock on Account {second_lock.account_id}...")
    second_lock.lock.acquire()
    print(f"[{thread_name}] ✓ Acquired lock on Account {second_lock.account_id}")
    
    # Critical section
    if from_account.balance >= amount:
        from_account.balance -= amount
        to_account.balance += amount
        print(f"[{thread_name}] SUCCESS! Transfer completed.")
    else:
        print(f"[{thread_name}] FAILED! Insufficient funds")
    
    # Release locks
    second_lock.lock.release()
    first_lock.lock.release()
    print(f"[{thread_name}] Released all locks")

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def run_deadlock_version():
    """Run the version that causes deadlock"""
    print("\n" + "="*70)
    print("VERSION 1: DEADLOCK PROBLEM")
    print("="*70)
    
    # Reset accounts
    account1 = BankAccount(6005, 1000)
    account2 = BankAccount(6004, 1000)
    
    print(f"\nInitial state:")
    print(f"  {account1}")
    print(f"  {account2}")
    
    def thread1():
        transfer_with_deadlock(account1, account2, 50, "Thread-1")
    
    def thread2():
        transfer_with_deadlock(account2, account1, 50, "Thread-2")
    
    t1 = threading.Thread(target=thread1, name="Thread-1")
    t2 = threading.Thread(target=thread2, name="Thread-2")
    
    print("\nStarting concurrent transfers...")
    t1.start()
    t2.start()
    
    # Wait with timeout
    t1.join(timeout=3.0)
    t2.join(timeout=3.0)
    
    if t1.is_alive() or t2.is_alive():
        print("\n" + "="*70)
        print("💀 DEADLOCK DETECTED! 💀")
        print("="*70)
        print("\nProblem Analysis:")
        print("  • Thread-1: Locked 6005, waiting for 6004")
        print("  • Thread-2: Locked 6004, waiting for 6005")
        print("  • Circular wait = DEADLOCK (deadly embrace)!")
        print("="*70)
    else:
        print("\n✓ No deadlock (this time)")
    
    return account1, account2

def run_solution_version():
    """Run the version with deadlock prevention"""
    print("\n\n" + "="*70)
    print("VERSION 2: DEADLOCK SOLUTION")
    print("="*70)
    print("\nSolution: Fixed Lock Ordering")
    print("  → Always acquire locks in order of account ID")
    print("  → This breaks the circular wait condition!")
    print("="*70)
    
    # Reset accounts
    account1 = BankAccount(6005, 1000)
    account2 = BankAccount(6004, 1000)
    
    print(f"\nInitial state:")
    print(f"  {account1}")
    print(f"  {account2}")
    
    def thread1():
        transfer_with_solution(account1, account2, 50, "Thread-1")
    
    def thread2():
        transfer_with_solution(account2, account1, 50, "Thread-2")
    
    t1 = threading.Thread(target=thread1, name="Thread-1")
    t2 = threading.Thread(target=thread2, name="Thread-2")
    
    print("\nStarting concurrent transfers...")
    t1.start()
    t2.start()
    
    # Wait for completion
    t1.join()
    t2.join()
    
    print("\n" + "="*70)
    print("✓ ALL TRANSFERS COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\nFinal state:")
    print(f"  {account1}")
    print(f"  {account2}")
    print("\nNo deadlock occurred because both threads always")
    print("acquire locks in the same order (6004 before 6005)!")
    print("="*70)
    
    return account1, account2

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("DEADLOCK SIMULATION: Problem & Solution")
    print("="*70)
    
    # Run deadlock version
    run_deadlock_version()
    
    # Give some time before running solution
    time.sleep(1)
    
    # Run solution version
    run_solution_version()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS:")
    print("="*70)
    print("1. PROBLEM: Naive locking in arbitrary order → Deadlock")
    print("2. SOLUTION: Fixed global lock ordering → No deadlock")
    print("3. This implements the 'cooperating processes' approach")
    print("   from your slide: establish fixed ordering for resources!")
    print("="*70)