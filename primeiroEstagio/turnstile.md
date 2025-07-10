# turnstile (reusable barrier)

## the little book of semaphores
Often a set of cooperating threads will perform a series of steps in a loop and synchronize at a barrier after each step. For this application we need a reusable barrier that locks itself after all the threads have passed through.  
Puzzle: Rewrite the barrier solution so that after all the threads have passed through, the turnstile is locked again.

## my implementation