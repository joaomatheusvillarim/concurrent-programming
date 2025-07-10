import threading
import time
import unittest
import random

# ============================================================================
# TODO: Implement the synchronization primitives in the classes below.
# The testing code at the end of the file will verify your implementations.
# ============================================================================

class Barrier:
    """
    A Barrier is a synchronization primitive that allows multiple threads to wait
    until all of them have reached a certain point before proceeding.

    Imagine a group of friends agreeing to meet at a location before starting
    an activity together. No one starts until the last person arrives.
    """
    def __init__(self, n):
        """
        Initializes the Barrier.
        :param n: The number of threads that must wait on the barrier.
        """
        self.n = n
        self.count = 0
        self.mutex = threading.Semaphore(1)
        self.turnstile = threading.Semaphore(0) # Locked initially

    def wait(self):
        """
        Causes a thread to wait at the barrier. The thread will be blocked
        until all 'n' threads have called this method.
        """
        # === YOUR IMPLEMENTATION GOES HERE ===
        # Hint: You'll need to manage a counter and use semaphores to block
        # and release threads. The first n-1 threads should block, and the
        # nth thread should release them all.
        self.mutex.acquire()
        self.count += 1
        if self.count == self.n:
            # The last thread has arrived, release all waiting threads.
            # We signal 'n' times to release all threads including itself.
            for _ in range(self.n):
                self.turnstile.release()
        self.mutex.release()

        # All threads will wait here until the turnstile is signaled.
        self.turnstile.acquire()


class Turnstile:
    """
    A Turnstile is a synchronization primitive that allows threads to pass
    through one at a time. It's like a physical turnstile that lets one
    person through per rotation. It can be locked and unlocked.
    """
    def __init__(self):
        """
        Initializes the Turnstile.
        """
        self.mutex = threading.Semaphore(1)
        self.turnstile = threading.Semaphore(0) # Locked initially

    def wait(self):
        """
        A thread calling wait() will pass through the turnstile if it's unlocked.
        This is often used in combination with other logic to control thread flow.
        In this implementation, it's part of a two-phase barrier.
        """
        # === YOUR IMPLEMENTATION GOES HERE ===
        # Hint: A turnstile is simpler than a full barrier. Think about
        # how one thread can signal the next one to proceed.
        # This implementation is often used inside a barrier.
        self.turnstile.acquire()
        self.turnstile.release()

    def lock(self):
        """
        Locks the turnstile, preventing any threads from passing through wait().
        """
        self.turnstile.acquire()

    def unlock(self):
        """
        Unlocks the turnstile, allowing one thread to pass through wait().
        """
        self.turnstile.release()


class Lightswitch:
    """
    A Lightswitch is used to control access to a resource. The first thread
    to arrive "turns on the light" (locks a semaphore), and the last thread
to
    leave "turns off the light" (unlocks the semaphore). All other threads
    pass through without changing the semaphore's state.

    This is useful for protecting a resource that can be used by multiple
    threads concurrently, but access to the "room" itself needs to be
    controlled.
    """
    def __init__(self):
        """
        Initializes the Lightswitch.
        """
        self.counter = 0
        self.mutex = threading.Semaphore(1)

    def lock(self, semaphore):
        """
        A thread calls this method to enter the "room". The first thread in
        will lock the given semaphore.
        :param semaphore: The semaphore to lock if this is the first thread.
        """
        # === YOUR IMPLEMENTATION GOES HERE ===
        # Hint: You need a counter and a mutex to protect the counter.
        # The first thread (when the counter goes from 0 to 1) locks
        # the semaphore.
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            # First thread in, turn on the light (lock the semaphore)
            semaphore.acquire()
        self.mutex.release()

    def unlock(self, semaphore):
        """
        A thread calls this method to leave the "room". The last thread out
        will unlock the given semaphore.
        :param semaphore: The semaphore to unlock if this is the last thread.
        """
        # === YOUR IMPLEMENTATION GOES HERE ===
        # Hint: The last thread (when the counter goes from 1 to 0) unlocks
        # the semaphore.
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            # Last thread out, turn off the light (unlock the semaphore)
            semaphore.release()
        self.mutex.release()


