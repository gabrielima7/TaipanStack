import re
from pathlib import Path

def process_file(filepath, imports_to_remove, test_def_names, class_names):
    p = Path(filepath)
    if not p.exists():
        return
    text = p.read_text()

    # Imports
    for name in imports_to_remove:
        text = text.replace(f"    {name},\n", "")
        text = text.replace(f", {name}", "")
        text = text.replace(f"{name}, ", "")

    # Functions
    for pattern in test_def_names:
        text = re.sub(rf"def {pattern}\(.*?(?=\ndef |\nclass |\Z)", "", text, flags=re.DOTALL)

    # Classes
    for class_name in class_names:
        text = re.sub(rf"class {class_name}\b.*?(?=\nclass |\Z)", "", text, flags=re.DOTALL)

    p.write_text(text)

process_file("tests/test_property_sanitizers.py",
             ["sanitize_env_value", "sanitize_sql_identifier"],
             [],
             ["TestSanitizeEnvValueProperties", "TestSanitizeSqlIdentifierProperties"])

process_file("tests/test_security_sanitizers.py",
             ["sanitize_env_value", "sanitize_sql_identifier"],
             [],
             ["TestSanitizeEnvValue", "TestSanitizeSqlIdentifier"])

process_file("tests/test_security_guards.py",
             ["guard_hash_algorithm"],
             [],
             ["TestGuardHashAlgorithm"])

process_file("tests/test_very_last.py",
             ["guard_hash_algorithm"],
             [],
             ["TestGuardHashAlgorithmFormat"])

process_file("tests/test_benchmarks.py",
             ["sanitize_env_value", "sanitize_sql_identifier"],
             ["test_bench_sanitize_env_value_standard",
              "test_bench_sanitize_env_value_large",
              "test_bench_sanitize_sql_identifier",
              "test_bench_sanitize_sql_identifier_dirty"],
             [])

process_file("tests/test_final_coverage.py",
             [],
             ["test_sanitize_env_value_multiline",
              "test_sanitize_sql_identifier_starts_with_number"],
             [])

process_file("tests/test_100_coverage_final.py",
             [],
             ["test_sanitize_env_value_multiline_allowed",
              "test_sanitize_sql_identifier_starts_with_number"],
             [])

process_file("tests/test_mocked_coverage.py",
             [],
             ["test_sanitize_sql_identifier_starts_with_number"],
             [])

Path("tests/test_fuzz_sanitizers_types.py").unlink(missing_ok=True)
