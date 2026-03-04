window.BENCHMARK_DATA = {
  "lastUpdate": 1772637583532,
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
          "id": "2277ebf3a66228473b8588356a153fdc394bb3f8",
          "message": "🧪 test ValueError in validate_ip_address (#128)\n\n* test: add assertions to test ValueError chaining in validate_ip_address\n\nAdded assertions to explicitly test that `ValueError` is correctly raised and chained when an invalid IP address is passed to `validate_ip_address` in both `test_security_validators.py` and `test_security_validators_extended.py`. This ensures full test coverage for the error handling logic handling `ValueError` from the `ipaddress` module.\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n* style: fix formatting in tests/test_security_validators.py and tests/test_security_validators_extended.py\n\nRan `ruff format` to fix formatting issues in the modified test files that caused the `ruff format --check` CI job to fail.\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n---------\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:12:42Z",
          "tree_id": "5cb2dbcab5a4a93829ce612dccf0823e4f1efe2e",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/2277ebf3a66228473b8588356a153fdc394bb3f8"
        },
        "date": 1772637245439,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 206630.9758781794,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012165358985415314",
            "extra": "mean: 4.839545454160543 usec\nrounds: 242"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155190.78016390995,
            "unit": "iter/sec",
            "range": "stddev: 9.028149575976198e-7",
            "extra": "mean: 6.443681763464404 usec\nrounds: 61426"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53569.33070548113,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016295564496954392",
            "extra": "mean: 18.667397685028043 usec\nrounds: 26350"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 165483.93388298957,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011484293840888431",
            "extra": "mean: 6.042882692812224 usec\nrounds: 11423"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109091.40867816251,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012067490447258992",
            "extra": "mean: 9.1666246876522 usec\nrounds: 41624"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19744.325632770353,
            "unit": "iter/sec",
            "range": "stddev: 0.000004082048617894377",
            "extra": "mean: 50.64746290145584 usec\nrounds: 9933"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34306.214913215685,
            "unit": "iter/sec",
            "range": "stddev: 0.000017413065904149008",
            "extra": "mean: 29.149237318360438 usec\nrounds: 15692"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4512401.688023685,
            "unit": "iter/sec",
            "range": "stddev: 3.185967532427521e-8",
            "extra": "mean: 221.6114763572711 nsec\nrounds: 153093"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 588694.8807234026,
            "unit": "iter/sec",
            "range": "stddev: 2.9969056601792866e-7",
            "extra": "mean: 1.6986728316222852 usec\nrounds: 185186"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1071695.0775619145,
            "unit": "iter/sec",
            "range": "stddev: 5.028925596095288e-7",
            "extra": "mean: 933.1012346114164 nsec\nrounds: 10935"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 626835.6433307033,
            "unit": "iter/sec",
            "range": "stddev: 4.294321628932941e-7",
            "extra": "mean: 1.5953145144817877 usec\nrounds: 147211"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2871201.657471541,
            "unit": "iter/sec",
            "range": "stddev: 4.059763131861459e-8",
            "extra": "mean: 348.286229703786 nsec\nrounds: 111657"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1104419.6832240517,
            "unit": "iter/sec",
            "range": "stddev: 2.9791816806382556e-7",
            "extra": "mean: 905.4528954797084 nsec\nrounds: 154274"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30818.407240520264,
            "unit": "iter/sec",
            "range": "stddev: 0.000002289335859717228",
            "extra": "mean: 32.44814023630634 usec\nrounds: 12700"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2480997.411711163,
            "unit": "iter/sec",
            "range": "stddev: 4.691154899319429e-8",
            "extra": "mean: 403.06370142896435 nsec\nrounds: 76430"
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
          "id": "7a1d97aede2deb6f2e0d8326fc169f20731f6db6",
          "message": "test: add coverage for validate_url out of range port ValueError (#126)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:12:50Z",
          "tree_id": "acb9d9e5bbee49dcdf955dad94b3bd04976c9eac",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/7a1d97aede2deb6f2e0d8326fc169f20731f6db6"
        },
        "date": 1772637288782,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 195733.57809142832,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021349125914009915",
            "extra": "mean: 5.108985436994843 usec\nrounds: 206"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 144106.27705642692,
            "unit": "iter/sec",
            "range": "stddev: 0.00000181779666661405",
            "extra": "mean: 6.939322980416984 usec\nrounds: 73828"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 51532.20164392979,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025902950510339897",
            "extra": "mean: 19.405342059896146 usec\nrounds: 27235"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 162135.22110468024,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010112844623041347",
            "extra": "mean: 6.1676913454502555 usec\nrounds: 10792"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108472.98327426615,
            "unit": "iter/sec",
            "range": "stddev: 0.000001164776001978132",
            "extra": "mean: 9.218885383391472 usec\nrounds: 44819"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19275.058509417213,
            "unit": "iter/sec",
            "range": "stddev: 0.000003838081580552843",
            "extra": "mean: 51.88051696504216 usec\nrounds: 10728"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 32016.624705484333,
            "unit": "iter/sec",
            "range": "stddev: 0.000016456043276822734",
            "extra": "mean: 31.233773366144483 usec\nrounds: 15439"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4448507.312429099,
            "unit": "iter/sec",
            "range": "stddev: 3.043491068424626e-8",
            "extra": "mean: 224.79450516038304 nsec\nrounds: 152161"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 585067.2935081858,
            "unit": "iter/sec",
            "range": "stddev: 2.4591330556382445e-7",
            "extra": "mean: 1.7092050967398293 usec\nrounds: 189036"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1071756.1087268535,
            "unit": "iter/sec",
            "range": "stddev: 4.4689582594055646e-7",
            "extra": "mean: 933.0480991500082 nsec\nrounds: 10811"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 613423.5843473851,
            "unit": "iter/sec",
            "range": "stddev: 4.160281345021258e-7",
            "extra": "mean: 1.6301949020494368 usec\nrounds: 155473"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2965120.856590783,
            "unit": "iter/sec",
            "range": "stddev: 4.172906042342927e-8",
            "extra": "mean: 337.2543813102467 nsec\nrounds: 114338"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1144524.4381194739,
            "unit": "iter/sec",
            "range": "stddev: 2.818163717340345e-7",
            "extra": "mean: 873.7253366499219 nsec\nrounds: 171763"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 28586.339027209808,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023047808933569867",
            "extra": "mean: 34.98174421873866 usec\nrounds: 14227"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2332100.1831746204,
            "unit": "iter/sec",
            "range": "stddev: 8.58544639656156e-8",
            "extra": "mean: 428.79804530463804 nsec\nrounds: 172712"
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
          "id": "359857ad515178f87deb8721fa829f6aa20df20f",
          "message": "test: improve DNS resolution error testing for guard_ssrf (#122)\n\nUpdated the `test_unresolvable_hostname_returns_err` test in `tests/test_security_ssrf.py` to:\n1. Remove assertions on platform-specific string messages (like \"Name or service not known\").\n2. Validate that long hostnames correctly truncate to 80 characters in the `SecurityError.value` attribute as designed.\n3. Validate that the error prefix is correctly formatted.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:14:05Z",
          "tree_id": "005eee69290fae954c14318ba4159fce2ffb6947",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/359857ad515178f87deb8721fa829f6aa20df20f"
        },
        "date": 1772637296292,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 186492.27696503015,
            "unit": "iter/sec",
            "range": "stddev: 0.000002016593927920574",
            "extra": "mean: 5.3621523436464535 usec\nrounds: 256"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 153757.75275992288,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010933069868892945",
            "extra": "mean: 6.503737093253427 usec\nrounds: 68743"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53361.8077362617,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014797548093749814",
            "extra": "mean: 18.73999480944226 usec\nrounds: 31981"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164393.31538196836,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010131191764573974",
            "extra": "mean: 6.082972398704272 usec\nrounds: 9601"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108919.71721054763,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010771872359235029",
            "extra": "mean: 9.181074149016991 usec\nrounds: 42010"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19816.419334447284,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035239131135241023",
            "extra": "mean: 50.463203423520596 usec\nrounds: 10574"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33909.45900100178,
            "unit": "iter/sec",
            "range": "stddev: 0.000014798863716893679",
            "extra": "mean: 29.4902964972239 usec\nrounds: 17329"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4393235.567471181,
            "unit": "iter/sec",
            "range": "stddev: 5.132129726625216e-8",
            "extra": "mean: 227.62266776764915 nsec\nrounds: 152161"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 591820.4066185307,
            "unit": "iter/sec",
            "range": "stddev: 2.442064721451081e-7",
            "extra": "mean: 1.6897017892871011 usec\nrounds: 187970"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1039987.3887183409,
            "unit": "iter/sec",
            "range": "stddev: 3.311499652575476e-7",
            "extra": "mean: 961.5501215186653 nsec\nrounds: 10694"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 615933.8197417782,
            "unit": "iter/sec",
            "range": "stddev: 3.68453046628288e-7",
            "extra": "mean: 1.6235510503697235 usec\nrounds: 153799"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2942020.569250575,
            "unit": "iter/sec",
            "range": "stddev: 3.7751590400485536e-8",
            "extra": "mean: 339.90245019074024 nsec\nrounds: 107910"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1127738.4512372622,
            "unit": "iter/sec",
            "range": "stddev: 2.410572254108704e-7",
            "extra": "mean: 886.730428409958 nsec\nrounds: 182816"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30247.063487456562,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020128082252849424",
            "extra": "mean: 33.061060635347275 usec\nrounds: 13474"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2484154.496042571,
            "unit": "iter/sec",
            "range": "stddev: 5.706252302454839e-8",
            "extra": "mean: 402.5514522519992 nsec\nrounds: 106180"
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
          "id": "06ef920855b4c9084f410bd3007d5922a70a02b0",
          "message": "test: add test for CVE-2020-10735 limit in get_optimization_level (#129)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:12:38Z",
          "tree_id": "b203f78d4c2656c292b4fabb0d290e9865a1d5ae",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/06ef920855b4c9084f410bd3007d5922a70a02b0"
        },
        "date": 1772637299579,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 171696.26930110517,
            "unit": "iter/sec",
            "range": "stddev: 0.000002380422554499045",
            "extra": "mean: 5.82423837204227 usec\nrounds: 172"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154148.54501323416,
            "unit": "iter/sec",
            "range": "stddev: 8.361245316101953e-7",
            "extra": "mean: 6.487249035754095 usec\nrounds: 67669"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 45048.75792319065,
            "unit": "iter/sec",
            "range": "stddev: 0.00000725544190609513",
            "extra": "mean: 22.198170295949716 usec\nrounds: 31457"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 161863.96256489077,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010275545920992358",
            "extra": "mean: 6.178027425957172 usec\nrounds: 10975"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109246.58070290893,
            "unit": "iter/sec",
            "range": "stddev: 0.000001183638252344728",
            "extra": "mean: 9.153604566530591 usec\nrounds: 43972"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19568.665258534536,
            "unit": "iter/sec",
            "range": "stddev: 0.000004103300048028863",
            "extra": "mean: 51.10210567702706 usec\nrounds: 10428"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33495.51180993547,
            "unit": "iter/sec",
            "range": "stddev: 0.000019651408072305966",
            "extra": "mean: 29.8547460828283 usec\nrounds: 11488"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4386904.297650141,
            "unit": "iter/sec",
            "range": "stddev: 3.238829269559966e-8",
            "extra": "mean: 227.95117744777792 nsec\nrounds: 149858"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590135.4308286213,
            "unit": "iter/sec",
            "range": "stddev: 2.783655259035043e-7",
            "extra": "mean: 1.6945262862727235 usec\nrounds: 184843"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1069411.195544856,
            "unit": "iter/sec",
            "range": "stddev: 3.774088517600678e-7",
            "extra": "mean: 935.0940070255282 nsec\nrounds: 10212"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 603321.3806128447,
            "unit": "iter/sec",
            "range": "stddev: 3.8552395774278535e-7",
            "extra": "mean: 1.6574914003283212 usec\nrounds: 142796"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2920579.452653,
            "unit": "iter/sec",
            "range": "stddev: 4.0978052407951735e-8",
            "extra": "mean: 342.39780708285 nsec\nrounds: 113935"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1139144.945327846,
            "unit": "iter/sec",
            "range": "stddev: 2.993857362648986e-7",
            "extra": "mean: 877.8514131160016 nsec\nrounds: 161239"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30071.96899740398,
            "unit": "iter/sec",
            "range": "stddev: 0.000002243272961824942",
            "extra": "mean: 33.25355915624703 usec\nrounds: 13084"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2519653.4414321636,
            "unit": "iter/sec",
            "range": "stddev: 4.211228657054941e-8",
            "extra": "mean: 396.87997704625445 nsec\nrounds: 55329"
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
          "id": "e54c8c6522e84c27a988549e470ba38ff447dba9",
          "message": "🧪 Added missing SecurityError tests for path traversal when `base_dir` is not provided (#120)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:14:10Z",
          "tree_id": "e9cc1003809c4f1087a287d9df7d2603907e4448",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/e54c8c6522e84c27a988549e470ba38ff447dba9"
        },
        "date": 1772637363175,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 193568.90361571367,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016542873919978417",
            "extra": "mean: 5.166119047640364 usec\nrounds: 168"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 151514.85738554416,
            "unit": "iter/sec",
            "range": "stddev: 8.118535590264773e-7",
            "extra": "mean: 6.600012812310569 usec\nrounds: 70245"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53129.90463372889,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018854596010133633",
            "extra": "mean: 18.821791736572436 usec\nrounds: 27422"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164331.7072092326,
            "unit": "iter/sec",
            "range": "stddev: 0.000001038046596532679",
            "extra": "mean: 6.085252913041101 usec\nrounds: 11929"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109699.05958389974,
            "unit": "iter/sec",
            "range": "stddev: 0.00000113559774264229",
            "extra": "mean: 9.11584842926737 usec\nrounds: 42528"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 20029.852567084054,
            "unit": "iter/sec",
            "range": "stddev: 0.000003250518614785443",
            "extra": "mean: 49.92547981323359 usec\nrounds: 10923"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34307.62405241996,
            "unit": "iter/sec",
            "range": "stddev: 0.0000142310492539957",
            "extra": "mean: 29.148040052906637 usec\nrounds: 16628"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4390284.527238022,
            "unit": "iter/sec",
            "range": "stddev: 4.302690014585837e-8",
            "extra": "mean: 227.77567007228924 nsec\nrounds: 151700"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 561138.3704816814,
            "unit": "iter/sec",
            "range": "stddev: 5.472705662819558e-7",
            "extra": "mean: 1.7820916419269612 usec\nrounds: 188680"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1055978.2035605446,
            "unit": "iter/sec",
            "range": "stddev: 3.9536387661127365e-7",
            "extra": "mean: 946.9892433652535 nsec\nrounds: 10877"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 615886.1805649964,
            "unit": "iter/sec",
            "range": "stddev: 3.9214855248826035e-7",
            "extra": "mean: 1.623676633047081 usec\nrounds: 146994"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2876507.0010119667,
            "unit": "iter/sec",
            "range": "stddev: 3.8660360162972884e-8",
            "extra": "mean: 347.6438609913263 nsec\nrounds: 109806"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1127107.8275735402,
            "unit": "iter/sec",
            "range": "stddev: 2.62779345559117e-7",
            "extra": "mean: 887.2265594613245 nsec\nrounds: 189394"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30316.367840280265,
            "unit": "iter/sec",
            "range": "stddev: 0.000002398504433483271",
            "extra": "mean: 32.98548181195163 usec\nrounds: 14460"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2519465.4844921147,
            "unit": "iter/sec",
            "range": "stddev: 4.819411102334871e-8",
            "extra": "mean: 396.9095850509827 nsec\nrounds: 81215"
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
          "id": "422a8e4ab0b100e9004fca52f7ece2829469ef9b",
          "message": "Remove unused __future__ import annotations (#112)\n\nRemoves redundant `from __future__ import annotations` across the codebase since Python 3.11+ makes it unnecessary unless supporting older versions, which we do not. Fixes typing runtime NameErrors caused by implicit stringified annotations by using explicit quotes for forward references and ensuring type hints used at runtime are imported globally instead of inside TYPE_CHECKING blocks.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:14:33Z",
          "tree_id": "098f2c44026744eb67c7126edacfa6cc23e940f8",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/422a8e4ab0b100e9004fca52f7ece2829469ef9b"
        },
        "date": 1772637428250,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 185949.84002379872,
            "unit": "iter/sec",
            "range": "stddev: 0.000002641421381828908",
            "extra": "mean: 5.377794355036903 usec\nrounds: 248"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154074.33387685925,
            "unit": "iter/sec",
            "range": "stddev: 9.7845819389779e-7",
            "extra": "mean: 6.490373671186724 usec\nrounds: 61051"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53661.67438530985,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020456694416495093",
            "extra": "mean: 18.635273898083117 usec\nrounds: 27565"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 149979.21364547857,
            "unit": "iter/sec",
            "range": "stddev: 0.000002075980181391961",
            "extra": "mean: 6.667590632684632 usec\nrounds: 1644"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108824.78156693005,
            "unit": "iter/sec",
            "range": "stddev: 0.000001395044729823914",
            "extra": "mean: 9.189083456923589 usec\nrounds: 44502"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 18981.018926542998,
            "unit": "iter/sec",
            "range": "stddev: 0.000013979799889174922",
            "extra": "mean: 52.684210677520745 usec\nrounds: 10096"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 28804.00147939217,
            "unit": "iter/sec",
            "range": "stddev: 0.000020136970073760593",
            "extra": "mean: 34.7173985779528 usec\nrounds: 17299"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4493373.992974843,
            "unit": "iter/sec",
            "range": "stddev: 3.7445527341113854e-8",
            "extra": "mean: 222.54991495525428 nsec\nrounds: 154036"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 589610.0359170972,
            "unit": "iter/sec",
            "range": "stddev: 2.6591705777648014e-7",
            "extra": "mean: 1.696036259702674 usec\nrounds: 183151"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1079708.4840799407,
            "unit": "iter/sec",
            "range": "stddev: 5.477119214085426e-7",
            "extra": "mean: 926.1759213202225 nsec\nrounds: 10067"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 629199.5300254422,
            "unit": "iter/sec",
            "range": "stddev: 3.535251966879789e-7",
            "extra": "mean: 1.5893209582651215 usec\nrounds: 147016"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2942305.7458447414,
            "unit": "iter/sec",
            "range": "stddev: 3.901166254033536e-8",
            "extra": "mean: 339.8695058839832 nsec\nrounds: 106068"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1136843.123147779,
            "unit": "iter/sec",
            "range": "stddev: 3.192669754257082e-7",
            "extra": "mean: 879.6288420438547 nsec\nrounds: 165536"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30482.894809265115,
            "unit": "iter/sec",
            "range": "stddev: 0.000003148936915836182",
            "extra": "mean: 32.805283299276915 usec\nrounds: 16149"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2499553.1914552418,
            "unit": "iter/sec",
            "range": "stddev: 4.3404849722348e-8",
            "extra": "mean: 400.0715021462919 nsec\nrounds: 90091"
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
          "id": "4ca07f102f3b8e25fdee09f5fd89c75544198c7f",
          "message": "Add test for validate_port with uncastable string (#107)\n\nAdds a test to `tests/test_security_validators_extended.py` to ensure that passing a string that cannot be cast to an integer to `validate_port` properly triggers the expected `ValueError` branch and re-raises with the correct error message. This improves the test coverage of `src/taipanstack/security/validators.py`.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:14:44Z",
          "tree_id": "763a8f3ccc191088661d941d34f972ed906a1dc1",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/4ca07f102f3b8e25fdee09f5fd89c75544198c7f"
        },
        "date": 1772637495242,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 229877.00820727134,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010884841953812868",
            "extra": "mean: 4.3501523175312 usec\nrounds: 302"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 165447.343422272,
            "unit": "iter/sec",
            "range": "stddev: 7.275158892728426e-7",
            "extra": "mean: 6.044219141359649 usec\nrounds: 59327"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 57802.791956177476,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014249485489703095",
            "extra": "mean: 17.300202397803528 usec\nrounds: 29694"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 168150.75854529304,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010637055434860643",
            "extra": "mean: 5.947044239652599 usec\nrounds: 1085"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 124922.38791864757,
            "unit": "iter/sec",
            "range": "stddev: 7.243107325835916e-7",
            "extra": "mean: 8.004970259223862 usec\nrounds: 41391"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 22756.050088937525,
            "unit": "iter/sec",
            "range": "stddev: 0.000002541636806349527",
            "extra": "mean: 43.94435748259024 usec\nrounds: 9883"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33174.46146811399,
            "unit": "iter/sec",
            "range": "stddev: 0.000010535337597569686",
            "extra": "mean: 30.1436694296051 usec\nrounds: 12185"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4645776.921887437,
            "unit": "iter/sec",
            "range": "stddev: 2.2768856850609717e-8",
            "extra": "mean: 215.24925040821134 nsec\nrounds: 154084"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 629554.3127747833,
            "unit": "iter/sec",
            "range": "stddev: 1.7511064861519988e-7",
            "extra": "mean: 1.5884253029615338 usec\nrounds: 191498"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1300484.4694330327,
            "unit": "iter/sec",
            "range": "stddev: 3.382489351555732e-7",
            "extra": "mean: 768.9442077197325 nsec\nrounds: 10324"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 685748.5832375379,
            "unit": "iter/sec",
            "range": "stddev: 2.723076579915067e-7",
            "extra": "mean: 1.458260395200274 usec\nrounds: 108343"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 3041077.121477019,
            "unit": "iter/sec",
            "range": "stddev: 3.4047695889368336e-8",
            "extra": "mean: 328.8308582961115 nsec\nrounds: 107527"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1146758.9107989941,
            "unit": "iter/sec",
            "range": "stddev: 2.1129551534058464e-7",
            "extra": "mean: 872.0228729709706 nsec\nrounds: 158178"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 31830.401865344887,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015896505787378655",
            "extra": "mean: 31.41650564860579 usec\nrounds: 17261"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2679390.8644965393,
            "unit": "iter/sec",
            "range": "stddev: 3.1633502744194397e-8",
            "extra": "mean: 373.2191571041617 nsec\nrounds: 104319"
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
          "id": "b3d44b869d8703eab5b42c3c4826256a15c0a080",
          "message": "🧪 [Testing Improvement] Add explicit raise test to `safe_from` decorator in Result module (#119)\n\n* Add test for explicitly raised exception in safe_from decorator\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n* Format tests/test_result_module.py using ruff\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n---------\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:14:16Z",
          "tree_id": "a160f0bf6c2ef3d6c46a9eb4cd86d02aff5d29c2",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/b3d44b869d8703eab5b42c3c4826256a15c0a080"
        },
        "date": 1772637583151,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 188101.6941392971,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026225293160264964",
            "extra": "mean: 5.316273224309498 usec\nrounds: 183"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154539.01332189282,
            "unit": "iter/sec",
            "range": "stddev: 8.348848950646699e-7",
            "extra": "mean: 6.4708579309813326 usec\nrounds: 73774"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53245.51465660319,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016967890914843632",
            "extra": "mean: 18.780924674112168 usec\nrounds: 25237"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 165216.22698120333,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010189027193987047",
            "extra": "mean: 6.052674233468424 usec\nrounds: 13568"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110622.97354685431,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011156954409545732",
            "extra": "mean: 9.039713614066345 usec\nrounds: 44028"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19631.890653573624,
            "unit": "iter/sec",
            "range": "stddev: 0.000009162406503861486",
            "extra": "mean: 50.93752902591521 usec\nrounds: 9147"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34440.51597847026,
            "unit": "iter/sec",
            "range": "stddev: 0.000014605986403172687",
            "extra": "mean: 29.035569636213587 usec\nrounds: 15861"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4307468.032187228,
            "unit": "iter/sec",
            "range": "stddev: 3.148722660619757e-8",
            "extra": "mean: 232.15494404766616 nsec\nrounds: 200000"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590952.5097729355,
            "unit": "iter/sec",
            "range": "stddev: 2.5913897794838327e-7",
            "extra": "mean: 1.692183353928373 usec\nrounds: 190115"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1062562.1813084325,
            "unit": "iter/sec",
            "range": "stddev: 3.541044462462521e-7",
            "extra": "mean: 941.1213927909671 nsec\nrounds: 10396"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 619395.2770236054,
            "unit": "iter/sec",
            "range": "stddev: 3.730314521333307e-7",
            "extra": "mean: 1.6144779224105863 usec\nrounds: 164420"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2896726.6322188815,
            "unit": "iter/sec",
            "range": "stddev: 5.36161611299071e-8",
            "extra": "mean: 345.21724931767983 nsec\nrounds: 111645"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1138885.09024454,
            "unit": "iter/sec",
            "range": "stddev: 2.8607743262095364e-7",
            "extra": "mean: 878.0517091371187 nsec\nrounds: 185151"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 28982.078416782875,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028046905927245462",
            "extra": "mean: 34.5040816472611 usec\nrounds: 13889"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2473438.69762551,
            "unit": "iter/sec",
            "range": "stddev: 4.250593728047729e-8",
            "extra": "mean: 404.29544542986616 nsec\nrounds: 81281"
          }
        ]
      }
    ]
  }
}