# peterson lock

## implementação

```java

public class PetersonLock implements Lock {

  boolean[] flag = new boolean[2];
  int victim;

  public void lock() {
    int i = ThreadID.get();
    int j = 1 - i;

    flag[i] = true; //writeA(flag[A] = true), writeB(flag[B] = true)
    victim = i;     //writeA(victim = A), writeB(victim = B)

    //readA(flag[B]) && readA(victim), readB(flag[A]) && readB(victim)
    while (flag[j] = true && victim == i) {
      //spin-lock
    }
  }

  public void unlock() {
    int i = ThreadID.get();
    flag[i] = false;  //writeA(flag[A] = false), writeB(flag[B] = false)
  }

}

```

## *the art of multiprocessor programming*

### prova por absurdo que *peterson lock* garante exclusão mútua
sejam A e B duas threads tal que A!=B. sejam RCA e RCB dois intervalos em que são
executadas regiões críticas por A e B, respectivamente. logo:

(eq.1)  writeA(flag[A] = true) -> writeA(victim = A) -> readA(flag[B]) -> readA(victim) -> RCA  
(eq.2)  writeB(flag[B] = true) -> writeB(victim = B) -> readB(flag[A]) -> readB(victim) -> RCB

assumir que RCA e RCB se sobrepoem implica que uma das threads, digamos A, foi a
última a escrever em victim:

(eq.3)  writeB(victim = B) -> writeA(victim = A)

dado que A executou RCA após a escrita em victim, deduz-se que A leu flag[B]==false,
portanto:

(eq.4)  writeA(victim = A) -> readA(flag[B] == false)

juntando as equações 2, 3, e 4, temos:

(eq.5)  writeB(flag[B] = true) -> writeB(victim = B) -> writeA(victim = A) -> read(flag[B] == false)

o que é um absurdo, pois não é possível que o valor de flag[B] tenha sido escrito por B
como true e lido por A como false nesta ordem de execução.
[#] Q.E.D.

### prova por contradição que peterson lock é livre de starvation
suponha que uma das threads, digamos A, executa infinitamente o spin-lock. isso
implica que outra thread B está repetidamente entrando e saindo da região crítica,
impedindo A de entrar.

no entanto, quando B entra na região crítica, este escreve seu ID em victim,
fazendo com que A liberte-se do spin-lock, o que nos leva a uma contradição.
[#] Q.E.D.

### prova que peterson lock é livre de deadlock
dado que peterson lock é livre de starvation, este algoritmo é também livre de deadlock.