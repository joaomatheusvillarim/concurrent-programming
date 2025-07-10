# primeiro estágio

## sincronização

## semáforos

## sinalização

## mutex

## multiplex

## barrier

## barrier reutilizável (turnstile)

## producer-consumer
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

## reader-writer
