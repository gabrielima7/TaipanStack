1. **Optimize `sanitize_path`** in `src/taipanstack/security/sanitizers.py`.
   - The primary bottleneck is repeatedly calling `Path(str(path).replace("\x00", ""))` and other `pathlib.Path` instantiations for strings when they can be done as pure string manipulations or more directly.
   - Refactor `sanitize_path` to handle `str` directly to clean null bytes before converting to `Path`.
   - Update `_clean_path_parts` to avoid intermediate list appending where unnecessary, although caching `path.parts` instead of looping is probably enough.
   - *However*, memory tells me: "For senior-level Python optimizations in TaipanStack... sanitize strings (e.g., `replace('\x00', '')`) before casting to `pathlib.Path` objects to avoid intermediate allocation overhead."
   - Apply this memory tip.

2. **Optimize `sanitize_filename`** in `src/taipanstack/security/sanitizers.py`.
   - The current code has loops and Regex replacements.
   - Use `replace("/", replacement).replace("\\", replacement)` earlier or more effectively.

3. **Optimize `_check_ip_safety`** in `src/taipanstack/security/guards.py`.
   - In `_check_ip_safety(hostname)`, `ipaddress.ip_address` is instantiated repeatedly in a loop.
   - We can cache the check or just ensure it is called correctly.

Let me refine the plan based on benchmarking. I will request review.
