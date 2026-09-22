1. **Fuzzing Implementation**
   - Write a property-based test `test_security_fuzzing_guard_file_extension.py` in `tests/` targeting `guard_file_extension` from `taipanstack.security.guards`. The test will fuzz `filename`, `allowed_extensions`, and `denied_extensions` looking for logical edge cases and validation bypasses (e.g. empty strings, null bytes, huge lists).
2. **Verify Test File**
   - Read the newly created test file `tests/test_security_fuzzing_guard_file_extension.py` using `cat` to verify it was written correctly.
3. **Hardening (The Fix)**
   - Modify `src/taipanstack/security/guards.py` to fix the vulnerability by updating `_check_allowed_extension` and `_check_denied_extension`. We need to explicitly check and ensure the input types for `denied_extensions` and `allowed_extensions` are safely evaluated.
   - For `_check_denied_extension`, change the empty string handling and explicitly avoid generating empty `ext` vulnerabilities when the collection evaluates dynamically. We'll adjust the condition to correctly block denied extensions.
   - We will also ensure `guard_file_extension` verifies that `allowed_extensions` and `denied_extensions` are explicitly sequences. We will raise `TypeError` if they are passed as non-sequence objects (e.g., passing a string incorrectly, which the current code doesn't strictly prevent although it iterates over characters, which is dangerous).
4. **Verify Modifications**
   - Read the modifications in `src/taipanstack/security/guards.py` using `cat` to ensure the edits were applied successfully.
5. **Run Tests**
   - Run the complete suite `poetry run pytest` (and `make all` if appropriate) to ensure tests pass and the coverage remains at 100%.
6. **Pre-flight Check**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
7. **Pull Request**
   - Create a PR documenting the fuzzing implementation targeting `guard_file_extension`, the edge cases generated (e.g. "bombarded with empty extension lists and empty filenames"), and the code modifications.
