import java.util.concurrent.Semaphore;

class FooBar {
  int n;
  Semaphore fooRendezvous;
  Semaphore barRendezvous;

  public FooBar(int n) {
    this.n = n;
    this.fooRendezvous = new Semaphore(0);
    this.barRendezvous = new Semaphore(0);
  }

  public void foo(Runnable printFoo) throws InterruptedException {
    for (int i = 0; i < n; i++) {
      printFoo.run();
      this.fooRendezvous.release();
      this.barRendezvous.acquire();
    }
  }

  public void bar(Runnable printBar) throws InterruptedException {
    for (int i = 0; i < n; i++) {
      this.fooRendezvous.acquire();
      printBar.run();
      this.barRendezvous.release();
    }
  }
}