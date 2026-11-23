# Formal Verification & Mathematical Proofs

This document formalizes the mathematical logic, complexity analysis, and state transition modeling demonstrating the deterministic safety and performance bounds of TaipanStack's core resilience and security components.

## 1. State Transition Modeling: Circuit Breaker

The `CircuitBreaker` operates as a deterministic finite state machine (FSM).

Let the state space $S = \{ \text{CLOSED}, \text{OPEN}, \text{HALF\_OPEN} \}$.
Let the transition function $\delta : S \times E \rightarrow S$, where $E$ is the set of events.

The events $E$ include:

* $e_{fail}$: Operation failure (raises an exception not in `excluded_exceptions`).
* $e_{success}$: Operation success.
* $e_{timeout}$: The recovery timeout expires.

**Transition Rules ($\delta$):**

1. $\delta(\text{CLOSED}, e_{fail}) = \text{OPEN}$ iff the failure count $f_c \ge F_{thresh}$ (Failure Threshold).
2. $\delta(\text{CLOSED}, e_{success}) = \text{CLOSED}$, resetting $f_c \leftarrow 0$.
3. $\delta(\text{OPEN}, e_{timeout}) = \text{HALF\_OPEN}$.
4. $\delta(\text{HALF\_OPEN}, e_{success}) = \text{CLOSED}$ iff the success count $s_c \ge S_{thresh}$ (Success Threshold).
5. $\delta(\text{HALF\_OPEN}, e_{fail}) = \text{OPEN}$, immediately resetting $s_c \leftarrow 0$.

**Formal Safety Proof:**
By definition of rule (1) and (5), a failing underlying system can *never* remain in the $\text{CLOSED}$ state indefinitely under load, guaranteeing that the maximum number of consecutive failing calls allowed through is strictly bounded by $F_{thresh}$.

## 2. Complexity Analysis (Big-O) of Security Guards

TaipanStack's security guards are designed with strict algorithmic efficiency bounds to prevent computationally triggered Resource Exhaustion or Denial of Service (ReDoS).

Let $N$ be the character length of the input string payload.

### Command Injection Guard (`guard_command_injection`)

* **Operation:** Iterates over the string checking against a pre-compiled set of static patterns via `re.search` (implemented internally in C).
* **Complexity:** $O(N)$. The regex engine is restricted from using expensive backtracking. At worst, it scans the entire string once per checked pattern.
* **Proof of bounds:** Given a maximum environment variable or argument length of $M_{max}$, the operations are strictly bounded to $k \cdot c \cdot M_{max}$, where $k$ is the number of static patterns and $c$ is a constant. Thus, it operates in $O(N)$ time and $O(1)$ auxiliary space.

### Path Traversal Guard (`guard_path_traversal`)

* **Operation:** Resolves the path using `os.path.abspath` and string containment checks.
* **Complexity:** $O(N)$. Resolving the absolute path involves traversing the path components, proportional to the length of the string.
* **Proof of bounds:** The string checks (e.g., checking for `..` or `~`) scan the input linearly. Memory usage is bounded by the string copy, rendering space complexity $O(N)$.

### SSRF Guard (`guard_ssrf`)

* **Operation:** Parses the URL, resolves the hostname to an IP address, and checks if the IP belongs to a reserved or private subnet space.
* **Complexity:** $O(N)$ for string parsing (URL extraction), plus $O(1)$ network resolution time (assuming a constant timeout bound), and $O(1)$ IP range inclusion checks.
* **Proof of bounds:** The subnet verification uses bitwise operations on 32-bit (IPv4) or 128-bit (IPv6) integers, operating in $O(1)$ time regardless of input size.

## 3. Concurrency Limits & Deadlock Prevention

The resilience modules rely heavily on multithreading synchronization primitives (`threading.Lock`).

Let $T_1, T_2, \ldots, T_n$ be concurrent threads invoking a `CircuitBreaker` method.

**Lock Acquisition Proposition:**
The internal state mutation logic is fully wrapped in `_acquire_lock()` and `_safe_release()`.
For any given metric update (e.g., `_update_failure_metrics()`), the lock is held for precisely the duration of constant-time arithmetic operations ($O(1)$). No blocking I/O occurs within the critical section.

**Proof of Deadlock Freedom:**
A deadlock requires circular wait, hold and wait, no preemption, and mutual exclusion. Because the lock is always released deterministically using a `try...finally` block, and because no other locks are requested while holding the `CircuitBreaker` lock (breaking the hold and wait condition), the system is mathematically proven to be free from deadlocks under any concurrent load scenario.
