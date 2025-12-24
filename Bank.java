// public class Bank {
//     private int balance = 0;

//     public void deposit() {
//         balance += 100;
//     }

//     public void withdraw() {
//         balance -= 100;
//     }

//     public int getValue() {
//         return balance;
//     }

//     public void runThread(String threadName) {
//         deposit();
//         System.out.println("Value for Thread after deposit " + threadName + ": " + getValue());
//         withdraw();
//         System.out.println("Value for Thread after withdraw " + threadName + ": " + getValue());
//     }
// }
public class Bank {
    private int balance = 0;

    public synchronized void deposit() {
        balance += 100;
    }

    public synchronized void withdraw() {
        balance -= 100;
    }

    public synchronized int getValue() {
        return balance;
    }

    public void runThread(String threadName) {
        deposit();
        System.out.println("Value for Thread after deposit " + threadName + ": " + getValue());
        withdraw();
        System.out.println("Value for Thread after withdraw " + threadName + ": " + getValue());
    }
}
