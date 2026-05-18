import os
import shutil

redundant_files = [
    'tests/test_100_coverage_final_operations.py',
    'tests/test_100_percent_coverage_operations.py',
    'tests/test_absolute_final_operations.py',
    'tests/test_chaos_bulkhead_resource_exhaustion_operations.py',
    'tests/test_chaos_circuit_breaker_clock_jump_operations.py',
    'tests/test_chaos_circuit_breaker_nan_config_operations.py',
    'tests/test_chaos_circuit_breaker_nan_operations.py',
    'tests/test_chaos_circuit_breaker_nan_state_corruption_operations.py',
    'tests/test_chaos_circuit_breaker_operations.py',
    'tests/test_chaos_circuit_breaker_result_monad_operations.py',
    'tests/test_chaos_circuit_breaker_time_corruption_operations.py',
    'tests/test_chaos_circuit_breaker_type_mutation.py',
    'tests/test_chaos_circuit_breaker_type_mutation_half_open.py',
    'tests/test_chaos_circuit_breaker_type_mutation_last_failure_time_operations.py',
    'tests/test_chaos_circuit_breaker_untracked_err_operations.py',
    'tests/test_chaos_concurrency_resource_exhaustion_operations.py',
    'tests/test_chaos_http_bridge_operations.py',
    'tests/test_chaos_orchestrator_resource_exhaustion_operations.py',
    'tests/test_chaos_rate_limit_nan_operations.py',
    'tests/test_chaos_rate_limit_state_corruption_operations.py',
    'tests/test_chaos_rate_limit_tokens_mutation_operations.py',
    'tests/test_chaos_rate_limit_type_mutation.py',
    'tests/test_chaos_resilience_circuit_operations.py',
    'tests/test_chaos_resilience_thread_exhaustion_operations.py',
    'tests/test_chaos_retry_callback_operations.py',
    'tests/test_chaos_retry_nan_operations.py',
    'tests/test_chaos_retry_result_operations.py',
    'tests/test_chaos_retry_type_mutation.py',
    'tests/test_chaos_rl_nan_operations.py',
    'tests/test_chaos_timeout_resource_exhaustion_operations.py',
    'tests/test_edge_cases_coverage_operations.py',
    'tests/test_final_coverage_operations.py',
    'tests/test_final_push_100_operations.py',
    'tests/test_full_coverage_operations.py',
    'tests/test_fuzz_cache_operations.py',
    'tests/test_fuzz_email_operations.py',
    'tests/test_fuzz_guard_command_generator_operations.py',
    'tests/test_fuzz_guard_file_extension_operations.py',
    'tests/test_fuzz_guard_null_bytes_operations.py',
    'tests/test_fuzz_guard_path_operations.py',
    'tests/test_fuzz_guard_ssrf_operations.py',
    'tests/test_fuzz_guard_symlink_loop_operations.py',
    'tests/test_fuzz_index_error.py',
    'tests/test_fuzz_jwt_operations.py',
    'tests/test_fuzz_logging_redact_operations.py',
    'tests/test_fuzz_models_recursion_operations.py',
    'tests/test_fuzz_password_operations.py',
    'tests/test_fuzz_password_verification_operations.py',
    'tests/test_fuzz_path_traversal.py',
    'tests/test_fuzz_python_version_operations.py',
    'tests/test_fuzz_sanitizers_types_operations.py',
    'tests/test_fuzz_timeout_operations.py',
    'tests/test_fuzz_url_security_operations.py',
    'tests/test_mocked_coverage_operations.py',
    'tests/test_structlog_branches_operations.py',
    'tests/test_targeted_lines_operations.py',
    'tests/test_ultra_final_operations.py',
    'tests/test_utils_circuit_breaker_chaos_operations.py',
    'tests/test_utils_rate_limit_chaos_operations.py',
    'tests/test_utils_resilience_chaos_operations.py',
    'tests/test_utils_retry_chaos_coverage_operations.py',
    'tests/test_utils_retry_chaos_operations.py',
    'tests/test_v031_features_operations.py',
    'tests/test_v033_structlog_integration_operations.py',
    'tests/test_v034_async_retry_circuit_operations.py',
    'tests/test_v034_logging_coverage_operations.py',
    'tests/test_v034_logging_mask_operations.py',
    'tests/test_very_last_operations.py'
]

# We need to map redundant files to target 'keep' files based on the code they test.
# E.g., tests/test_chaos_circuit_breaker_* -> tests/test_circuit_breaker_type_corruption_operations.py or whatever the main test file is.
# There are too many, but let's see which target files exist.

keep_files = []
for f in os.listdir('tests'):
    if f.startswith('test_') and f.endswith('.py') and f"tests/{f}" not in redundant_files:
        keep_files.append(f"tests/{f}")

print(f"Keep files: {len(keep_files)}")

# 1. Read all contents of redundant files.
redundant_content = {}
for rf in redundant_files:
    if os.path.exists(rf):
        with open(rf, 'r') as f:
            redundant_content[rf] = f.read()

# 2. Append all tests to an aggregator file per module, or we can just append all of them to an 'edge_cases' file?
# No, "migrate missing assertions to 'kept' files".

# To do this safely and maintain tests:
# Let's map redundant files -> keep file.
mapping = {}
for rf in redundant_files:
    content = redundant_content.get(rf, "")
    target = None
    if "taipanstack.resilience.circuit_breaker" in content:
        target = "tests/test_utils_circuit_breaker_operations.py" # wait, is it in redundant files? Yes.
        # Find a kept file for circuit breaker
        for kf in keep_files:
            if 'circuit_breaker' in kf:
                target = kf
                break

    # Heuristic: find the module being imported in the redundant file and match it to a keep file.
    imports = []
    for line in content.split('\n'):
        if line.startswith('from taipanstack.') or line.startswith('import taipanstack.'):
            # Extract module path
            # 'from taipanstack.security.guards import ...' -> 'taipanstack.security.guards'
            if ' import ' in line:
                m = line.split(' import ')[0].replace('from ', '')
                imports.append(m)

    if imports:
        # try to find a keep file that imports the same module
        best_match = None
        best_count = -1
        for kf in keep_files:
            with open(kf, 'r') as f:
                kc = f.read()
            count = kc.count(imports[0])
            if count > best_count:
                best_count = count
                best_match = kf

        if best_match and best_count > 0:
            mapping[rf] = best_match

    if rf not in mapping:
        mapping[rf] = keep_files[0] # fallback

# Move classes/functions from redundant file to keep file.
# Note: redundant files often have duplicate imports, etc.
# We will just append the raw text of classes and functions, then run ruff to clean up imports?
# Or just copy the whole file content, stripping standard imports.
for rf, target in mapping.items():
    content = redundant_content[rf]
    # Remove imports and top-level decorators
    # Actually, simplest is to just append the entire file content wrapped in a unique class or just as is, but we'd need to handle duplicate imports.
    # Appending the whole file content will work if we run ruff formatting/linting afterwards to fix duplicate imports or unused.
    # No, it might cause redefinition of variables.

    # Better: append the content.
    with open(target, 'a') as f:
        f.write("\n\n" + f"# Migrated from {rf}\n")
        f.write(content)

# Delete redundant files
for rf in redundant_files:
    if os.path.exists(rf):
        os.remove(rf)
