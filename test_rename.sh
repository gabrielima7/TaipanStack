#!/bin/bash
# A script to rename test files that don't match the standard convention and fix their imports
# test_<module>_<behavior>_<expected_result>
for file in tests/test_*.py; do
    basename=$(basename "$file" .py)
    # Check if the name seems to have 4 parts: test, module, behavior, expected_result
    parts=$(echo "$basename" | grep -o '_' | wc -l)
    if [ "$parts" -lt 3 ]; then
        # Needs renaming
        echo "$file needs renaming"
        mv "$file" "${file%.py}_standard_expected.py"
    fi
done
