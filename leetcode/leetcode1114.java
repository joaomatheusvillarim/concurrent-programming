import java.util.concurrent.Semaphore;

class Foo {

  Semaphore firstIsDone;
  Semaphore secondIsDone;

  public Foo() {
    this.firstIsDone = new Semaphore(0);
    this.secondIsDone = new Semaphore(0);
  }

  public void first(Runnable printFirst) throws InterruptedException {
      
    printFirst.run();
    firstIsDone.release();
  }

  public void second(Runnable printSecond) throws InterruptedException {

    firstIsDone.acquire(); 
    printSecond.run();
    secondIsDone.release();
  }

  public void third(Runnable printThird) throws InterruptedException {

    secondIsDone.acquire();      
    printThird.run();
  }

}