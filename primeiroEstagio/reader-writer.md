# reader-writer
## the little book of semaphores
"The next classical problem, called the Reader-Writer Problem, pertains to any situation where a data structure, database, or file system is read and modified by concurrent threads. While the data structure is being written or modified it is often necessary to bar other threads from reading, in order to prevent a reader from interrupting a modification in progress and reading inconsistent or invalid data.  
As in the producer-consumer problem, the solution is asymmetric. Readers and writers execute different code before entering the critical section. The synchronization constraints are:
1. Any number of readers can be in the critical section simultaneously.
2. Writers must have exclusive access to the critical section.

In other words, a writer cannot enter the critical section while any other thread (reader or writer) is there, and while the writer is there, no other thread may enter. The exclusion pattern here might be called categorical mutual exclusion. A thread in the critical section does not necessarily exclude other threads, but the presence of one category in the critical section excludes other categories.  
Puzzle: Use semaphores to enforce these constraints, while allowing readers and writers to access the data structure, and avoiding the possibility of deadlock."

## my implementation
```python
#shared variables
inode = Inode()
mutex = Semaphore(1)
```

```python
#reader
read(inode) #critical section
```

```python
#writer
mutex.wait()
inode.write(data) #critical section
mutex.signal()
```