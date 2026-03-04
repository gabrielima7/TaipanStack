window.BENCHMARK_DATA = {
  "lastUpdate": 1772637244550,
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
      },
      {
        "commit": {
          "author": {
            "email": "gabrielima.alu.lmb@gmail.com",
            "name": "gabrielima7",
            "username": "gabrielima7"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a6a6ab85b0a41b8a07c55be03dbe10ddad0ea9fb",
          "message": "refactor: optimize string concatenation in `generate_pre_commit_config` (#130)\n\nReplaced sequential `+=` string concatenations in conditional blocks with a list to hold chunks and a final `\"\".join(security_hooks)` implementation. This improves performance and memory usage by reducing the creation of intermediate string objects.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:12:35Z",
          "tree_id": "7a01feb9ca71711dd3e55b901482405d69dc36c6",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/a6a6ab85b0a41b8a07c55be03dbe10ddad0ea9fb"
        },
        "date": 1772637239717,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 203389.1538250578,
            "unit": "iter/sec",
            "range": "stddev: 7.099315154518372e-7",
            "extra": "mean: 4.916683024602853 usec\nrounds: 1997"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 147281.17077098056,
            "unit": "iter/sec",
            "range": "stddev: 9.090281803379891e-7",
            "extra": "mean: 6.789734185064166 usec\nrounds: 51502"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 51957.70806369333,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015501861788393477",
            "extra": "mean: 19.246422470639605 usec\nrounds: 27912"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163664.46906404695,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010064960364155218",
            "extra": "mean: 6.1100616750766426 usec\nrounds: 12047"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110826.26823266079,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011242032098715235",
            "extra": "mean: 9.023131572928822 usec\nrounds: 43360"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19916.93520777764,
            "unit": "iter/sec",
            "range": "stddev: 0.000004119766146714279",
            "extra": "mean: 50.208528047502824 usec\nrounds: 10607"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33764.169396719204,
            "unit": "iter/sec",
            "range": "stddev: 0.000019401376403276057",
            "extra": "mean: 29.61719532473285 usec\nrounds: 8299"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4439612.118791559,
            "unit": "iter/sec",
            "range": "stddev: 3.115013628045534e-8",
            "extra": "mean: 225.24490276232996 nsec\nrounds: 153799"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 589844.9408063609,
            "unit": "iter/sec",
            "range": "stddev: 2.7639647322381086e-7",
            "extra": "mean: 1.6953608157305098 usec\nrounds: 189394"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1063419.3574023724,
            "unit": "iter/sec",
            "range": "stddev: 3.8135331694020463e-7",
            "extra": "mean: 940.362795767337 nsec\nrounds: 10058"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 598055.349887782,
            "unit": "iter/sec",
            "range": "stddev: 5.214733660147071e-7",
            "extra": "mean: 1.6720860371663562 usec\nrounds: 164150"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2864771.749257438,
            "unit": "iter/sec",
            "range": "stddev: 7.467416350695684e-8",
            "extra": "mean: 349.06794939565907 nsec\nrounds: 111533"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1151802.2924873692,
            "unit": "iter/sec",
            "range": "stddev: 3.094755145878856e-7",
            "extra": "mean: 868.20455778088 nsec\nrounds: 178859"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29924.675588751707,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031466407867871325",
            "extra": "mean: 33.41723779207441 usec\nrounds: 12881"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2477062.3189655053,
            "unit": "iter/sec",
            "range": "stddev: 4.5194037453499524e-8",
            "extra": "mean: 403.70401355810395 nsec\nrounds: 93371"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gabrielima.alu.lmb@gmail.com",
            "name": "gabrielima7",
            "username": "gabrielima7"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1c4a9383ad472139cf92a3771a9737fa7b3e2137",
          "message": "🧪 [testing improvement] Add base Exception handling test for safe decorator (#127)\n\n* test: verify safe decorator catches base Exception\n\nAdds a test to `TestSafeDecorator` to verify that the `@safe` decorator correctly catches a basic `Exception` and returns it wrapped in an `Err` result, rather than just subclass exceptions. Asserts the error type exactly matches `Exception` using `type(err) is Exception`.\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n* test: verify safe decorator catches base Exception and fix lint\n\nAdds a test to `TestSafeDecorator` to verify that the `@safe` decorator correctly catches a basic `Exception` and returns it wrapped in an `Err` result, rather than just subclass exceptions. Asserts the error type exactly matches `Exception` using `type(err) is Exception`.\nAlso fixes a ruff TRY002 error by adding a `# noqa: TRY002` comment.\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n---------\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:12:46Z",
          "tree_id": "6b6707594ceeabd2ca3e7c8af24a51d2c4d2d79f",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/1c4a9383ad472139cf92a3771a9737fa7b3e2137"
        },
        "date": 1772637244122,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 220169.6939022437,
            "unit": "iter/sec",
            "range": "stddev: 7.021367014048403e-7",
            "extra": "mean: 4.541951175369323 usec\nrounds: 1659"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 153667.42915648542,
            "unit": "iter/sec",
            "range": "stddev: 8.210616032690117e-7",
            "extra": "mean: 6.507559900554214 usec\nrounds: 62345"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52831.92694433277,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013722337775150922",
            "extra": "mean: 18.92794864464562 usec\nrounds: 31467"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163372.42453431635,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010180222379207114",
            "extra": "mean: 6.120984020714893 usec\nrounds: 11202"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109011.48609118564,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010988238774466202",
            "extra": "mean: 9.173345267153982 usec\nrounds: 44244"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 17068.03715345171,
            "unit": "iter/sec",
            "range": "stddev: 0.000017174718945938185",
            "extra": "mean: 58.58904518483354 usec\nrounds: 10955"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33893.29874663269,
            "unit": "iter/sec",
            "range": "stddev: 0.000019935425699902112",
            "extra": "mean: 29.504357409275496 usec\nrounds: 11796"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4442484.611918447,
            "unit": "iter/sec",
            "range": "stddev: 2.9356425634482617e-8",
            "extra": "mean: 225.0992602917037 nsec\nrounds: 154250"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 586060.9484468389,
            "unit": "iter/sec",
            "range": "stddev: 2.389201890631065e-7",
            "extra": "mean: 1.7063071727439323 usec\nrounds: 188324"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1054993.6930320677,
            "unit": "iter/sec",
            "range": "stddev: 4.2506917925364367e-7",
            "extra": "mean: 947.8729651226492 nsec\nrounds: 10320"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 601498.6537135649,
            "unit": "iter/sec",
            "range": "stddev: 3.592044353638779e-7",
            "extra": "mean: 1.6625141117542759 usec\nrounds: 151930"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2869661.9226932866,
            "unit": "iter/sec",
            "range": "stddev: 3.706088307362814e-8",
            "extra": "mean: 348.47310482538626 nsec\nrounds: 110412"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1130247.4465934888,
            "unit": "iter/sec",
            "range": "stddev: 2.571438250723226e-7",
            "extra": "mean: 884.7620076594303 nsec\nrounds: 159211"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29756.14661541177,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026670174783462655",
            "extra": "mean: 33.606501975026035 usec\nrounds: 15696"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2458846.050160368,
            "unit": "iter/sec",
            "range": "stddev: 5.040513651819341e-8",
            "extra": "mean: 406.69483961151076 nsec\nrounds: 104091"
          }
        ]
      }
    ]
  }
}