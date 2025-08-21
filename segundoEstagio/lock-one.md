# *lockone*

## implementação
```java
public class LockOne implements Lock {

  boolean[] flag = new boolean[2];

  public void lock() {
    int i = ThreadID.get();
    int j = 1 - i;
    flag[i] = true;          //writeA(flag[A] = true), writeB(flag[B] = true)
    while (flag[j]) {        //readA(flag[B]), readB(flag[A])
                             //spin-lock
    }
  }

  public void unlock() {
    int i = ThreadID.get();
    flag[i] = false;         //writeA(flag[A] = false), writeB(flag[B] = false)
  }

}
```

## *the art of multiprocessor programming*

### prova por absurdo que *lockone* garante exclusão mútua
sejam A e B threads tal que A!=B. sejam RCA e RCB intervalos em que são executadas
regiões críticas pelas threads A e B, respectivamente. logo,

(eq.1)  writeA(flag[A] = true) -> readA(flag[B] = false) -> RCA  
(eq.2)  writeB(flag[B] = true) -> readB(flag[A] = false) -> RCB

assumir que RCA e RCB se sobrepoem implica que A performou readA(flag[B] = false)
antes que B performasse writeB(flag[B] = true), assim como B performou
readB(flag[A] = false) antes que A performasse writeA(flag[A] = true), assim:

(eq.3)  writeA(flag[A] = true) -> readA(flag[B] = false) -> writeB(flag[B] = true)
-> readB(flag[A] = false) -> writeA(flag[A] = true)

formando um ciclo entre os eventos, o que é um absurdo, pois um evento não pode
preceder a si mesmo.
[#] Q.E.D.

### *deadlock* em *lockone*
caso ocorra writeA[flag[A] = true] -> writeB(flag[B] = true) -> readA(flag[B]) ->
readB(flag[B]),
(leia-se: A levantou sua bandeira -> B levantou sua bandeira -> A viu a bandeira
erguida de B -> B viu a bandeira erguida de A)
ocorrerá um *deadlock*.