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

data = inode.read() #critical section

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

## implementing lightswitch as a class
```python
#definition
class Lightswitch:
  def __init__(self):
    self.count = 0
    self.mutex = Semaphore(1)

  def lock(self, semaphore):
    self.mutex.wait()
    count += 1
    if count == 1:
      semaphore.wait()
    mutex.signal()

  def unlock(self, semaphore):
    self.mutex.wait()
    count -= 1
    if count == 0:
      semaphore.signal()
    self.mutex.signal()
```

```python
#shared variables
reader_lightswitch = Lightswitch()
roomEmpty = Semaphore(1)
```

```python
#reader
reader_lightswitch.lock(roomEmpty)
data = inode.read()
reader_lightswitch.unlock(roomEmpty)
```

```python
#writer
roomEmpty.wait()
inode.write(data)
roomEmpty.signal()
```

## solving starvation
"If a writer arrives while there are readers in the critical section, it might wait in queue forever while readers come and go. As long as a new reader arrives before the last of the current readers departs, there will always be at least one reader in the room."
```python
#shared variables
reader_lightswitch = Lightswitch()
roomEmpty = Semaphore(1)
turnstile = Semaphore(1)
```
```python
#reader
turnstile.wait()
turnstile.signal()

reader_lightswitch.lock(roomEmpty)
data = inode.read() #critical section
reader_lightswitch.unlock(roomEmpty)
```
```python
#writer
turnstile.wait()
roomEmpty.wait()
inode.write(data) #critical section
turnstile.signal()
roomEmpty.signal()
```