1. **Optimize `sanitize_path`** in `src/taipanstack/security/sanitizers.py`.
   - Before converting to `pathlib.Path`, replace `\x00` in the string to avoid instantiating multiple `Path` objects. Specifically:
     ```python
     if type(path) is str:
         path = Path(path.replace("\x00", ""))
     else:
         path = Path(str(path).replace("\x00", ""))
     ```
   - This directly follows the memory guideline.

2. **Optimize `collect_results`** in `src/taipanstack/core/result.py`.
   - Apply the fast-path list comprehension check (`if type(results) in (list, tuple):`), which falls back safely to generator iterations if an `AttributeError` occurs on a list.
   - Specifically:
     ```python
     def collect_results(results):
         if type(results) in (list, tuple):
             try:
                 return Ok([r.ok_value for r in results])
             except AttributeError:
                 pass

         values = []
         append = values.append
         for result in results:
             try:
                 append(result.ok_value)
             except AttributeError:
                 return result
         return Ok(values)
     ```
   - *However*, memory states: "When optimizing iterable processing (e.g., `collect_results`), explicitly verify types (`if type(results) in (list, tuple):`) before applying fast-path list comprehensions. Avoid wrapping generic generator iterations in broad `try...except` blocks, as an exception will partially consume the generator and break subsequent safe fallback iterations."
   - Because `[r.ok_value for r in results]` on a list won't consume a generator partially (it's a list), it is safe. We will implement this fast path.

3. **Optimize `guard_ssrf`** in `src/taipanstack/security/guards.py`.
   - The memory states: "For senior-level Python optimizations in TaipanStack, favor exact type checking (`type(val) is type`) over `isinstance()` for speed, apply fast-path string checks (e.g., `.isidentifier()`, `.isascii()`) before falling back to regex..."
   - We will replace `isinstance(..., str)` with `type(...) is str` in all relevant functions in `guards.py` and `sanitizers.py` where it is a simple check.

4. **Verify tests and benchmarks**.
   - Run `poetry run pytest`.
   - Run `poetry run pytest tests/test_benchmarks.py --benchmark-only`.

5. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done**.
   - Call `pre_commit_instructions` and follow steps.

6. **Submit PR**.
   - Description will outline exact functions modified and before/after metrics.
