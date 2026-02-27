window.BENCHMARK_DATA = {
  "lastUpdate": 1772201089114,
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
          "id": "783fea61cdf6a6f8995d5a7d9c6958d8ff7821c1",
          "message": "fix(ci): rewrite gh-pages bootstrap to check remote branch\n\nRoot cause: The step used 'git rev-parse --verify gh-pages' which only\n\nchecks locally. Since CI runners are clean, it always created a new\n\norphan branch, diverging from the remote gh-pages and causing\n\nnon-fast-forward errors on both fetch and push.\n\nFix: Check remote via 'git ls-remote', fetch if exists, create+push\n\nonly if missing. Also deleted corrupted remote gh-pages branch.",
          "timestamp": "2026-02-27T11:04:08-03:00",
          "tree_id": "cb3f848a176101cd06177e5e5e07b14a57fcf6e3",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/783fea61cdf6a6f8995d5a7d9c6958d8ff7821c1"
        },
        "date": 1772201088479,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 180682.9816741667,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014567711142125365",
            "extra": "mean: 5.534555555449835 usec\nrounds: 216"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154990.83310218857,
            "unit": "iter/sec",
            "range": "stddev: 8.05822369643797e-7",
            "extra": "mean: 6.451994482413549 usec\nrounds: 63252"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53338.599121045205,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017868023029720799",
            "extra": "mean: 18.748148929270275 usec\nrounds: 18727"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163618.4944613498,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012234006001614274",
            "extra": "mean: 6.111778520466839 usec\nrounds: 11220"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109969.40420063313,
            "unit": "iter/sec",
            "range": "stddev: 0.000001143056558071556",
            "extra": "mean: 9.09343837287283 usec\nrounds: 43682"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19590.862973922634,
            "unit": "iter/sec",
            "range": "stddev: 0.000003605923800982295",
            "extra": "mean: 51.04420368470232 usec\nrounds: 10693"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 31667.384860029124,
            "unit": "iter/sec",
            "range": "stddev: 0.000015130030325580984",
            "extra": "mean: 31.578231180756877 usec\nrounds: 15330"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4436056.793970111,
            "unit": "iter/sec",
            "range": "stddev: 3.0454477899763374e-8",
            "extra": "mean: 225.42542768143664 nsec\nrounds: 149410"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 588169.5517134629,
            "unit": "iter/sec",
            "range": "stddev: 2.468692373772807e-7",
            "extra": "mean: 1.7001900167847868 usec\nrounds: 190513"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1069478.3380209822,
            "unit": "iter/sec",
            "range": "stddev: 5.028205248798151e-7",
            "extra": "mean: 935.0353012763695 nsec\nrounds: 9943"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 593256.8754739914,
            "unit": "iter/sec",
            "range": "stddev: 6.236671126647443e-7",
            "extra": "mean: 1.6856104688226918 usec\nrounds: 158203"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2893164.2901466414,
            "unit": "iter/sec",
            "range": "stddev: 4.095844217930181e-8",
            "extra": "mean: 345.6423139900874 nsec\nrounds: 109927"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1137311.801675842,
            "unit": "iter/sec",
            "range": "stddev: 2.57475606398785e-7",
            "extra": "mean: 879.2663529266896 nsec\nrounds: 183790"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30590.65783044196,
            "unit": "iter/sec",
            "range": "stddev: 0.000002716580602302488",
            "extra": "mean: 32.68971872206229 usec\nrounds: 16745"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2634338.1541584437,
            "unit": "iter/sec",
            "range": "stddev: 4.204284466031127e-8",
            "extra": "mean: 379.60198785464047 nsec\nrounds: 98146"
          }
        ]
      }
    ]
  }
}