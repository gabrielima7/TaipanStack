window.BENCHMARK_DATA = {
  "lastUpdate": 1772571684012,
  "repoUrl": "https://github.com/gabrielima7/TaipanStack",
  "entries": {
    "TaipanStack Performance": [
      {
        "commit": {
          "author": {
            "email": "gabrielima.alu.lmb@gmail.com",
            "name": "gabriel",
            "username": "gabrielima7"
          },
          "committer": {
            "email": "gabrielima.alu.lmb@gmail.com",
            "name": "gabriel",
            "username": "gabrielima7"
          },
          "distinct": true,
          "id": "b3f210d9cbec43d7e840d57dbc6754895a10a9b2",
          "message": "docs: finalize v0.3.3 release notes, update test counts, add CI fixes section",
          "timestamp": "2026-03-03T18:00:37-03:00",
          "tree_id": "bac18ad039680316f8f0951e2ab2594c44f0d2cb",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/b3f210d9cbec43d7e840d57dbc6754895a10a9b2"
        },
        "date": 1772571683769,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 191019.3894874923,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015268310977251792",
            "extra": "mean: 5.2350706526861694 usec\nrounds: 184"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 153411.0152571547,
            "unit": "iter/sec",
            "range": "stddev: 9.137133845282058e-7",
            "extra": "mean: 6.518436751909589 usec\nrounds: 66587"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52936.217626773294,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026409523741711337",
            "extra": "mean: 18.89065832112332 usec\nrounds: 23885"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 143874.1510485716,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030486462533398265",
            "extra": "mean: 6.950518857709208 usec\nrounds: 8299"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110623.0126146724,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011302561708217476",
            "extra": "mean: 9.039710421585154 usec\nrounds: 38929"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19267.74611536553,
            "unit": "iter/sec",
            "range": "stddev: 0.000008622651924881544",
            "extra": "mean: 51.900206387010975 usec\nrounds: 10490"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34007.72165432187,
            "unit": "iter/sec",
            "range": "stddev: 0.00001604681507346325",
            "extra": "mean: 29.405086590765926 usec\nrounds: 16526"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4382244.9582919385,
            "unit": "iter/sec",
            "range": "stddev: 3.294538807494066e-8",
            "extra": "mean: 228.1935422408882 nsec\nrounds: 150083"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590724.1362105086,
            "unit": "iter/sec",
            "range": "stddev: 2.532063247331537e-7",
            "extra": "mean: 1.6928375508997962 usec\nrounds: 181819"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 769143.548905846,
            "unit": "iter/sec",
            "range": "stddev: 8.147095354368383e-7",
            "extra": "mean: 1.3001474190644406 usec\nrounds: 7265"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 591287.7057663477,
            "unit": "iter/sec",
            "range": "stddev: 4.3129037964755064e-7",
            "extra": "mean: 1.6912240695144072 usec\nrounds: 161499"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2894251.405322218,
            "unit": "iter/sec",
            "range": "stddev: 4.227325118088497e-8",
            "extra": "mean: 345.5124866350961 nsec\nrounds: 108496"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1132793.6509593083,
            "unit": "iter/sec",
            "range": "stddev: 2.8549412342461325e-7",
            "extra": "mean: 882.773309289956 nsec\nrounds: 162049"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29323.84442135205,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022183703343660694",
            "extra": "mean: 34.10194057883671 usec\nrounds: 12403"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2428088.2541508693,
            "unit": "iter/sec",
            "range": "stddev: 4.460355288566528e-8",
            "extra": "mean: 411.84664449098494 nsec\nrounds: 70943"
          }
        ]
      }
    ]
  }
}