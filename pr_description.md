**Daily Micro-Chaos Experiment: Resilience Retrier Type Mutation Resilience**

### Target
`src/taipanstack/resilience/retry.py` (`Retrier` context manager)

### Chaos Experiment (Simulated Failure)
This experiment simulates a rare production failure where the underlying state tracking mechanism (`retrier.attempt`) is unexpectedly corrupted to a non-numeric type, such as a string (`"corrupted"`) or `math.nan`. Before this fix, this mutation would cause a catastrophic `TypeError` when evaluating the attempt conditions and logging limits, leading to an application crash.

### Hardening Adjustments
The resilience module was modified to detect and safely degrade upon type mutation or structural degradation:
- Wrapped the evaluation in a `try/except TypeError` guard block.
- Implemented `math.isfinite(self.attempt)` evaluation.
- When corruption is detected, the process correctly aborts the retries, allowing the core exception to gracefully propagate downstream instead of raising a raw `TypeError` inside the resilience flow.

The implementation strictly follows TaipanStack's Look-Before-You-Leap guidelines and has been validated against a custom Micro-Chaos test suite ensuring stable degradation. All system tests, MyPy static types, and `make all` workflows are completely green.
