import java.util.concurrent.Semaphore;
import java.util.function.IntConsumer;

class ZeroEvenOdd {
  int n;
  Semaphore zeroSemaphore = new Semaphore(1);
  Semaphore oddSemaphore = new Semaphore(0);
  Semaphore evenSemaphore = new Semaphore(0);
    
  public ZeroEvenOdd(int n) {
    this.n = n;
  }

  public void zero(IntConsumer printNumber) throws InterruptedException {
    for (int i = 1; i <= n; i++) {
      this.zeroSemaphore.acquire();
      printNumber.accept(0);

      if (i % 2 == 1) {
        oddSemaphore.release();
      } else {
        evenSemaphore.release();
      }
    }
  }

  public void odd(IntConsumer printNumber) throws InterruptedException {
    for (int i = 1; i <= n; i += 2) {
      oddSemaphore.acquire();
      printNumber.accept(i);
      zeroSemaphore.release();
    }
  }

  public void even(IntConsumer printNumber) throws InterruptedException {
    for (int i = 2; i <= n; i += 2) {
      evenSemaphore.acquire();
      printNumber.accept(i);
      zeroSemaphore.release();
    }
  }
}