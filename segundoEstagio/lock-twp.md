# *locktwo*

## implementação

```java

public class LockTwo implements Lock {

  int victim;

  public void lock() {
    int i = ThreadID.get();
    victim = i;              //writeA(victim = A), writeB(victim = B)
    while (victim == i) {    //readA(victim), readB(victim)
                             //spin-lock
    }
  }

  public void unlock() {

  }
}
```

## *the art of multiprocessor programming*

### prova por absurdo que *locktwo* garante exclusão mútua
sejam A e B duas threads tal que A!=B. sejam RCA e RCB intervalos em que são
executadas regiões críticas de A e B, respectivamente. logo:

(eq.1)  writeA(victim = A) -> readA(victim == B) -> RCA  
(eq.2)  writeB(victim = B) -> readB(victim == A) -> RCB

assumir que RCA e RCB se sobrepoem implica que writeB(victim = B) ocorre entre
writeA(victim = A) e readA(victim == B), assim como writeA(victim = A) ocorre
entre writeB(victim = B) e readB(victim == A), o que é um absurdo, pois apenas
uma dessas implicações pode ser verdadeira sem formar um ciclo na ordem dos
eventos.

### *deadlock* em *locktwo*
caso apenas uma thread execute o algoritmo, ocorrerá um *deadlock*, pois não
haverá uma thread que a liberte do spin-lock ao escrever o seu proṕrio ID em
victim.
[#] Q.E.D.