# barrier

## the little book of semaphores
"Consider again the Rendezvous problem from Section 3.3. A limitation of the solution we presented is that it does not work with more than two threads.  
Puzzle: Generalize the rendezvous solution. Every thread should run the following code:
```python
rendezvous()
critical_point()
```
The synchronization requirement is that no thread executes critical point until after all threads have executed rendezvous.  
You can assume that there are n threads and that this value is stored in a variable, n, that is accessible from all threads.  
When the first n − 1 threads arrive they should block until the nth thread arrives, at which point all the threads may proceed."

## my implementation

```python
#shared variables
barrier = Semaphore(0)
count = 0
mutex = Semaphore(1)
```
```python
#threads a, b, ..., n
prepare() #rendezvous

mutex.wait()
count += 1
if count == n:
  barrier.signal()
mutex.signal()

barrier.wait()
barrier.signal()

run() #critical point
```
you may notice that the if statement is inside the section protected by the mutex, that is to ensure only one thread executes it with count equal to n.