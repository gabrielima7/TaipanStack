window.BENCHMARK_DATA = {
  "lastUpdate": 1772485448905,
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
          "id": "b7cda956f9f9ab904c5ae6f01662c703ec21b8ab",
          "message": "chore(release): bump version to v0.3.2 and update docs/changelog",
          "timestamp": "2026-03-02T18:02:38-03:00",
          "tree_id": "cd3de4a067d4a36a8fd5b4fb06b1bfcfbe021879",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/b7cda956f9f9ab904c5ae6f01662c703ec21b8ab"
        },
        "date": 1772485448455,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 191971.26623632948,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015654267302351476",
            "extra": "mean: 5.209112903224449 usec\nrounds: 186"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 153595.3191267318,
            "unit": "iter/sec",
            "range": "stddev: 8.017754683109923e-7",
            "extra": "mean: 6.510615073984761 usec\nrounds: 67852"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53365.703669106195,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013820458534732916",
            "extra": "mean: 18.73862670677961 usec\nrounds: 17284"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163804.0519106707,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010751522266357832",
            "extra": "mean: 6.10485508957582 usec\nrounds: 10993"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109240.20025741716,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012288536701799793",
            "extra": "mean: 9.154139205563222 usec\nrounds: 44560"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19732.03891155835,
            "unit": "iter/sec",
            "range": "stddev: 0.000003893813124804374",
            "extra": "mean: 50.6790000000575 usec\nrounds: 10738"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33894.2227682246,
            "unit": "iter/sec",
            "range": "stddev: 0.00001440974073046492",
            "extra": "mean: 29.50355306384211 usec\nrounds: 17168"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4152499.1359078763,
            "unit": "iter/sec",
            "range": "stddev: 8.127059226082894e-8",
            "extra": "mean: 240.81883397685098 nsec\nrounds: 153093"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 437101.60964729113,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015520632909849178",
            "extra": "mean: 2.2877975690982386 usec\nrounds: 149656"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1086738.3689643547,
            "unit": "iter/sec",
            "range": "stddev: 3.9701399795656026e-7",
            "extra": "mean: 920.1846815742642 nsec\nrounds: 10001"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 618245.3630737768,
            "unit": "iter/sec",
            "range": "stddev: 4.047051624048163e-7",
            "extra": "mean: 1.6174807927846395 usec\nrounds: 159185"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2920860.7085265997,
            "unit": "iter/sec",
            "range": "stddev: 4.3099889022772676e-8",
            "extra": "mean: 342.36483687175445 nsec\nrounds: 107216"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1114156.6210595162,
            "unit": "iter/sec",
            "range": "stddev: 2.8250409703336874e-7",
            "extra": "mean: 897.5398800296515 nsec\nrounds: 171527"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29732.43726699666,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028402006484237127",
            "extra": "mean: 33.633300594230505 usec\nrounds: 20027"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2445608.7717815023,
            "unit": "iter/sec",
            "range": "stddev: 5.999479413683958e-8",
            "extra": "mean: 408.8961454253738 nsec\nrounds: 52068"
          }
        ]
      }
    ]
  }
}