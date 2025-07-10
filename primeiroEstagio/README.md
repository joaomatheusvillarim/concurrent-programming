# primeiro estágio

## introduction
### synchronization
"In computer systems, synchronization [...] refers to relationships among events — any number of events, and any kind of relationship (before, during, after).
Computer programmers are often concerned with synchronization constraints, which are requirements pertaining to the order of events. Examples include:
* **Serialization**: Event A must happen before Event B.
* **Mutual exclusion**: Events A and B must not happen at the same time."

### execution model
"In the simplest model, computers execute one instruction after another in sequence, which makes synchronization trivial; if Statement A comes before Statement B, it will be executed first.

Therefore, if computer is parallel, meaning that it has multiple processors running at the same time, it is not easy to know if a statement on one processor is executed before a statement on another.  
Beyond that, a single processor could run multiple threads of execution. **A thread is a sequence of instructions that execute sequentially.** If there are multiple threads, then the processor can work on one for a while, then switch to another, and so on.

In general the programmer has no control over when each thread runs; the operating system (specifically, the scheduler) makes those decisions. As a result, again, the programmer can’t tell when statements in different threads will be executed."

### non-determinism
"Concurrent programs are often non-deterministic, which means it is not possible to tell, by looking at the program, what will happen when it executes."

## semaphores
"A semaphore is like an integer, with three differences:
1. When you create the semaphore, you can initialize its value to any non-negative integer, but after that the only operations you are allowed to perform are **increment** and **decrement**. You cannot read the current value of the semaphore.
2. When a thread decrements the semaphore, **if the result is negative, the thread blocks itself and cannot continue until another thread increments** the semaphore.
3. When a thread increments the semaphore, **if there are other threads waiting, one of the waiting threads gets unblocked.**" 

## basic synchronization patterns

### signaling
in the following codes, we can't tell which will run first: a or b
```python
#thread a
a.run()
```
```python
#thread b
b.run()
```
but if we'd like to guarantee that a runs before b, we can use **signaling** for that:
```python
#shared variables
semaphore = Semaphore(0)
```
```python
#thread a
a.run()
semaphore.signal()
```
```python
#thread b
semaphore.wait()
b.run()
```

### *rendezvous*
```python
#thread a
a1.run()
a2.run()
```
```python
#thread b
b1.run()
b2.run()
```
if we'd like to guarantee that a1 runs before b2 and b1 runs before a2, we can use ***rendezvous*** for that:
```python
#shared variables
a1_done = Semaphore(0)
b1_done = Semaphore(0)
```
```python
#thread a
a1.run()
a1_done.signal() "i'm ready"
b1_done.wait() "now i'm waiting for you to be ready"
a2.run()
```
```python
#thread b
b1.run()
b1_done.signal() "i'm ready"
a1_done.wait() "now i'm waiting for you to be ready"
b2.run()
```
be careful, if we switch order of signal and wait in either thread, it could cause a **deadlock**.

### mutex
consider that there are two threads of the following code running:
```python
#threads a and b
count += 1
```
as we know, this code has concurrent updates, which is not an atomic operation, it consists of reading the count variable and then writing it as count + 1. a thread could lose the cpu midst update and the output of two concurrent updates would be as if only one ran. we can solve that with **mutual exclusion** (or mutex, for short):
```python
#shared variables
mutex = Semaphore(1)
```
```python
#threads a and b
mutex.wait()
count += 1 #critical section
mutex.signal()
```
this way, only one thread can access the critical section at a time.

### multiplex
if we want to limit access to the critical section to n threads instead of one, we can use multiplex:
```python
#shared variables
mutiplex = Semaphore(n)
```
```python
#threads a, b, ..., n
multiplex.wait()
a.run()
multiplex.signal()
```
this way, the first n threads can enter the critical section and the n+1-nth thread will be blocked if none of them left.

### barrier
barrier is a generalization of *rendezvous* for n threads instead of two. the first n-1 threads will prepare and then block until the n-nth thread arrives and unblocks them all.

```python
#shared variables
barrier = Semaphore(0)
count = 0
mutex = Semaphore(1)
```
```python
#threads a, b, ..., n
prepare()

mutex.wait()
count += 1
if count == n:
  barrier.signal()
mutex.signal()

barrier.wait()
barrier.signal()

run()
```

### reusable barrier (turnstile)
consider that the previous code is running on a loop for each thread, and we'd like to guarantee that the barrier is reusable, i.e. it unblocks every time all n threads are done with prepare().
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

## classical synchronization problems

### producer-consumer
```python
#shared variables
buffer = Buffer(size)
mutex = Semaphore(1)
empty = Semaphore(0)
full = semaphore(size)
```

```python
#producer
data = produce()
full.wait() #checking if buffer is not full before adding onto it
mutex.wait() #controls access to buffer
buffer.put(data) #critical section
mutex.signal()
empty.signal() #echoing that buffer is not empty
```

```python
#consumer
empty.wait() #checking if buffer is not empty before retrieving from it
mutex.wait() #controls access to buffer
data = buffer.get() #critical section
mutex.signal()
full.signal() #echoing that buffer is not full
```

### reader-writer (or lightswitch)
```python
#shared variables
inode = Inode()
mutex = Semaphore(1)
readers = 0
roomEmpty = Semaphore(1)
```

```python
#reader
mutex.wait()
readers += 1
if readers == 1:
  roomEmpty.wait() #first in locks the room
mutex.signal()

read(inode) #critical section

mutex.wait()
readers -= 1
if readers == 0:
  roomEmpty.signal() #last out unlocks the room
mutex.signal()
```

```python
#writer
roomEmpty.wait()
inode.write(data) #critical section
roomEmpty.signal()
```

## summary
- signaling: simplest pattern;
- rendezvous: bilateral signaling;
- mutex: to protect critical sections;
- multiplex: generalization of mutex;
- barrier: everyone but the n-nth thread blocks before signaling, the n-nth thread signals, then blocks, then signals again while everyone unblocks each other;
- turnstile: two-phase barrier where the n-nth thread locks the following phase right before unlocking the current phase;
- producer-consumer: producers check if the buffer is full before adding and echo that is not empty after; consumers check if the buffer is empty before getting and echo that is not full after;
- reader-writer: first in locks the room, last out unlocks the room; can use a turnstile to avoid starvation between writers.

i sent the following prompt to gemini 2.5 pro: "i'm studying for a concurrent programming exam. write a python script in which i need to implement the classes Barrier, Turnstile and Lightswitch and everything else is already written so I can test the correctness of my implementation" and got [gemini-template.py](gemini-template.py) as a result. my implementations are [here](my-implementations.py). 