# turnstile (reusable barrier)

## the little book of semaphores
Often a set of cooperating threads will perform a series of steps in a loop and synchronize at a barrier after each step. For this application we need a reusable barrier that locks itself after all the threads have passed through.  
Puzzle: Rewrite the barrier solution so that after all the threads have passed through, the turnstile is locked again.

## my implementation
```python
#shared variables
turnstile = Semaphore(0)
turnstile2 = Semaphore(1)
count = 0
mutex = Semaphore(1)
```
```python
#threads a, b, ..., n
prepare()

mutex.wait()
count += 1
if count == n:
  turnstile2.wait() #locks the second turnstile
  turnstile.signal() #unlocks the first turnstile
mutex.signal()

turnstile.wait()
turnstile.signal()

run()

mutex.wait()
count -= 1
if count == 0:
  turnstile.wait() #locks the first turnstile
  turnstile2.signal() #unlocks the second turnstile
mutex.signal()

turnstile2.wait()
turnstile2.signal()
```