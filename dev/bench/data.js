window.BENCHMARK_DATA = {
  "lastUpdate": 1772637289438,
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
      }
    ]
  }
}