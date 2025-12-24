public class Main {
    public static void main(String[] args) {
        Bank bank = new Bank();

        // Create threads using Runnable
        Thread t1 = new Thread(() -> bank.runThread("Thread1"));
        Thread t2 = new Thread(() -> bank.runThread("Thread2"));
        Thread t3 = new Thread(() -> bank.runThread("Thread3"));

        // Start threads
        t1.start();
        t2.start();
        t3.start();

        // Wait for threads to finish
        try {
            t1.join();
            t2.join();
            t3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
