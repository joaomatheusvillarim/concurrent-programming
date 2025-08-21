# bakery lock

## implementação

```java

public class BakeryLock implements Lock {

  boolean[] flag;
  Label[] label;
  int n;

  public BakeryLock(int n) {
    flag = new boolean[n];
    label = new Label[n];
    n = n;
  }

  public void lock() {
    int i = ThreadID.get();

    flag[i] = true;
    label[i] = max(flag[0 : n-1]) + 1;

    while (checkLockCondition(i)) {
      //spin-lock
    }
  }

  private boolean checkLockCondition(int i) {
    // (exists k != i | flag[k]=true && (label[k], k) << label[i], i)
    boolean resp = false;
    for (int j = 0; j < n; j++) {
      if (i != j) {
        if (flag[j] && (label[j] < label[i] || (label[j] == label[i] && j < i))) {
          resp = true;
        }
      }
    }
    return resp;
  }

}

```

## *the art of multiprocessor programming*
