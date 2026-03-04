window.BENCHMARK_DATA = {
  "lastUpdate": 1772640626298,
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
          "id": "9c7d47ba65d887fa3d9875f9d6e8598967fab394",
          "message": "🧪 test: add coverage for ValueError inside validate_python_version (#118)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:14:19Z",
          "tree_id": "bd4844c9d4e334da076157bb4c335ec2e712e027",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/9c7d47ba65d887fa3d9875f9d6e8598967fab394"
        },
        "date": 1772637639649,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 186118.62677994347,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018058694604702404",
            "extra": "mean: 5.37291735545817 usec\nrounds: 242"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 153762.81940654543,
            "unit": "iter/sec",
            "range": "stddev: 8.174021664631287e-7",
            "extra": "mean: 6.50352278827577 usec\nrounds: 64814"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53731.39516783621,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014677554716419873",
            "extra": "mean: 18.611093139800012 usec\nrounds: 27346"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164530.99017183215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010887843798895252",
            "extra": "mean: 6.077882342746642 usec\nrounds: 11542"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108786.96316635133,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011528855999170423",
            "extra": "mean: 9.1922779246154 usec\nrounds: 42382"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19357.91424965694,
            "unit": "iter/sec",
            "range": "stddev: 0.000009050547235641526",
            "extra": "mean: 51.65845798793751 usec\nrounds: 10616"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 29158.184273495,
            "unit": "iter/sec",
            "range": "stddev: 0.000024366434036924173",
            "extra": "mean: 34.295688326142006 usec\nrounds: 11650"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4503169.631595473,
            "unit": "iter/sec",
            "range": "stddev: 2.998184276141372e-8",
            "extra": "mean: 222.0658073777432 nsec\nrounds: 152859"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 592999.5190992653,
            "unit": "iter/sec",
            "range": "stddev: 2.808745739367314e-7",
            "extra": "mean: 1.686342008368761 usec\nrounds: 189394"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1065527.7259563366,
            "unit": "iter/sec",
            "range": "stddev: 3.976492354714613e-7",
            "extra": "mean: 938.5020920994582 nsec\nrounds: 10755"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 617114.077478524,
            "unit": "iter/sec",
            "range": "stddev: 3.4805205036019565e-7",
            "extra": "mean: 1.6204459377849807 usec\nrounds: 142410"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 3014049.178539429,
            "unit": "iter/sec",
            "range": "stddev: 4.513671010435851e-8",
            "extra": "mean: 331.7795897689151 nsec\nrounds: 110060"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1136467.9426881564,
            "unit": "iter/sec",
            "range": "stddev: 2.789373103250741e-7",
            "extra": "mean: 879.9192325958966 nsec\nrounds: 180506"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 28760.867351462064,
            "unit": "iter/sec",
            "range": "stddev: 0.000002228592117631023",
            "extra": "mean: 34.76946601713543 usec\nrounds: 12933"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2475357.772327313,
            "unit": "iter/sec",
            "range": "stddev: 4.289462191902224e-8",
            "extra": "mean: 403.98200663308245 nsec\nrounds: 78101"
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
          "id": "e54df65f9c348b591c554c890282b7de9ae057bc",
          "message": "🧪 test: add coverage for log_operation expected_exceptions handling (#116)\n\n* test: improve testing coverage of log_operation expected_exceptions\n\nAdded explicit unit tests to ensure that `expected_exceptions` inside the `log_operation` context manager correctly captures and logs expected exceptions while allowing unexpected exceptions to bypass logging and bubble up.\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n* test: format test_utils_logging.py with ruff\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n* ci: remove openh264 repo on openSUSE Tumbleweed before installing dependencies\n\nThe `repo-openh264` repository periodically fails on `codecs.opensuse.org`,\ncausing zypper to fail its refresh and abort dependency installation for\nthe openSUSE container CI job. Removing this problematic repo allows zypper\nto proceed with installing the required system packages.\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n---------\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:14:24Z",
          "tree_id": "394ae1ed45a116ecde2cf8a77d82242b326b374b",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/e54df65f9c348b591c554c890282b7de9ae057bc"
        },
        "date": 1772637792327,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 201653.8938634806,
            "unit": "iter/sec",
            "range": "stddev: 0.000001648606363611644",
            "extra": "mean: 4.9589917697150865 usec\nrounds: 243"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 161320.25060777497,
            "unit": "iter/sec",
            "range": "stddev: 8.52598230850578e-7",
            "extra": "mean: 6.198849780064774 usec\nrounds: 66609"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 56086.8186629075,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016642856785464773",
            "extra": "mean: 17.82950118833074 usec\nrounds: 31136"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164147.24614306653,
            "unit": "iter/sec",
            "range": "stddev: 9.134760727792517e-7",
            "extra": "mean: 6.092091238182733 usec\nrounds: 11048"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 115250.17112885795,
            "unit": "iter/sec",
            "range": "stddev: 0.00000111288796506437",
            "extra": "mean: 8.676776704148477 usec\nrounds: 45742"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 20149.182733586535,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033902151122933706",
            "extra": "mean: 49.629804504830204 usec\nrounds: 10522"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 35338.82449988975,
            "unit": "iter/sec",
            "range": "stddev: 0.0000153560940544443",
            "extra": "mean: 28.297489069086602 usec\nrounds: 17885"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4059109.0728853364,
            "unit": "iter/sec",
            "range": "stddev: 4.160551814572577e-8",
            "extra": "mean: 246.35947988705124 nsec\nrounds: 146199"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 539670.0947326489,
            "unit": "iter/sec",
            "range": "stddev: 4.0464286093480885e-7",
            "extra": "mean: 1.8529839058346622 usec\nrounds: 175778"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1141530.588175217,
            "unit": "iter/sec",
            "range": "stddev: 3.968370175772056e-7",
            "extra": "mean: 876.0168236915497 nsec\nrounds: 10402"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 630040.3886350112,
            "unit": "iter/sec",
            "range": "stddev: 3.9861635320750387e-7",
            "extra": "mean: 1.587199833595605 usec\nrounds: 156250"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2317495.463891638,
            "unit": "iter/sec",
            "range": "stddev: 2.2354854132828704e-7",
            "extra": "mean: 431.5003052134381 nsec\nrounds: 188395"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1152730.67271377,
            "unit": "iter/sec",
            "range": "stddev: 3.03530214681904e-7",
            "extra": "mean: 867.5053277152676 nsec\nrounds: 149032"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 33675.13825746754,
            "unit": "iter/sec",
            "range": "stddev: 0.000002245413292640217",
            "extra": "mean: 29.69549797700527 usec\nrounds: 15077"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2787738.5033250237,
            "unit": "iter/sec",
            "range": "stddev: 4.8290462051359796e-8",
            "extra": "mean: 358.71370245348675 nsec\nrounds: 111075"
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
          "id": "42f427e6a0aa3ae160876f43dadab636e8c30a81",
          "message": "chore: preserve config package public API (#102)\n\nThe previously reported unused import issue was a false positive, as the imports were explicitly exported via __all__ in src/taipanstack/config/__init__.py, correctly defining the module's public API. The file is intentionally left untouched to prevent breaking downstream consumers while adhering to the rule to prioritize preserving functionality.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:15:57Z",
          "tree_id": "763a8f3ccc191088661d941d34f972ed906a1dc1",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/42f427e6a0aa3ae160876f43dadab636e8c30a81"
        },
        "date": 1772637800278,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 190985.48510758943,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011911154152546795",
            "extra": "mean: 5.2359999998778015 usec\nrounds: 177"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154984.43761877136,
            "unit": "iter/sec",
            "range": "stddev: 8.298505635627232e-7",
            "extra": "mean: 6.452260726072295 usec\nrounds: 48783"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53742.50510984231,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015701457879180844",
            "extra": "mean: 18.607245753731373 usec\nrounds: 27377"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 160433.45618672448,
            "unit": "iter/sec",
            "range": "stddev: 0.000001091464693366735",
            "extra": "mean: 6.233113863956936 usec\nrounds: 1897"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108710.58897959413,
            "unit": "iter/sec",
            "range": "stddev: 0.000001263618220229196",
            "extra": "mean: 9.198735922474931 usec\nrounds: 43953"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19170.297594352272,
            "unit": "iter/sec",
            "range": "stddev: 0.000003773026277337686",
            "extra": "mean: 52.164031104796635 usec\nrounds: 10545"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33507.723202597925,
            "unit": "iter/sec",
            "range": "stddev: 0.000014568099759914044",
            "extra": "mean: 29.84386596348832 usec\nrounds: 15548"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4297906.002707934,
            "unit": "iter/sec",
            "range": "stddev: 3.205466562047558e-8",
            "extra": "mean: 232.6714449710481 nsec\nrounds: 148965"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 585062.0956862884,
            "unit": "iter/sec",
            "range": "stddev: 2.9669166933746064e-7",
            "extra": "mean: 1.7092202816984052 usec\nrounds: 189754"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1065464.4655963636,
            "unit": "iter/sec",
            "range": "stddev: 3.5088375819810317e-7",
            "extra": "mean: 938.5578142582899 nsec\nrounds: 10084"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 598182.4666634803,
            "unit": "iter/sec",
            "range": "stddev: 4.5684633535915304e-7",
            "extra": "mean: 1.6717307104933425 usec\nrounds: 166334"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2931058.646879662,
            "unit": "iter/sec",
            "range": "stddev: 4.174565202293133e-8",
            "extra": "mean: 341.17365787423785 nsec\nrounds: 111521"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1128121.5489520403,
            "unit": "iter/sec",
            "range": "stddev: 2.7590802617443635e-7",
            "extra": "mean: 886.429304474276 nsec\nrounds: 189036"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30589.15622707649,
            "unit": "iter/sec",
            "range": "stddev: 0.000002309203206004637",
            "extra": "mean: 32.69132344078304 usec\nrounds: 19240"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2491281.048116063,
            "unit": "iter/sec",
            "range": "stddev: 4.3555731274947596e-8",
            "extra": "mean: 401.39991461669257 nsec\nrounds: 103649"
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
          "id": "6f5849e6d2d131998ecd3a5dea034625d2995e1c",
          "message": "Add test for UserAlreadyExistsError path in secure_system create_user (#101)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:00Z",
          "tree_id": "7f18f59d2c8dbf6a4dbf67279f4f0110bcb7401c",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/6f5849e6d2d131998ecd3a5dea034625d2995e1c"
        },
        "date": 1772637930726,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 220006.49953167228,
            "unit": "iter/sec",
            "range": "stddev: 8.05097277630227e-7",
            "extra": "mean: 4.545320261577269 usec\nrounds: 1530"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154596.05425505797,
            "unit": "iter/sec",
            "range": "stddev: 9.066928905643217e-7",
            "extra": "mean: 6.468470394141916 usec\nrounds: 66676"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53728.53622709946,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015490660569517555",
            "extra": "mean: 18.612083451765855 usec\nrounds: 22516"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 159316.99138971645,
            "unit": "iter/sec",
            "range": "stddev: 0.000001392409245630238",
            "extra": "mean: 6.2767944038927395 usec\nrounds: 1644"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108831.98694933647,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011410468810616313",
            "extra": "mean: 9.188475080083952 usec\nrounds: 42456"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19703.531123987592,
            "unit": "iter/sec",
            "range": "stddev: 0.000003728531525022322",
            "extra": "mean: 50.752324225913696 usec\nrounds: 10431"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33685.95160766938,
            "unit": "iter/sec",
            "range": "stddev: 0.00001529459121660628",
            "extra": "mean: 29.685965581341243 usec\nrounds: 16677"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4493148.0592808025,
            "unit": "iter/sec",
            "range": "stddev: 2.967812042901778e-8",
            "extra": "mean: 222.56110566702768 nsec\nrounds: 148987"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590518.8622113527,
            "unit": "iter/sec",
            "range": "stddev: 2.3861118375381977e-7",
            "extra": "mean: 1.6934260088750097 usec\nrounds: 185529"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1075370.8772656445,
            "unit": "iter/sec",
            "range": "stddev: 3.5616314475862066e-7",
            "extra": "mean: 929.9117366305375 nsec\nrounds: 9415"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 597127.8530848484,
            "unit": "iter/sec",
            "range": "stddev: 6.43207898076419e-7",
            "extra": "mean: 1.674683227107656 usec\nrounds: 141985"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2720273.442239717,
            "unit": "iter/sec",
            "range": "stddev: 2.511629500067833e-7",
            "extra": "mean: 367.6101028935332 nsec\nrounds: 114195"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1138902.8823157584,
            "unit": "iter/sec",
            "range": "stddev: 3.2980757861095165e-7",
            "extra": "mean: 878.037992112792 nsec\nrounds: 175747"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 31498.70801494843,
            "unit": "iter/sec",
            "range": "stddev: 0.000002163184967473919",
            "extra": "mean: 31.747333875580775 usec\nrounds: 11064"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2532032.220713458,
            "unit": "iter/sec",
            "range": "stddev: 4.274581495957515e-8",
            "extra": "mean: 394.9396819753414 nsec\nrounds: 54933"
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
          "id": "b347dba393f4637593583cdaf33b17e42319316b",
          "message": "chore: Remove unused imports from root __init__.py (#100)\n\nRemoved `apply_optimizations`, `get_optimization_profile`, `guard_path_traversal`, and `guard_command_injection` from `src/taipanstack/__init__.py`'s imports and `__all__` list.\nThese elements were verified to not be used externally, improving code maintainability.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:03Z",
          "tree_id": "cb793a3d2af9f258bab19317699aa33ced8924f7",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/b347dba393f4637593583cdaf33b17e42319316b"
        },
        "date": 1772637949669,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 217769.01654477452,
            "unit": "iter/sec",
            "range": "stddev: 8.881496398774993e-7",
            "extra": "mean: 4.592021472413613 usec\nrounds: 1630"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154203.02299006327,
            "unit": "iter/sec",
            "range": "stddev: 8.937645158069344e-7",
            "extra": "mean: 6.484957172755552 usec\nrounds: 64982"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53780.30155856037,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014536597326128177",
            "extra": "mean: 18.594168701548067 usec\nrounds: 23343"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 162341.82433411147,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010345590647664335",
            "extra": "mean: 6.1598420745964155 usec\nrounds: 1716"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109871.74334134623,
            "unit": "iter/sec",
            "range": "stddev: 0.000001033239971839976",
            "extra": "mean: 9.101521188147803 usec\nrounds: 41745"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19773.789719383887,
            "unit": "iter/sec",
            "range": "stddev: 0.000008126977235263583",
            "extra": "mean: 50.571995261976426 usec\nrounds: 10975"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34864.11162197801,
            "unit": "iter/sec",
            "range": "stddev: 0.000015394161032496523",
            "extra": "mean: 28.68279022401963 usec\nrounds: 17676"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4515506.507958284,
            "unit": "iter/sec",
            "range": "stddev: 3.3219929949454904e-8",
            "extra": "mean: 221.45909838403608 nsec\nrounds: 152626"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 591672.7528936856,
            "unit": "iter/sec",
            "range": "stddev: 2.511061621759457e-7",
            "extra": "mean: 1.6901234594787664 usec\nrounds: 188680"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1054102.1802640012,
            "unit": "iter/sec",
            "range": "stddev: 4.66796517174746e-7",
            "extra": "mean: 948.6746339425545 nsec\nrounds: 10041"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 614245.7954412724,
            "unit": "iter/sec",
            "range": "stddev: 3.7246423508289795e-7",
            "extra": "mean: 1.6280127717953734 usec\nrounds: 152602"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2935706.031397256,
            "unit": "iter/sec",
            "range": "stddev: 5.898905694731278e-8",
            "extra": "mean: 340.6335611620906 nsec\nrounds: 112146"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1136241.5003692978,
            "unit": "iter/sec",
            "range": "stddev: 2.631173898880124e-7",
            "extra": "mean: 880.0945922807634 nsec\nrounds: 188324"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29751.147805333585,
            "unit": "iter/sec",
            "range": "stddev: 0.000002215661306660771",
            "extra": "mean: 33.61214856459174 usec\nrounds: 16094"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2468689.3288102136,
            "unit": "iter/sec",
            "range": "stddev: 4.549708210130112e-8",
            "extra": "mean: 405.0732460863012 nsec\nrounds: 106975"
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
          "id": "0a21e1cc9f02852a7f49592993f7c74fdb4eabd5",
          "message": "refactor(core): remove unused compat imports from core package (#99)\n\nRemoved unused `compat` imports (`PY311`, `PY312`, `PythonFeatures`, etc.) from `src/taipanstack/core/__init__.py`.\nThese variables are internal utilities meant for direct submodule imports (`from taipanstack.core.compat import ...`), and keeping them in the core `__init__.py`'s `__all__` list violates the architectural principle of maintaining a minimal public API. Tests and linting successfully passed.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:07Z",
          "tree_id": "436f524bd3eb6d5a95ef50137f10cd1a16a8d97c",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/0a21e1cc9f02852a7f49592993f7c74fdb4eabd5"
        },
        "date": 1772638032240,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 206964.7624740013,
            "unit": "iter/sec",
            "range": "stddev: 6.845401297969397e-7",
            "extra": "mean: 4.831740379600219 usec\nrounds: 1949"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 151746.9076343255,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012182484096405617",
            "extra": "mean: 6.589920121533981 usec\nrounds: 76366"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52920.82384493392,
            "unit": "iter/sec",
            "range": "stddev: 0.000002420460147485439",
            "extra": "mean: 18.89615329742697 usec\nrounds: 29159"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 160755.2280632758,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018607887107925151",
            "extra": "mean: 6.220637499928675 usec\nrounds: 1120"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110296.24297353084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010228950629858221",
            "extra": "mean: 9.066491958751326 usec\nrounds: 45453"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19857.911079659978,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032346636986256896",
            "extra": "mean: 50.35776401598847 usec\nrounds: 11255"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33744.69355342167,
            "unit": "iter/sec",
            "range": "stddev: 0.000012583321234833057",
            "extra": "mean: 29.634288971001826 usec\nrounds: 17853"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4373072.273155784,
            "unit": "iter/sec",
            "range": "stddev: 2.838335821675551e-8",
            "extra": "mean: 228.67218686002894 nsec\nrounds: 196079"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 563017.1197640112,
            "unit": "iter/sec",
            "range": "stddev: 4.929358979236003e-7",
            "extra": "mean: 1.776144925076435 usec\nrounds: 158958"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 755349.8203130978,
            "unit": "iter/sec",
            "range": "stddev: 9.578080615167654e-7",
            "extra": "mean: 1.3238899025427622 usec\nrounds: 6467"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 607367.1173900565,
            "unit": "iter/sec",
            "range": "stddev: 3.904539771974654e-7",
            "extra": "mean: 1.646450674341975 usec\nrounds: 161265"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2918740.096105041,
            "unit": "iter/sec",
            "range": "stddev: 5.192919543337516e-8",
            "extra": "mean: 342.6135822557704 nsec\nrounds: 114587"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1131607.12644889,
            "unit": "iter/sec",
            "range": "stddev: 2.6947969095741446e-7",
            "extra": "mean: 883.6989239702935 nsec\nrounds: 183824"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29910.670480529134,
            "unit": "iter/sec",
            "range": "stddev: 0.000004890919045888884",
            "extra": "mean: 33.43288478441054 usec\nrounds: 16838"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2512548.0183656868,
            "unit": "iter/sec",
            "range": "stddev: 4.8237163625432955e-8",
            "extra": "mean: 398.00234371272876 nsec\nrounds: 105175"
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
          "id": "563fe0e9bae199891787de18fc8078b30f5647fe",
          "message": "Fix unused imports by defining __all__ in utils/__init__.py (#98)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:09Z",
          "tree_id": "f3fca0eced5e735b8423bf8d0e28ea0b4e5ac8f3",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/563fe0e9bae199891787de18fc8078b30f5647fe"
        },
        "date": 1772638108405,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 175017.4191831604,
            "unit": "iter/sec",
            "range": "stddev: 0.000002143733489919329",
            "extra": "mean: 5.713716981242155 usec\nrounds: 212"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154632.03940514367,
            "unit": "iter/sec",
            "range": "stddev: 7.964717002793705e-7",
            "extra": "mean: 6.466965085935069 usec\nrounds: 68597"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53568.13176353483,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016110958669655495",
            "extra": "mean: 18.667815491760813 usec\nrounds: 29435"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163176.72957584262,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012282212824328949",
            "extra": "mean: 6.128324808319018 usec\nrounds: 1564"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109262.03595589132,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011378466738824982",
            "extra": "mean: 9.152309777603781 usec\nrounds: 41278"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19084.04156601256,
            "unit": "iter/sec",
            "range": "stddev: 0.000003988665995406375",
            "extra": "mean: 52.399802030453294 usec\nrounds: 10047"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33805.23506504316,
            "unit": "iter/sec",
            "range": "stddev: 0.000015397982537657143",
            "extra": "mean: 29.581217171717462 usec\nrounds: 17028"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4408098.598661699,
            "unit": "iter/sec",
            "range": "stddev: 3.777351616643994e-8",
            "extra": "mean: 226.85517976028626 nsec\nrounds: 147864"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 569106.2298652929,
            "unit": "iter/sec",
            "range": "stddev: 4.997995354046358e-7",
            "extra": "mean: 1.7571411935461652 usec\nrounds: 186916"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 871200.2464724476,
            "unit": "iter/sec",
            "range": "stddev: 7.546675244645617e-7",
            "extra": "mean: 1.147841732195407 usec\nrounds: 7759"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 465591.31407081237,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010691282536178362",
            "extra": "mean: 2.147806391095837 usec\nrounds: 114065"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2922696.2748522973,
            "unit": "iter/sec",
            "range": "stddev: 4.193521434901039e-8",
            "extra": "mean: 342.1498185096067 nsec\nrounds: 111025"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1135062.7807579383,
            "unit": "iter/sec",
            "range": "stddev: 2.837710042005142e-7",
            "extra": "mean: 881.0085371068637 nsec\nrounds: 176992"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29099.070033179767,
            "unit": "iter/sec",
            "range": "stddev: 0.000004646750699584163",
            "extra": "mean: 34.36535940357425 usec\nrounds: 16967"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2342486.230998411,
            "unit": "iter/sec",
            "range": "stddev: 8.654463949021778e-8",
            "extra": "mean: 426.896852910742 nsec\nrounds: 174521"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "49699333+dependabot[bot]@users.noreply.github.com",
            "name": "dependabot[bot]",
            "username": "dependabot[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bcfcf1508a5e4f85c67fa798e66b1c36fbe8ea30",
          "message": "build(deps): bump the actions group with 2 updates (#95)\n\nBumps the actions group with 2 updates: [actions/upload-artifact](https://github.com/actions/upload-artifact) and [dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact).\n\n\nUpdates `actions/upload-artifact` from 4 to 7\n- [Release notes](https://github.com/actions/upload-artifact/releases)\n- [Commits](https://github.com/actions/upload-artifact/compare/v4...v7)\n\nUpdates `dawidd6/action-download-artifact` from 9 to 16\n- [Release notes](https://github.com/dawidd6/action-download-artifact/releases)\n- [Commits](https://github.com/dawidd6/action-download-artifact/compare/v9...v16)\n\n---\nupdated-dependencies:\n- dependency-name: actions/upload-artifact\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n  dependency-group: actions\n- dependency-name: dawidd6/action-download-artifact\n  dependency-version: '16'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n  dependency-group: actions\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:19Z",
          "tree_id": "3e5b1099bbb4362ebf03cbc611735137e36a1be1",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/bcfcf1508a5e4f85c67fa798e66b1c36fbe8ea30"
        },
        "date": 1772638191457,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 162691.95086199432,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022626579281075806",
            "extra": "mean: 6.146585585222121 usec\nrounds: 111"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 150896.3990747092,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028770200694028756",
            "extra": "mean: 6.627063376806609 usec\nrounds: 69852"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53614.753989834215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019614985851004933",
            "extra": "mean: 18.65158236461568 usec\nrounds: 26753"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 159112.4683512213,
            "unit": "iter/sec",
            "range": "stddev: 0.000001221586247714286",
            "extra": "mean: 6.284862590357296 usec\nrounds: 1521"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109799.48362437617,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012033705371099895",
            "extra": "mean: 9.107510955342907 usec\nrounds: 43951"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19319.40215161871,
            "unit": "iter/sec",
            "range": "stddev: 0.000003816621927264753",
            "extra": "mean: 51.7614361020076 usec\nrounds: 10908"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33462.279334860556,
            "unit": "iter/sec",
            "range": "stddev: 0.000015068644274498206",
            "extra": "mean: 29.88439579960751 usec\nrounds: 17284"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4427835.394612197,
            "unit": "iter/sec",
            "range": "stddev: 3.0783519483030565e-8",
            "extra": "mean: 225.84398715827393 nsec\nrounds: 153563"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 592327.4141382311,
            "unit": "iter/sec",
            "range": "stddev: 2.424634418141981e-7",
            "extra": "mean: 1.688255475149445 usec\nrounds: 189036"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1064104.891663468,
            "unit": "iter/sec",
            "range": "stddev: 2.7662832173270706e-7",
            "extra": "mean: 939.7569805705378 nsec\nrounds: 9419"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 616928.0662223066,
            "unit": "iter/sec",
            "range": "stddev: 3.8887385142526296e-7",
            "extra": "mean: 1.6209345217885671 usec\nrounds: 165536"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2181293.7413978204,
            "unit": "iter/sec",
            "range": "stddev: 1.7387623016618456e-7",
            "extra": "mean: 458.4435287285875 nsec\nrounds: 199243"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1097180.9410995764,
            "unit": "iter/sec",
            "range": "stddev: 2.722136063407653e-7",
            "extra": "mean: 911.4266959448063 nsec\nrounds: 160721"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29852.118827100247,
            "unit": "iter/sec",
            "range": "stddev: 0.000003294069533981483",
            "extra": "mean: 33.498459717110045 usec\nrounds: 15416"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2453161.7876093737,
            "unit": "iter/sec",
            "range": "stddev: 4.4612649554801096e-8",
            "extra": "mean: 407.6371990835564 nsec\nrounds: 75104"
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
          "id": "116e81465c8fb8ebc02ffe70b813ddabf0cd6196",
          "message": "security: fix plaintext password handling in UserService (#93)\n\nImplement secure password hashing using PBKDF2-HMAC-SHA256 with 600,000\niterations. Update User model to store password_hash instead of\ndiscarding the plaintext password. Add security utilities for password\nhashing and verification.\n\n- Created src/taipanstack/security/password.py with hash_password and verify_password\n- Exported password utilities in src/taipanstack/security/__init__.py\n- Updated User model and UserService.create_user in src/app/secure_system.py\n- Added tests in tests/test_security_password.py\n- Updated tests in tests/test_secure_system.py\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:26Z",
          "tree_id": "6a84cd7b14b30a09bda2a187dfeefac0fe9e0dff",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/116e81465c8fb8ebc02ffe70b813ddabf0cd6196"
        },
        "date": 1772638357299,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 227531.28556109586,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012113040182810086",
            "extra": "mean: 4.394999999819733 usec\nrounds: 189"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 164904.78752316104,
            "unit": "iter/sec",
            "range": "stddev: 5.804002210754969e-7",
            "extra": "mean: 6.064105324168039 usec\nrounds: 56948"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 58336.30841808126,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026539535369437937",
            "extra": "mean: 17.14198287682618 usec\nrounds: 25521"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 171400.64351610496,
            "unit": "iter/sec",
            "range": "stddev: 7.439669071291114e-7",
            "extra": "mean: 5.834283812977862 usec\nrounds: 12022"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 126030.13768694054,
            "unit": "iter/sec",
            "range": "stddev: 7.556822259269802e-7",
            "extra": "mean: 7.934610073060499 usec\nrounds: 39710"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 22434.24131626312,
            "unit": "iter/sec",
            "range": "stddev: 0.000003577213406793442",
            "extra": "mean: 44.574718881849414 usec\nrounds: 11376"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 36364.35764678021,
            "unit": "iter/sec",
            "range": "stddev: 0.00001639913838990957",
            "extra": "mean: 27.499454540441814 usec\nrounds: 18126"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4509795.773653811,
            "unit": "iter/sec",
            "range": "stddev: 4.2888637579963275e-8",
            "extra": "mean: 221.739531054146 nsec\nrounds: 153941"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 600057.8023577371,
            "unit": "iter/sec",
            "range": "stddev: 3.485860082552263e-7",
            "extra": "mean: 1.6665061200284652 usec\nrounds: 179084"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1262111.4802216871,
            "unit": "iter/sec",
            "range": "stddev: 2.843269646514509e-7",
            "extra": "mean: 792.323036174548 nsec\nrounds: 10974"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 663144.336244298,
            "unit": "iter/sec",
            "range": "stddev: 3.597829503588698e-7",
            "extra": "mean: 1.5079673388503565 usec\nrounds: 131165"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 3000982.3708719797,
            "unit": "iter/sec",
            "range": "stddev: 3.121598278848643e-8",
            "extra": "mean: 333.2242167452085 nsec\nrounds: 116118"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1116933.9578682934,
            "unit": "iter/sec",
            "range": "stddev: 2.4369928624824174e-7",
            "extra": "mean: 895.308082412083 nsec\nrounds: 169578"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 32395.78709042887,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017558380448465513",
            "extra": "mean: 30.86821126489758 usec\nrounds: 15819"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2632007.063093969,
            "unit": "iter/sec",
            "range": "stddev: 3.056885554455187e-8",
            "extra": "mean: 379.93819014470546 nsec\nrounds: 72177"
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
          "id": "2160d45c1c93dc442d8dc84f95fe6adf1ae406e1",
          "message": "test: add coverage for ValueError in validate_python_version (#89)\n\nAdded a test that mocks `re.match` to allow non-numeric versions (like \"a.b\") to pass the initial regex check and hit the int conversion ValueError handling block in `validate_python_version`.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:40Z",
          "tree_id": "95c6720eca312b8b55585ae31cd1054ff8328e87",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/2160d45c1c93dc442d8dc84f95fe6adf1ae406e1"
        },
        "date": 1772638373354,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 196016.20400350733,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027309072192590824",
            "extra": "mean: 5.101619047689072 usec\nrounds: 63"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 170040.01087779258,
            "unit": "iter/sec",
            "range": "stddev: 5.293986521545502e-7",
            "extra": "mean: 5.880968807504359 usec\nrounds: 60880"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 57818.23190866467,
            "unit": "iter/sec",
            "range": "stddev: 0.000001239793132247256",
            "extra": "mean: 17.295582500338263 usec\nrounds: 30412"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 176922.07976855728,
            "unit": "iter/sec",
            "range": "stddev: 8.139240659559098e-7",
            "extra": "mean: 5.652205769388207 usec\nrounds: 11717"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 126281.24949602493,
            "unit": "iter/sec",
            "range": "stddev: 7.554498967811949e-7",
            "extra": "mean: 7.918832003887306 usec\nrounds: 43126"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 22590.592345507066,
            "unit": "iter/sec",
            "range": "stddev: 0.00000222735434001776",
            "extra": "mean: 44.26621421455933 usec\nrounds: 11045"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 39652.25425034603,
            "unit": "iter/sec",
            "range": "stddev: 0.00001813981738169711",
            "extra": "mean: 25.219247150148426 usec\nrounds: 12106"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4621947.984224464,
            "unit": "iter/sec",
            "range": "stddev: 2.385895449769389e-8",
            "extra": "mean: 216.35899049776717 nsec\nrounds: 153234"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 628722.2363923354,
            "unit": "iter/sec",
            "range": "stddev: 2.1595264192697713e-7",
            "extra": "mean: 1.5905274891152712 usec\nrounds: 185049"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1292275.725190556,
            "unit": "iter/sec",
            "range": "stddev: 2.3018791158278312e-7",
            "extra": "mean: 773.8286655911163 nsec\nrounds: 10926"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 659078.6331948814,
            "unit": "iter/sec",
            "range": "stddev: 2.679706109232741e-7",
            "extra": "mean: 1.5172696392120975 usec\nrounds: 142572"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2958693.974416115,
            "unit": "iter/sec",
            "range": "stddev: 6.966707386029338e-8",
            "extra": "mean: 337.9869660893405 nsec\nrounds: 117014"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1138213.242277794,
            "unit": "iter/sec",
            "range": "stddev: 2.251963368931466e-7",
            "extra": "mean: 878.5699927359819 nsec\nrounds: 153023"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 32209.149405902626,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015256696670619857",
            "extra": "mean: 31.047078809747788 usec\nrounds: 18551"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2654021.074441878,
            "unit": "iter/sec",
            "range": "stddev: 3.177587992583818e-8",
            "extra": "mean: 376.7867593931716 nsec\nrounds: 108779"
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
          "id": "49479ad9cfaa066d482fdac4c71f49f1709b81f0",
          "message": "test: add tests for expected_exceptions in log_operation (#86)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:51Z",
          "tree_id": "7c8ba1b6aba6dd4deff4ca1347f61345f3ea68fd",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/49479ad9cfaa066d482fdac4c71f49f1709b81f0"
        },
        "date": 1772638493951,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 168460.131360145,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012759296878288134",
            "extra": "mean: 5.936122641755129 usec\nrounds: 106"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 152408.04517023047,
            "unit": "iter/sec",
            "range": "stddev: 0.000001437706084898251",
            "extra": "mean: 6.5613334183445575 usec\nrounds: 66676"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54026.25940686619,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018548708095512951",
            "extra": "mean: 18.50951761196538 usec\nrounds: 18794"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 162895.86257671448,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010905821350182657",
            "extra": "mean: 6.138891339422805 usec\nrounds: 11789"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 99328.37191387267,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031879559972375277",
            "extra": "mean: 10.067616942992855 usec\nrounds: 44821"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 18097.390388426156,
            "unit": "iter/sec",
            "range": "stddev: 0.000016371629122440127",
            "extra": "mean: 55.25658553730106 usec\nrounds: 10095"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33636.03346095571,
            "unit": "iter/sec",
            "range": "stddev: 0.000014745514331349163",
            "extra": "mean: 29.73002156038368 usec\nrounds: 17022"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4383329.926454431,
            "unit": "iter/sec",
            "range": "stddev: 4.7993815142005884e-8",
            "extra": "mean: 228.13705944530625 nsec\nrounds: 152393"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 586723.9794627301,
            "unit": "iter/sec",
            "range": "stddev: 2.9313084229151133e-7",
            "extra": "mean: 1.7043789499036701 usec\nrounds: 184129"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1052396.1066693563,
            "unit": "iter/sec",
            "range": "stddev: 3.730752974209763e-7",
            "extra": "mean: 950.2125612805804 nsec\nrounds: 10190"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 612753.8209629757,
            "unit": "iter/sec",
            "range": "stddev: 4.116132159123787e-7",
            "extra": "mean: 1.631976767486241 usec\nrounds: 141784"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2899302.223391881,
            "unit": "iter/sec",
            "range": "stddev: 4.347164171006762e-8",
            "extra": "mean: 344.9105760454292 nsec\nrounds: 110547"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1125561.7605633908,
            "unit": "iter/sec",
            "range": "stddev: 2.9925518984129235e-7",
            "extra": "mean: 888.4452502183959 nsec\nrounds: 162576"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30013.571003455072,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023955812826492246",
            "extra": "mean: 33.31826125871137 usec\nrounds: 17320"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2502009.8773690625,
            "unit": "iter/sec",
            "range": "stddev: 4.5893506358433184e-8",
            "extra": "mean: 399.678677948231 nsec\nrounds: 104406"
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
          "id": "90a91e78f5aad61e8d40cb84971defbbf7ee2d6b",
          "message": "test: add test for validate_port with invalid string (#85)\n\nAdds a test case to cover the scenario where a non-integer string is passed to `validate_port()`, ensuring the function correctly catches the `ValueError` and re-raises it with the expected message.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:54Z",
          "tree_id": "7c5c94fe2281ed55df5e3f5b6b6809346a60d770",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/90a91e78f5aad61e8d40cb84971defbbf7ee2d6b"
        },
        "date": 1772638587385,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 211076.57496674056,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013522518457239837",
            "extra": "mean: 4.737617142771861 usec\nrounds: 175"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155078.549381945,
            "unit": "iter/sec",
            "range": "stddev: 8.204344264759324e-7",
            "extra": "mean: 6.44834507406364 usec\nrounds: 48549"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54309.38977825594,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014130930459777855",
            "extra": "mean: 18.41302220634366 usec\nrounds: 30712"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163471.14799992,
            "unit": "iter/sec",
            "range": "stddev: 9.760769316632814e-7",
            "extra": "mean: 6.1172874371720285 usec\nrounds: 11940"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 111211.81730702333,
            "unit": "iter/sec",
            "range": "stddev: 0.000001154679289838813",
            "extra": "mean: 8.99185018476312 usec\nrounds: 40590"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 16121.185513728997,
            "unit": "iter/sec",
            "range": "stddev: 0.000020297616332650432",
            "extra": "mean: 62.030177566556 usec\nrounds: 10627"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34035.02264121213,
            "unit": "iter/sec",
            "range": "stddev: 0.000015339304930031522",
            "extra": "mean: 29.381499478984505 usec\nrounds: 16315"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4408727.381564961,
            "unit": "iter/sec",
            "range": "stddev: 3.049092178605523e-8",
            "extra": "mean: 226.8228251494403 nsec\nrounds: 151907"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 562446.5641009455,
            "unit": "iter/sec",
            "range": "stddev: 4.1793513919550907e-7",
            "extra": "mean: 1.7779466776518955 usec\nrounds: 171204"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1077468.196623352,
            "unit": "iter/sec",
            "range": "stddev: 3.423612618460377e-7",
            "extra": "mean: 928.1016396900369 nsec\nrounds: 9209"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 626938.6920955102,
            "unit": "iter/sec",
            "range": "stddev: 3.7136543539995533e-7",
            "extra": "mean: 1.5950522955562871 usec\nrounds: 162576"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2846679.9083227008,
            "unit": "iter/sec",
            "range": "stddev: 5.404249124637311e-8",
            "extra": "mean: 351.2864221496385 nsec\nrounds: 109686"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1129631.0135781046,
            "unit": "iter/sec",
            "range": "stddev: 2.927096644466778e-7",
            "extra": "mean: 885.2448170951872 nsec\nrounds: 162023"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29742.27546300208,
            "unit": "iter/sec",
            "range": "stddev: 0.000003755963482822248",
            "extra": "mean: 33.622175318897526 usec\nrounds: 22422"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2487306.39749734,
            "unit": "iter/sec",
            "range": "stddev: 4.993981524624225e-8",
            "extra": "mean: 402.0413411898905 nsec\nrounds: 31569"
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
          "id": "2cee426ab1c79ef614a1415339186082d64a6438",
          "message": "test: add test for ValueError in validate_port (#84)\n\nAdds a test case to explicitly check the exception handling branch when\na string that cannot be cast to an integer is passed to validate_port,\nensuring 100% test coverage for this module.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-04T15:16:56Z",
          "tree_id": "f058bc8c1964c8ad8782d9531b64c06e078cbf05",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/2cee426ab1c79ef614a1415339186082d64a6438"
        },
        "date": 1772638662761,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 151494.89818453253,
            "unit": "iter/sec",
            "range": "stddev: 0.000004039241566588625",
            "extra": "mean: 6.600882353027641 usec\nrounds: 68"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 156045.2086696554,
            "unit": "iter/sec",
            "range": "stddev: 8.789520631903644e-7",
            "extra": "mean: 6.408399261504915 usec\nrounds: 63372"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 51704.73448073938,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016184377794456738",
            "extra": "mean: 19.3405886335711 usec\nrounds: 30722"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 161117.70287436986,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012757570451585634",
            "extra": "mean: 6.206642610711384 usec\nrounds: 10725"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109342.86840087737,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013886384547981681",
            "extra": "mean: 9.145543871537726 usec\nrounds: 41348"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19108.497690086453,
            "unit": "iter/sec",
            "range": "stddev: 0.000006517835000681988",
            "extra": "mean: 52.33273783311615 usec\nrounds: 6267"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 29693.3085425929,
            "unit": "iter/sec",
            "range": "stddev: 0.00001980653272139098",
            "extra": "mean: 33.6776212918669 usec\nrounds: 11967"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4356256.657229602,
            "unit": "iter/sec",
            "range": "stddev: 5.37185100708544e-8",
            "extra": "mean: 229.55488592269228 nsec\nrounds: 82707"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 591586.5604207097,
            "unit": "iter/sec",
            "range": "stddev: 2.7537887592037606e-7",
            "extra": "mean: 1.6903697056417994 usec\nrounds: 185874"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1061629.104340316,
            "unit": "iter/sec",
            "range": "stddev: 3.3054355771160803e-7",
            "extra": "mean: 941.948554265935 nsec\nrounds: 7989"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 618330.7095357168,
            "unit": "iter/sec",
            "range": "stddev: 3.6954493025076855e-7",
            "extra": "mean: 1.617257536425557 usec\nrounds: 152161"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2922249.011213092,
            "unit": "iter/sec",
            "range": "stddev: 4.189924407094413e-8",
            "extra": "mean: 342.20218611160345 nsec\nrounds: 108366"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1145592.3496278853,
            "unit": "iter/sec",
            "range": "stddev: 2.83071781654871e-7",
            "extra": "mean: 872.9108572738138 nsec\nrounds: 172981"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30144.532863647815,
            "unit": "iter/sec",
            "range": "stddev: 0.000002258068892416077",
            "extra": "mean: 33.17351124740532 usec\nrounds: 14670"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2456973.86629068,
            "unit": "iter/sec",
            "range": "stddev: 6.983609461198775e-8",
            "extra": "mean: 407.00473607803747 nsec\nrounds: 76424"
          }
        ]
      },
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
          "id": "3bd9376ac884e14dbeb758f1a31f848e05c7a58e",
          "message": "release: bump version to v0.3.4\n\n- Bump version to 0.3.4 in pyproject.toml and __init__.py\n- Add CHANGELOG.md entry for v0.3.4 with full list of changes\n- Add docs/releases/v0.3.4.md release notes document\n- Update mkdocs.yml navigation to include v0.3.4 release notes\n\nChanges since v0.3.3:\n- Security: fix plaintext password storage in UserService (#93)\n- Security: new password module with hash_password, verify_password, generate_secure_token\n- Test: CVE-2020-10735 coverage in get_optimization_level (#129)\n- Test: validate_url lazy port evaluation fix and tests (#115, #126)\n- Test: validate_ip_address exception chaining (#128)\n- Test: validate_port string and large-int edge cases (#114)\n- Test: @safe/@safe_from base Exception coverage (#127, #117, #119)\n- Test: log_operation expected_exceptions coverage (#116)\n- Test: path traversal SecurityError without base_dir (#120)\n- Test: SSRF DNS resolution platform-independent mocking (#122)\n- Perf: optimize string concatenation in generate_pre_commit_config (#130)\n- Refactor: remove unused compat imports from core public API (#99)\n- Refactor: remove unused imports from root __init__.py (#100)\n- Refactor: define __all__ in utils/__init__.py (#98)\n- Refactor: remove redundant __future__ import annotations (#112)\n- Refactor: preserve config package public API (#102)\n- CI: openSUSE Leap repo fix (#116)\n- Deps: bump GitHub Actions group (#95)",
          "timestamp": "2026-03-04T13:01:00-03:00",
          "tree_id": "47caa82e80eebb11b7df3f2a00c5e96a11c33f4e",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/3bd9376ac884e14dbeb758f1a31f848e05c7a58e"
        },
        "date": 1772640197154,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 200005.66056437284,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019238059508167785",
            "extra": "mean: 4.999858489895814 usec\nrounds: 212"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 156720.1921201915,
            "unit": "iter/sec",
            "range": "stddev: 9.155701493011605e-7",
            "extra": "mean: 6.380798711841052 usec\nrounds: 65364"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53499.98057305416,
            "unit": "iter/sec",
            "range": "stddev: 0.00000194374351143312",
            "extra": "mean: 18.69159557234794 usec\nrounds: 31348"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 161539.50703402754,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010662614772202972",
            "extra": "mean: 6.190436125259159 usec\nrounds: 11820"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109170.66093091642,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012396196142767803",
            "extra": "mean: 9.1599701922919 usec\nrounds: 44049"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19214.608675271098,
            "unit": "iter/sec",
            "range": "stddev: 0.000003771788816572465",
            "extra": "mean: 52.04373489463693 usec\nrounds: 8838"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33382.638494422674,
            "unit": "iter/sec",
            "range": "stddev: 0.000014518781510976019",
            "extra": "mean: 29.95569089504632 usec\nrounds: 16881"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4427446.316498875,
            "unit": "iter/sec",
            "range": "stddev: 3.276466561868681e-8",
            "extra": "mean: 225.86383402855313 nsec\nrounds: 152161"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 591946.7195866142,
            "unit": "iter/sec",
            "range": "stddev: 2.4186954600506666e-7",
            "extra": "mean: 1.689341231079803 usec\nrounds: 193051"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1080779.365862173,
            "unit": "iter/sec",
            "range": "stddev: 4.464522340485032e-7",
            "extra": "mean: 925.2582271519102 nsec\nrounds: 10119"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 615979.4015710774,
            "unit": "iter/sec",
            "range": "stddev: 4.076754352175533e-7",
            "extra": "mean: 1.6234309092957724 usec\nrounds: 138832"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2970946.1429512305,
            "unit": "iter/sec",
            "range": "stddev: 3.854387948994337e-8",
            "extra": "mean: 336.5931093609902 nsec\nrounds: 109939"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1137039.2795752934,
            "unit": "iter/sec",
            "range": "stddev: 2.93672278581414e-7",
            "extra": "mean: 879.4770927997489 nsec\nrounds: 162023"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29548.398295234365,
            "unit": "iter/sec",
            "range": "stddev: 0.0000038318481188203156",
            "extra": "mean: 33.84278193384453 usec\nrounds: 19329"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2512067.2554874886,
            "unit": "iter/sec",
            "range": "stddev: 5.4288404419873464e-8",
            "extra": "mean: 398.078513947251 nsec\nrounds: 102271"
          }
        ]
      },
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
          "id": "060cb07b8451644a37ec432b498ce9fbbc73734e",
          "message": "Revert \"release: bump version to v0.3.4\"\n\nThis reverts commit 3bd9376ac884e14dbeb758f1a31f848e05c7a58e.",
          "timestamp": "2026-03-04T13:09:41-03:00",
          "tree_id": "f058bc8c1964c8ad8782d9531b64c06e078cbf05",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/060cb07b8451644a37ec432b498ce9fbbc73734e"
        },
        "date": 1772640625635,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 201366.26612584156,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013120388764525537",
            "extra": "mean: 4.966075099068785 usec\nrounds: 253"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155887.55476984358,
            "unit": "iter/sec",
            "range": "stddev: 8.946618713940656e-7",
            "extra": "mean: 6.414880273646128 usec\nrounds: 62267"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54117.960238590145,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016802280695327514",
            "extra": "mean: 18.478153936166375 usec\nrounds: 25660"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 162921.68265579757,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010207516277820967",
            "extra": "mean: 6.137918438472591 usec\nrounds: 10630"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109230.75439222949,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013461829704315868",
            "extra": "mean: 9.154930821123566 usec\nrounds: 31339"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 18927.464362353494,
            "unit": "iter/sec",
            "range": "stddev: 0.000008734457317272567",
            "extra": "mean: 52.833278713708125 usec\nrounds: 10387"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33050.45889360758,
            "unit": "iter/sec",
            "range": "stddev: 0.000017386097197628404",
            "extra": "mean: 30.256765971664432 usec\nrounds: 16639"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4358878.894662121,
            "unit": "iter/sec",
            "range": "stddev: 3.073340549229017e-8",
            "extra": "mean: 229.41678907954685 nsec\nrounds: 152626"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590134.0329780993,
            "unit": "iter/sec",
            "range": "stddev: 2.5065213748077707e-7",
            "extra": "mean: 1.6945303000973688 usec\nrounds: 185874"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1028327.548964178,
            "unit": "iter/sec",
            "range": "stddev: 3.9431399901934363e-7",
            "extra": "mean: 972.4527958113036 nsec\nrounds: 9925"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 602098.9900988841,
            "unit": "iter/sec",
            "range": "stddev: 3.9859314896725885e-7",
            "extra": "mean: 1.6608564645420973 usec\nrounds: 147211"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2935331.9687129054,
            "unit": "iter/sec",
            "range": "stddev: 4.073498325267518e-8",
            "extra": "mean: 340.67696964390274 nsec\nrounds: 109195"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1132762.1321102318,
            "unit": "iter/sec",
            "range": "stddev: 2.7936569229520854e-7",
            "extra": "mean: 882.7978722568099 nsec\nrounds: 163372"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30113.221479079355,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021475990822122654",
            "extra": "mean: 33.20800468640437 usec\nrounds: 14510"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2449698.1334008677,
            "unit": "iter/sec",
            "range": "stddev: 8.946908797635269e-8",
            "extra": "mean: 408.2135616488168 nsec\nrounds: 91744"
          }
        ]
      }
    ]
  }
}