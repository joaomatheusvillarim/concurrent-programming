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
A semaphore is like an integer, with three differences:
1. When you create the semaphore, you can initialize its value to any non-negative integer, but after that the only operations you are allowed to perform are **increment** and **decrement**. You cannot read the current value of the semaphore.
2. When a thread decrements the semaphore, **if the result is negative, the thread blocks itself and cannot continue until another thread increments** the semaphore.
3. When a thread increments the semaphore, **if there are other threads waiting, one of the waiting threads gets unblocked.** 

## basic synchronization patterns

### signaling

### mutex

### multiplex

### barrier

### barrier reutilizável (turnstile)

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
buffer.put(data) #critical region
mutex.signal()
empty.signal() #echoing that buffer is not empty
```

```python
#consumer
empty.wait() #checking if buffer is not empty before retrieving from it
mutex.wait() #controls access to buffer
data = buffer.get() #critical region
mutex.signal()
full.signal() #echoing that buffer is not full
```

### reader-writer