# ============================================================================
# Test Harness - Do not modify the code below this line.
# ============================================================================

class TestConcurrentPrimitives(unittest.TestCase):

    def test_barrier(self):
        """Tests the Barrier implementation."""
        num_threads = 10
        barrier = Barrier(num_threads)
        threads = []
        result_list = []

        def worker():
            time.sleep(random.uniform(0.01, 0.05)) # Simulate work
            result_list.append(time.time())
            barrier.wait()
            result_list.append(time.time())

        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(len(result_list), num_threads * 2)
        arrival_times = sorted(result_list[:num_threads])
        departure_times = sorted(result_list[num_threads:])

        # Check that the last arrival is before the first departure.
        self.assertLessEqual(arrival_times[-1], departure_times[0])
        print(f"\nBarrier Test Passed: All {num_threads} threads waited correctly.")

    def test_lightswitch_for_readers_writers(self):
        """
        Tests the Lightswitch in a classic readers-writers scenario.
        Multiple readers can access a resource simultaneously, but writers
        must have exclusive access.
        """
        room_empty = threading.Semaphore(1) # Controls access to the room
        lightswitch = Lightswitch()
        log = []
        num_readers = 5
        num_writers = 2

        # --- Shared State ---
        shared_data = {"value": 0, "readers_in_room": 0}
        data_lock = threading.Lock() # To safely modify shared_data

        def reader(reader_id):
            time.sleep(random.uniform(0.01, 0.03))
            log.append(f"Reader {reader_id} trying to enter.")

            lightswitch.lock(room_empty) # First reader locks the room for writers
            log.append(f"Reader {reader_id} entered.")

            with data_lock:
                shared_data["readers_in_room"] += 1
            # Simulate reading
            time.sleep(random.uniform(0.02, 0.04))
            with data_lock:
                current_value = shared_data["value"]
                readers_count = shared_data["readers_in_room"]
            log.append(f"Reader {reader_id} read value {current_value} with {readers_count-1} other readers.")
            self.assertGreater(readers_count, 0) # There should be at least one reader

            with data_lock:
                shared_data["readers_in_room"] -= 1

            lightswitch.unlock(room_empty) # Last reader unlocks the room
            log.append(f"Reader {reader_id} left.")

        def writer(writer_id):
            time.sleep(random.uniform(0.01, 0.05))
            log.append(f"Writer {writer_id} trying to enter.")
            room_empty.acquire() # Writer waits for the room to be empty
            log.append(f"Writer {writer_id} entered.")

            with data_lock:
                # While a writer is in, no readers should be present.
                self.assertEqual(shared_data["readers_in_room"], 0)
                shared_data["value"] += 1
                new_value = shared_data["value"]
            log.append(f"Writer {writer_id} wrote value {new_value}.")
            time.sleep(0.05) # Simulate writing

            room_empty.release()
            log.append(f"Writer {writer_id} left.")

        threads = []
        for i in range(num_readers):
            threads.append(threading.Thread(target=reader, args=(i,)))
        for i in range(num_writers):
            threads.append(threading.Thread(target=writer, args=(i,)))

        random.shuffle(threads)
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # Final check
        self.assertEqual(shared_data["value"], num_writers)
        self.assertEqual(shared_data["readers_in_room"], 0)
        print("Lightswitch Test Passed: Readers and Writers scenario completed successfully.")
        # Uncomment the line below to see the detailed execution log
        # print("\n--- Lightswitch Log ---\n" + "\n".join(log))


if __name__ == "__main__":
    print("Starting Concurrent Programming Primitives Test Suite...")
    print("Your task is to implement the `wait`, `lock`, and `unlock` methods.")
    print("If your implementations are correct, the tests will pass.")
    print("-" * 70)
    # Note: I've provided a sample implementation.
    # You should delete it and write your own to learn.
    # If you run the script as is, the tests should pass.
    unittest.main()
