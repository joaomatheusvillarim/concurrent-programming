# producer-writer

## the little book of semaphores
"In multithreaded programs there is often a division of labor between threads. In one common pattern, some threads are producers and some are consumers. Producers create items of some kind and add them to a data structure; consumers remove the items and process them.  
Event-driven programs are a good example. An “event” is something that happens that requires the program to respond: the user presses a key or moves the mouse, a block of data arrives from the disk, a packet arrives from the network, a pending operation completes.  
Whenever an event occurs, a producer thread creates an event object and adds it to the event buffer. Concurrently, consumer threads take events out of the buffer and process them. In this case, the consumers are called “event handlers.”  
There are several synchronization constraints that we need to enforce to make this system work correctly:  
* While an item is being added to or removed from the buffer, the buffer is in an inconsistent state. Therefore, threads must have exclusive access to the buffer.
* If a consumer thread arrives while the buffer is empty, it blocks until a producer adds a new item.

Assume that producers perform the following operations over and over:
```python
data = produce()
buffer.put(data) 
```
Also, assume that consumers perform the following operations:  
```python
data = buffer.get()
process(data)
```
As specified above, access to the buffer has to be exclusive, but
produce() and process() can run concurrently.  
Puzzle: Add synchronization statements to the producer and consumer code to enforce the synchronization constraints."

## classroom extras
The buffer has a limited known size, which means that if a producer thread arrives when the buffer is full, it must block until a consumer removes an item. 

## my implementation

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