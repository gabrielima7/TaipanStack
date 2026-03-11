window.BENCHMARK_DATA = {
  "lastUpdate": 1773254615348,
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
          "id": "98842f47e1ce2f11d695c0ccabb583c3900cac17",
          "message": "docs: release notes for v0.3.4",
          "timestamp": "2026-03-04T13:49:24-03:00",
          "tree_id": "b44e84c51ec1e1261ce3ba3215461cba917c5922",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/98842f47e1ce2f11d695c0ccabb583c3900cac17"
        },
        "date": 1772643027800,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 149962.85011352357,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011914703218222066",
            "extra": "mean: 6.668318181756273 usec\nrounds: 44"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 153781.31826966518,
            "unit": "iter/sec",
            "range": "stddev: 8.101078577417649e-7",
            "extra": "mean: 6.502740458021288 usec\nrounds: 68644"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52816.070587397924,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013745604559651934",
            "extra": "mean: 18.933631163364186 usec\nrounds: 32044"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164813.21379655867,
            "unit": "iter/sec",
            "range": "stddev: 9.340867955278775e-7",
            "extra": "mean: 6.0674746700490605 usec\nrounds: 12120"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109077.33330916744,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012007319449196165",
            "extra": "mean: 9.167807551415034 usec\nrounds: 22936"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19897.272901477972,
            "unit": "iter/sec",
            "range": "stddev: 0.00000341716045773251",
            "extra": "mean: 50.25814366378419 usec\nrounds: 10803"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34403.724143769854,
            "unit": "iter/sec",
            "range": "stddev: 0.000013608901120612486",
            "extra": "mean: 29.066620689699064 usec\nrounds: 17429"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4420133.161422372,
            "unit": "iter/sec",
            "range": "stddev: 2.8818963741922627e-8",
            "extra": "mean: 226.2375280291666 nsec\nrounds: 154751"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590812.9226043392,
            "unit": "iter/sec",
            "range": "stddev: 2.2765474444576775e-7",
            "extra": "mean: 1.6925831540581637 usec\nrounds: 190115"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1051433.4192569319,
            "unit": "iter/sec",
            "range": "stddev: 4.065533509022462e-7",
            "extra": "mean: 951.0825713593155 nsec\nrounds: 11154"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 610493.6513418497,
            "unit": "iter/sec",
            "range": "stddev: 3.9657865940026476e-7",
            "extra": "mean: 1.6380186719420016 usec\nrounds: 163079"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2890478.1143944194,
            "unit": "iter/sec",
            "range": "stddev: 5.049503891696831e-8",
            "extra": "mean: 345.96352590249967 nsec\nrounds: 109087"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1348680.9458525907,
            "unit": "iter/sec",
            "range": "stddev: 1.2152282849650849e-7",
            "extra": "mean: 741.4652094516201 nsec\nrounds: 187618"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29572.254329106785,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020764766647249895",
            "extra": "mean: 33.81548085144595 usec\nrounds: 22221"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2520352.668436354,
            "unit": "iter/sec",
            "range": "stddev: 4.472594463276173e-8",
            "extra": "mean: 396.7698697581606 nsec\nrounds: 89679"
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
          "id": "018342ed80fb62280be579ed540251407a3cdf4c",
          "message": "fix: resolve strict mypy typing and duplication in decorators",
          "timestamp": "2026-03-04T17:26:59-03:00",
          "tree_id": "5b3d758427d1636be8e901c66b75c261e211d6cd",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/018342ed80fb62280be579ed540251407a3cdf4c"
        },
        "date": 1772656109382,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 207572.5402244335,
            "unit": "iter/sec",
            "range": "stddev: 0.000001249530701568444",
            "extra": "mean: 4.817592919173079 usec\nrounds: 113"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 166053.50714114256,
            "unit": "iter/sec",
            "range": "stddev: 6.292513498676234e-7",
            "extra": "mean: 6.022155251138524 usec\nrounds: 51246"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 58349.37792667075,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015226945381883034",
            "extra": "mean: 17.138143293605072 usec\nrounds: 14076"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 131748.4275027417,
            "unit": "iter/sec",
            "range": "stddev: 0.000002921439235679193",
            "extra": "mean: 7.590223420155735 usec\nrounds: 6772"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 124990.88346743463,
            "unit": "iter/sec",
            "range": "stddev: 7.790246680311768e-7",
            "extra": "mean: 8.000583500640206 usec\nrounds: 39832"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 22933.50623326481,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024934001575660837",
            "extra": "mean: 43.6043224192867 usec\nrounds: 10995"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 39858.76689824256,
            "unit": "iter/sec",
            "range": "stddev: 0.000019545175151968172",
            "extra": "mean: 25.088583461524284 usec\nrounds: 15600"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4640167.656078977,
            "unit": "iter/sec",
            "range": "stddev: 2.281886108934651e-8",
            "extra": "mean: 215.5094544245517 nsec\nrounds: 152976"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 629447.7244250324,
            "unit": "iter/sec",
            "range": "stddev: 1.8694674516295825e-7",
            "extra": "mean: 1.5886942810277949 usec\nrounds: 192605"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1273977.1055301488,
            "unit": "iter/sec",
            "range": "stddev: 3.6135189749722617e-7",
            "extra": "mean: 784.9434622169784 nsec\nrounds: 8879"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 671941.5882531754,
            "unit": "iter/sec",
            "range": "stddev: 3.1023862980020066e-7",
            "extra": "mean: 1.488224597914333 usec\nrounds: 129133"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2257106.7110675955,
            "unit": "iter/sec",
            "range": "stddev: 1.629925397172998e-7",
            "extra": "mean: 443.045069644495 nsec\nrounds: 158932"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1161953.9522718317,
            "unit": "iter/sec",
            "range": "stddev: 1.9453799658868385e-7",
            "extra": "mean: 860.6193025505165 nsec\nrounds: 108732"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 32260.57371953105,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025530662120637155",
            "extra": "mean: 30.997588843083236 usec\nrounds: 18392"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2556038.6312404214,
            "unit": "iter/sec",
            "range": "stddev: 1.0439980708143134e-7",
            "extra": "mean: 391.23039369507757 nsec\nrounds: 68302"
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
          "id": "0a51485a4c7b41305e9679c52502b63efeea63d5",
          "message": "fix(ci): resolve unwrap error in sec-types and format files",
          "timestamp": "2026-03-04T17:39:54-03:00",
          "tree_id": "f939826a4e0379b0a07a4a59a7fef9b7e84e7e5e",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/0a51485a4c7b41305e9679c52502b63efeea63d5"
        },
        "date": 1772656835961,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 178911.60559913155,
            "unit": "iter/sec",
            "range": "stddev: 0.000002344975821314273",
            "extra": "mean: 5.589352332126485 usec\nrounds: 193"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154450.05696203455,
            "unit": "iter/sec",
            "range": "stddev: 8.179126800494765e-7",
            "extra": "mean: 6.47458485719957 usec\nrounds: 66989"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53322.58255582684,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016288445727816467",
            "extra": "mean: 18.753780332245455 usec\nrounds: 30100"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 138939.4322961551,
            "unit": "iter/sec",
            "range": "stddev: 0.000003349497596931549",
            "extra": "mean: 7.197380782933235 usec\nrounds: 8430"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109219.15252210893,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013920055031096653",
            "extra": "mean: 9.155903309152421 usec\nrounds: 41400"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 18214.972708820973,
            "unit": "iter/sec",
            "range": "stddev: 0.000013828809528484014",
            "extra": "mean: 54.89989010610647 usec\nrounds: 5842"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33770.08890176671,
            "unit": "iter/sec",
            "range": "stddev: 0.000014570321220664903",
            "extra": "mean: 29.612003773779946 usec\nrounds: 16694"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4282217.325942796,
            "unit": "iter/sec",
            "range": "stddev: 3.542576507123569e-8",
            "extra": "mean: 233.52387884226454 nsec\nrounds: 145943"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 588934.8723578108,
            "unit": "iter/sec",
            "range": "stddev: 2.672232715877684e-7",
            "extra": "mean: 1.6979806204996777 usec\nrounds: 190115"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1057802.8260294818,
            "unit": "iter/sec",
            "range": "stddev: 2.611933973775792e-7",
            "extra": "mean: 945.3557651699156 nsec\nrounds: 9540"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 617557.8847059173,
            "unit": "iter/sec",
            "range": "stddev: 3.973670045039951e-7",
            "extra": "mean: 1.6192814062704461 usec\nrounds: 153799"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2920387.4257037253,
            "unit": "iter/sec",
            "range": "stddev: 4.0256613676158946e-8",
            "extra": "mean: 342.4203210841816 nsec\nrounds: 108850"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1126213.5223033272,
            "unit": "iter/sec",
            "range": "stddev: 3.0224302742720113e-7",
            "extra": "mean: 887.9310896168288 nsec\nrounds: 159439"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30330.89392074282,
            "unit": "iter/sec",
            "range": "stddev: 0.000002084395878779543",
            "extra": "mean: 32.96968439549075 usec\nrounds: 16790"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2473843.558801727,
            "unit": "iter/sec",
            "range": "stddev: 5.799995555261374e-8",
            "extra": "mean: 404.2292797546173 nsec\nrounds: 76488"
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
          "id": "464fd9ba6bb49e1864227f3d79aacd6476e1f946",
          "message": "chore: bump version to v0.3.5 (re-release of v0.3.4 due to PyPI immutability)",
          "timestamp": "2026-03-04T18:09:53-03:00",
          "tree_id": "6355951c1b68dadf0a679a51b0bea0f9b04cd8eb",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/464fd9ba6bb49e1864227f3d79aacd6476e1f946"
        },
        "date": 1772658640880,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 174284.4248422624,
            "unit": "iter/sec",
            "range": "stddev: 0.000001616565721403098",
            "extra": "mean: 5.7377473684470575 usec\nrounds: 190"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 149075.6921285141,
            "unit": "iter/sec",
            "range": "stddev: 8.940133152912565e-7",
            "extra": "mean: 6.708001725310972 usec\nrounds: 57961"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52864.10680067022,
            "unit": "iter/sec",
            "range": "stddev: 0.000001861887870107944",
            "extra": "mean: 18.916426674352167 usec\nrounds: 31251"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164292.28817272824,
            "unit": "iter/sec",
            "range": "stddev: 9.690763242365761e-7",
            "extra": "mean: 6.0867129621364375 usec\nrounds: 11333"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108146.7733930437,
            "unit": "iter/sec",
            "range": "stddev: 0.000001323382122441812",
            "extra": "mean: 9.246692884360458 usec\nrounds: 41486"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19493.113025877024,
            "unit": "iter/sec",
            "range": "stddev: 0.0000039494286387366634",
            "extra": "mean: 51.30016938148895 usec\nrounds: 10314"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34301.14910367698,
            "unit": "iter/sec",
            "range": "stddev: 0.000014905793023598488",
            "extra": "mean: 29.15354226114842 usec\nrounds: 16398"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4469049.232213976,
            "unit": "iter/sec",
            "range": "stddev: 3.602776597583726e-8",
            "extra": "mean: 223.76124048751623 nsec\nrounds: 149433"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 584424.9463429828,
            "unit": "iter/sec",
            "range": "stddev: 5.449932192323385e-7",
            "extra": "mean: 1.711083700751343 usec\nrounds: 191205"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1035653.6124547425,
            "unit": "iter/sec",
            "range": "stddev: 3.70778358880352e-7",
            "extra": "mean: 965.5738057339122 nsec\nrounds: 7811"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 601182.5065631645,
            "unit": "iter/sec",
            "range": "stddev: 4.611170563020221e-7",
            "extra": "mean: 1.6633883871917567 usec\nrounds: 161787"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2912677.0894331513,
            "unit": "iter/sec",
            "range": "stddev: 4.273745155582033e-8",
            "extra": "mean: 343.32676410572617 nsec\nrounds: 111657"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1107568.8878708328,
            "unit": "iter/sec",
            "range": "stddev: 3.529040079997878e-7",
            "extra": "mean: 902.8783770934367 nsec\nrounds: 42418"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30009.012224570226,
            "unit": "iter/sec",
            "range": "stddev: 0.000002246685585987249",
            "extra": "mean: 33.32332275772938 usec\nrounds: 19668"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2538385.737252711,
            "unit": "iter/sec",
            "range": "stddev: 7.932719586714602e-8",
            "extra": "mean: 393.95115774729976 nsec\nrounds: 106068"
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
          "distinct": false,
          "id": "d9dae47687fc02ef9ba361ef3d8b9557483a25bb",
          "message": "fix(qa): resolve validation, lint, and security issues",
          "timestamp": "2026-03-05T17:33:49-03:00",
          "tree_id": "73cffc7d95912fe540291fc8987d23df8255a338",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/d9dae47687fc02ef9ba361ef3d8b9557483a25bb"
        },
        "date": 1772742901720,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 197751.3556630662,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017678694819612377",
            "extra": "mean: 5.05685534567877 usec\nrounds: 159"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155819.76185439198,
            "unit": "iter/sec",
            "range": "stddev: 8.083285930428608e-7",
            "extra": "mean: 6.417671212554312 usec\nrounds: 65407"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52596.05194020059,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020301285641855795",
            "extra": "mean: 19.012833912647213 usec\nrounds: 23879"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 157903.17226179808,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010811695209158176",
            "extra": "mean: 6.332994997352137 usec\nrounds: 10994"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108897.70066656674,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011554598356488678",
            "extra": "mean: 9.182930345443145 usec\nrounds: 42438"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19498.96743439712,
            "unit": "iter/sec",
            "range": "stddev: 0.000003105022472747876",
            "extra": "mean: 51.28476691724464 usec\nrounds: 1064"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33960.46350159073,
            "unit": "iter/sec",
            "range": "stddev: 0.000016512780859383962",
            "extra": "mean: 29.446005645746244 usec\nrounds: 17004"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4408563.3935508225,
            "unit": "iter/sec",
            "range": "stddev: 3.4630468438249986e-8",
            "extra": "mean: 226.83126241595042 nsec\nrounds: 151012"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 568053.2397567343,
            "unit": "iter/sec",
            "range": "stddev: 5.257745410183443e-7",
            "extra": "mean: 1.7603983746806922 usec\nrounds: 186220"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1039891.4793935416,
            "unit": "iter/sec",
            "range": "stddev: 4.43677381273335e-7",
            "extra": "mean: 961.6388054099588 nsec\nrounds: 10313"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 623019.3398826008,
            "unit": "iter/sec",
            "range": "stddev: 4.11868478331882e-7",
            "extra": "mean: 1.6050866096523357 usec\nrounds: 154036"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2848100.2714114245,
            "unit": "iter/sec",
            "range": "stddev: 3.883187758457945e-8",
            "extra": "mean: 351.11123370138523 nsec\nrounds: 113431"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1117890.9690359537,
            "unit": "iter/sec",
            "range": "stddev: 3.096482958840932e-7",
            "extra": "mean: 894.5416214090892 nsec\nrounds: 157431"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29988.474752352537,
            "unit": "iter/sec",
            "range": "stddev: 0.000002065914421294408",
            "extra": "mean: 33.34614408562249 usec\nrounds: 15234"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2535149.088140007,
            "unit": "iter/sec",
            "range": "stddev: 4.47500919459721e-8",
            "extra": "mean: 394.45411896223004 nsec\nrounds: 107782"
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
          "id": "83848c4e6bca72b4dc4ad43cc988a1d99f50a76a",
          "message": "test: Add tests for normalize_ext inner function in guards.py (#138)\n\nAdds tests specifically targeting the nested helper function `normalize_ext` within `guard_file_extension` in `src/taipanstack/security/guards.py`. The new tests check if extensions containing uppercase characters and leading dots are properly normalized and verified against `denied_extensions` and `allowed_extensions` configuration, ensuring the normalization path hits 100% test coverage.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-05T20:43:37Z",
          "tree_id": "70d8ec69c4515f8b543bd2293b8424fc982be780",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/83848c4e6bca72b4dc4ad43cc988a1d99f50a76a"
        },
        "date": 1772743455313,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 156808.63074646684,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014800258315800278",
            "extra": "mean: 6.3772000000231595 usec\nrounds: 35"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155151.32851285883,
            "unit": "iter/sec",
            "range": "stddev: 7.975430469329126e-7",
            "extra": "mean: 6.445320253362321 usec\nrounds: 64730"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54412.69992404162,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017947932558213322",
            "extra": "mean: 18.37806250004076 usec\nrounds: 26512"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 160942.74294029502,
            "unit": "iter/sec",
            "range": "stddev: 9.776228776034748e-7",
            "extra": "mean: 6.2133898163458685 usec\nrounds: 11921"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 107861.37085751009,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020668919554565573",
            "extra": "mean: 9.271159749314208 usec\nrounds: 43080"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19540.28706592041,
            "unit": "iter/sec",
            "range": "stddev: 0.000005964615064276931",
            "extra": "mean: 51.17632083021278 usec\nrounds: 6745"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33267.5850238221,
            "unit": "iter/sec",
            "range": "stddev: 0.000017326081138614677",
            "extra": "mean: 30.059290425918334 usec\nrounds: 16858"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4097507.3286430133,
            "unit": "iter/sec",
            "range": "stddev: 6.414499298898083e-8",
            "extra": "mean: 244.05081426196654 nsec\nrounds: 147864"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590529.6106176999,
            "unit": "iter/sec",
            "range": "stddev: 2.2831232779436135e-7",
            "extra": "mean: 1.6933951863209822 usec\nrounds: 184502"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1041986.2924812039,
            "unit": "iter/sec",
            "range": "stddev: 4.1747779346889615e-7",
            "extra": "mean: 959.7055232068121 nsec\nrounds: 10646"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 587862.2701992595,
            "unit": "iter/sec",
            "range": "stddev: 3.8359248833592245e-7",
            "extra": "mean: 1.7010787231863747 usec\nrounds: 148965"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2163582.507570365,
            "unit": "iter/sec",
            "range": "stddev: 2.0140414811948898e-7",
            "extra": "mean: 462.19637869182463 nsec\nrounds: 196890"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1128405.473683988,
            "unit": "iter/sec",
            "range": "stddev: 2.6097277340525337e-7",
            "extra": "mean: 886.2062647881588 nsec\nrounds: 171498"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29133.678312141474,
            "unit": "iter/sec",
            "range": "stddev: 0.000002057594267063789",
            "extra": "mean: 34.32453634195753 usec\nrounds: 18037"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2429364.8894142383,
            "unit": "iter/sec",
            "range": "stddev: 4.1813447887402047e-8",
            "extra": "mean: 411.6302183987654 nsec\nrounds: 104625"
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
          "id": "11a766d98c80f8fda0c84e1e2947aa7f6b2323f1",
          "message": "refactor: group `_log_retry_attempt` and `_log_all_failed` params into `RetryConfig` (#137)\n\nThis commit refactors `_log_retry_attempt` and `_log_all_failed` in\n`src/taipanstack/utils/retry.py` to accept the `RetryConfig` dataclass\nrather than passing multiple configuration variables individually,\nwhich resolves the \"Too Many Parameters\" code health issue.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-05T20:43:40Z",
          "tree_id": "46d9b2c703cbe6623dbeddbd8a8b466e8db792fc",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/11a766d98c80f8fda0c84e1e2947aa7f6b2323f1"
        },
        "date": 1772743490627,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 222625.02192509721,
            "unit": "iter/sec",
            "range": "stddev: 8.642215820105149e-7",
            "extra": "mean: 4.491858064078945 usec\nrounds: 155"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 159944.20339477604,
            "unit": "iter/sec",
            "range": "stddev: 8.372654297219245e-7",
            "extra": "mean: 6.2521803152302375 usec\nrounds: 66173"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 56902.745284458215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015901641174402951",
            "extra": "mean: 17.573844548289816 usec\nrounds: 22663"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 166354.61178338743,
            "unit": "iter/sec",
            "range": "stddev: 9.258011728333386e-7",
            "extra": "mean: 6.011255048955982 usec\nrounds: 10943"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 115746.62796435537,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010912489190216067",
            "extra": "mean: 8.639560543465283 usec\nrounds: 43283"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 20335.95114151288,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031407454601808182",
            "extra": "mean: 49.173996979105915 usec\nrounds: 10925"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 35310.03688598335,
            "unit": "iter/sec",
            "range": "stddev: 0.000015707706413348004",
            "extra": "mean: 28.320559483667928 usec\nrounds: 17509"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4442050.275869982,
            "unit": "iter/sec",
            "range": "stddev: 3.922417257465686e-8",
            "extra": "mean: 225.1212701108328 nsec\nrounds: 143885"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 540674.1317109241,
            "unit": "iter/sec",
            "range": "stddev: 2.9333852516123865e-7",
            "extra": "mean: 1.849542897189388 usec\nrounds: 175501"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1134715.5798209072,
            "unit": "iter/sec",
            "range": "stddev: 4.0213597610186126e-7",
            "extra": "mean: 881.2781086145222 nsec\nrounds: 9072"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 604040.3337622716,
            "unit": "iter/sec",
            "range": "stddev: 4.570951131335647e-7",
            "extra": "mean: 1.6555185872630218 usec\nrounds: 127211"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2354900.9489594367,
            "unit": "iter/sec",
            "range": "stddev: 2.1079431062422754e-7",
            "extra": "mean: 424.64631068320364 nsec\nrounds: 198926"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1156296.2330829513,
            "unit": "iter/sec",
            "range": "stddev: 3.0396125747728966e-7",
            "extra": "mean: 864.8302843067908 nsec\nrounds: 140647"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 33171.29041924445,
            "unit": "iter/sec",
            "range": "stddev: 0.000002127538784719166",
            "extra": "mean: 30.146551049453482 usec\nrounds: 19060"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2743702.008821247,
            "unit": "iter/sec",
            "range": "stddev: 4.7784370628736415e-8",
            "extra": "mean: 364.47106747923374 nsec\nrounds: 77107"
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
          "id": "f1ae7e3ffeb4192f2d985e2441a806634b7e772e",
          "message": "🧪 [testing improvement] Add comprehensive tests for validate_project_dir (#136)\n\nAdded unit tests for the `validate_project_dir` validator in `StackConfig`.\nCoverage includes:\n- Absolute path handling\n- Paths with dots (non-traversal)\n- Non-existent path resolution\n- Direct classmethod invocation\n- Documentation of current \"..\" string check behavior\n- Traversal attack rejection (direct call)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-05T20:43:44Z",
          "tree_id": "9ba7d7b90215a4e74fc7fdb287664969d4ce3548",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/f1ae7e3ffeb4192f2d985e2441a806634b7e772e"
        },
        "date": 1772743504603,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 183433.6137633361,
            "unit": "iter/sec",
            "range": "stddev: 0.00000250161856349537",
            "extra": "mean: 5.451563535624328 usec\nrounds: 181"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154445.62612544445,
            "unit": "iter/sec",
            "range": "stddev: 8.766982691103636e-7",
            "extra": "mean: 6.47477060430171 usec\nrounds: 48667"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54411.70536206415,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016497344781873533",
            "extra": "mean: 18.378398422652637 usec\nrounds: 24725"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 165317.59270636184,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011361447108469552",
            "extra": "mean: 6.048962990745978 usec\nrounds: 9349"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109859.8634504819,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012375954645478153",
            "extra": "mean: 9.102505397257652 usec\nrounds: 40113"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19382.41948383691,
            "unit": "iter/sec",
            "range": "stddev: 0.000004301035567552621",
            "extra": "mean: 51.59314608962542 usec\nrounds: 7071"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33927.72196040079,
            "unit": "iter/sec",
            "range": "stddev: 0.000015559412378141534",
            "extra": "mean: 29.474422160354997 usec\nrounds: 15442"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4404771.00960019,
            "unit": "iter/sec",
            "range": "stddev: 3.302973586920779e-8",
            "extra": "mean: 227.02655775310055 nsec\nrounds: 154036"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 589551.9722376628,
            "unit": "iter/sec",
            "range": "stddev: 2.590010583202853e-7",
            "extra": "mean: 1.6962032985903708 usec\nrounds: 182482"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1052320.1527769158,
            "unit": "iter/sec",
            "range": "stddev: 5.381498456394317e-7",
            "extra": "mean: 950.2811452970366 nsec\nrounds: 9255"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 611875.1252798069,
            "unit": "iter/sec",
            "range": "stddev: 4.422859145508362e-7",
            "extra": "mean: 1.6343204008215007 usec\nrounds: 143205"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2922276.8433524016,
            "unit": "iter/sec",
            "range": "stddev: 4.18594706112116e-8",
            "extra": "mean: 342.1989269340579 nsec\nrounds: 108614"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1142008.7044537028,
            "unit": "iter/sec",
            "range": "stddev: 2.8024876940514647e-7",
            "extra": "mean: 875.6500682526454 nsec\nrounds: 131840"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29912.728488609075,
            "unit": "iter/sec",
            "range": "stddev: 0.000002163366509885017",
            "extra": "mean: 33.43058458812292 usec\nrounds: 16935"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2482001.26581668,
            "unit": "iter/sec",
            "range": "stddev: 4.6082559107357156e-8",
            "extra": "mean: 402.90068090299826 nsec\nrounds: 105742"
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
          "id": "40d08c7fbc42f5fb9cc425ff7e84b1b81b696e0f",
          "message": "🧪 [Testing] Add tests for async_wrapper in retry.py (#135)\n\n* test: add test suite for async_wrapper in retry decorator\n\nAdded `TestAsyncRetryDecorator` to `tests/test_utils_retry.py` to cover the `async_wrapper` function in `src/taipanstack/utils/retry.py`.\n\nThe new tests verify:\n- Happy path execution without retry\n- Proper retry behavior on failure\n- Exception raising when maximum attempts are exceeded\n- Ensuring only specified exceptions trigger a retry\n- Preservation of the last exception in RetryError\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n* test: fix code formatting error in CI for retry wrapper\n\nRan `ruff format` to resolve the formatting violations on `tests/test_utils_retry.py` which were causing the code quality check in GitHub Actions to fail.\n\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>\n\n---------\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-05T20:43:48Z",
          "tree_id": "a4262654f3eb2db1a77b25d9c61b82d3a0a09062",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/40d08c7fbc42f5fb9cc425ff7e84b1b81b696e0f"
        },
        "date": 1772743509581,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 223400.59563960557,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016074365676767872",
            "extra": "mean: 4.476263803760043 usec\nrounds: 163"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 167167.66565286551,
            "unit": "iter/sec",
            "range": "stddev: 6.399404988582259e-7",
            "extra": "mean: 5.982018090008895 usec\nrounds: 59425"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 58288.699006773466,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012881749797507075",
            "extra": "mean: 17.155984213746038 usec\nrounds: 29646"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 176256.0627815432,
            "unit": "iter/sec",
            "range": "stddev: 5.925102802711362e-7",
            "extra": "mean: 5.6735637016891065 usec\nrounds: 11962"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 122497.3846003565,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011542295154628007",
            "extra": "mean: 8.163439597200101 usec\nrounds: 27507"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 22468.37712621241,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022499889582551374",
            "extra": "mean: 44.50699729591793 usec\nrounds: 11464"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 39226.484502250154,
            "unit": "iter/sec",
            "range": "stddev: 0.000014961588943154297",
            "extra": "mean: 25.492980385296494 usec\nrounds: 17181"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4612050.039746673,
            "unit": "iter/sec",
            "range": "stddev: 2.5816684426314565e-8",
            "extra": "mean: 216.823319647919 nsec\nrounds: 154179"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 615173.9024228439,
            "unit": "iter/sec",
            "range": "stddev: 3.136562018323213e-7",
            "extra": "mean: 1.625556604500846 usec\nrounds: 190986"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1281154.162018528,
            "unit": "iter/sec",
            "range": "stddev: 3.0486067405457846e-7",
            "extra": "mean: 780.5461900263788 nsec\nrounds: 10630"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 625133.6131455393,
            "unit": "iter/sec",
            "range": "stddev: 5.74167129669138e-7",
            "extra": "mean: 1.5996580234555182 usec\nrounds: 123488"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2999927.1678827195,
            "unit": "iter/sec",
            "range": "stddev: 4.6876082586603855e-8",
            "extra": "mean: 333.3414259872682 nsec\nrounds: 114917"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1161090.5943938105,
            "unit": "iter/sec",
            "range": "stddev: 1.7381407702262193e-7",
            "extra": "mean: 861.2592375034149 nsec\nrounds: 161813"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 32224.650966759415,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020450452497146815",
            "extra": "mean: 31.032143716049134 usec\nrounds: 16964"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2640333.0452945167,
            "unit": "iter/sec",
            "range": "stddev: 2.8492578652619477e-8",
            "extra": "mean: 378.7400993909303 nsec\nrounds: 70329"
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
          "id": "38df447172ffb5b1ada0df270538376c5abc0903",
          "message": "test(circuit_breaker): add tests for async_wrapper (#132)\n\nAdd `test_decorator_async_success` and `test_decorator_async_failure_opens_circuit` to `tests/test_utils_circuit_breaker.py` to cover `async_wrapper` missing lines.\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-05T20:43:53Z",
          "tree_id": "5918de635a29708d8749d7075bca45543ad46d52",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/38df447172ffb5b1ada0df270538376c5abc0903"
        },
        "date": 1772743546228,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 168462.99153944768,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026447300244767236",
            "extra": "mean: 5.936021857749319 usec\nrounds: 183"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155762.68487929326,
            "unit": "iter/sec",
            "range": "stddev: 8.145022874778296e-7",
            "extra": "mean: 6.420022875022601 usec\nrounds: 69508"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53694.97595422043,
            "unit": "iter/sec",
            "range": "stddev: 0.000001444815449197993",
            "extra": "mean: 18.62371632036088 usec\nrounds: 26329"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 166662.8490632896,
            "unit": "iter/sec",
            "range": "stddev: 9.895153300642095e-7",
            "extra": "mean: 6.000137436869651 usec\nrounds: 12071"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109137.46878578827,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011582218684453709",
            "extra": "mean: 9.162756028021594 usec\nrounds: 43173"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19362.174032189134,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036288375102937724",
            "extra": "mean: 51.64709284905325 usec\nrounds: 10684"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33188.61531227245,
            "unit": "iter/sec",
            "range": "stddev: 0.000015312891646682685",
            "extra": "mean: 30.13081415391925 usec\nrounds: 14851"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4496051.332562672,
            "unit": "iter/sec",
            "range": "stddev: 2.8239924844338223e-8",
            "extra": "mean: 222.41738940067427 nsec\nrounds: 164447"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 587726.6522436746,
            "unit": "iter/sec",
            "range": "stddev: 2.631814042396048e-7",
            "extra": "mean: 1.7014712471902658 usec\nrounds: 186602"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1091202.087198435,
            "unit": "iter/sec",
            "range": "stddev: 4.09134450353168e-7",
            "extra": "mean: 916.4205345019194 nsec\nrounds: 10665"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 619541.4694375854,
            "unit": "iter/sec",
            "range": "stddev: 3.7646771377520164e-7",
            "extra": "mean: 1.6140969561049587 usec\nrounds: 166890"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2926560.9686144455,
            "unit": "iter/sec",
            "range": "stddev: 4.1638005049461493e-8",
            "extra": "mean: 341.69798979907677 nsec\nrounds: 110412"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1128044.0851532863,
            "unit": "iter/sec",
            "range": "stddev: 2.877163936062873e-7",
            "extra": "mean: 886.4901763694043 nsec\nrounds: 167758"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29368.95861554275,
            "unit": "iter/sec",
            "range": "stddev: 0.000002147743475364527",
            "extra": "mean: 34.0495559645338 usec\nrounds: 21192"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2454664.465420501,
            "unit": "iter/sec",
            "range": "stddev: 6.106857195598814e-8",
            "extra": "mean: 407.38765484538465 nsec\nrounds: 103328"
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
          "id": "1ca6263417c5b93e7186415ace8f77ad4eab2492",
          "message": "Add test for `async_wrapper` missing base Exception catch in `taipanstack/core/result.py` (#134)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-05T20:45:57Z",
          "tree_id": "89d840ba78342501f96e510d082c31deeb549c3e",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/1ca6263417c5b93e7186415ace8f77ad4eab2492"
        },
        "date": 1772743667251,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 189630.9781182774,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013194343446666646",
            "extra": "mean: 5.27339999995294 usec\nrounds: 220"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 156658.97750399628,
            "unit": "iter/sec",
            "range": "stddev: 8.581837727082163e-7",
            "extra": "mean: 6.383292013855322 usec\nrounds: 59165"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54317.81292089492,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015616151964548726",
            "extra": "mean: 18.410166872078186 usec\nrounds: 26775"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163757.26161172483,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010908418364898876",
            "extra": "mean: 6.106599427456481 usec\nrounds: 10480"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109189.65349444933,
            "unit": "iter/sec",
            "range": "stddev: 0.000001242288973532951",
            "extra": "mean: 9.158376897412127 usec\nrounds: 41043"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 16912.573782827658,
            "unit": "iter/sec",
            "range": "stddev: 0.00001911148974349218",
            "extra": "mean: 59.12760605457695 usec\nrounds: 10042"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33926.24686746281,
            "unit": "iter/sec",
            "range": "stddev: 0.000014677075533104707",
            "extra": "mean: 29.475703690615322 usec\nrounds: 17016"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4505782.914506766,
            "unit": "iter/sec",
            "range": "stddev: 3.373334446883271e-8",
            "extra": "mean: 221.93701271736805 nsec\nrounds: 154274"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 586469.327002173,
            "unit": "iter/sec",
            "range": "stddev: 2.967936873023603e-7",
            "extra": "mean: 1.7051190129782534 usec\nrounds: 188324"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1097028.0608627773,
            "unit": "iter/sec",
            "range": "stddev: 3.781278509170287e-7",
            "extra": "mean: 911.5537110450321 nsec\nrounds: 10361"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 612576.5661970703,
            "unit": "iter/sec",
            "range": "stddev: 4.012386730784626e-7",
            "extra": "mean: 1.6324489952465677 usec\nrounds: 148545"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2916307.015248125,
            "unit": "iter/sec",
            "range": "stddev: 4.1618341288798407e-8",
            "extra": "mean: 342.89942546220846 nsec\nrounds: 108261"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1142056.3603125117,
            "unit": "iter/sec",
            "range": "stddev: 2.8912838478001455e-7",
            "extra": "mean: 875.613529026151 nsec\nrounds: 173612"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29001.94334495643,
            "unit": "iter/sec",
            "range": "stddev: 0.000006484912664818558",
            "extra": "mean: 34.48044802052565 usec\nrounds: 17555"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2519542.5594097185,
            "unit": "iter/sec",
            "range": "stddev: 4.900507197398944e-8",
            "extra": "mean: 396.89744325440074 nsec\nrounds: 105955"
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
          "id": "97a4d18b54f908835a9ca385b60a6671cdfecc8c",
          "message": "fix(qa): resolve leftover merge artifacts in test_result_module",
          "timestamp": "2026-03-05T17:50:42-03:00",
          "tree_id": "48b64b490aea9979b725822844175664efc124eb",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/97a4d18b54f908835a9ca385b60a6671cdfecc8c"
        },
        "date": 1772743922561,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 209891.89471220275,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021294243273663",
            "extra": "mean: 4.764357391557063 usec\nrounds: 2009"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 144693.64010904692,
            "unit": "iter/sec",
            "range": "stddev: 0.000002084816096511172",
            "extra": "mean: 6.911153795331709 usec\nrounds: 49956"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53834.4060566186,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015183116716514624",
            "extra": "mean: 18.575481244248934 usec\nrounds: 24979"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164597.88730031537,
            "unit": "iter/sec",
            "range": "stddev: 9.075830125528243e-7",
            "extra": "mean: 6.075412123458549 usec\nrounds: 10987"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110397.16906384059,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012836845391782556",
            "extra": "mean: 9.058203289811889 usec\nrounds: 43893"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19531.248404696147,
            "unit": "iter/sec",
            "range": "stddev: 0.000003811610585572047",
            "extra": "mean: 51.20000418199367 usec\nrounds: 9804"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33600.35528977327,
            "unit": "iter/sec",
            "range": "stddev: 0.000015687813791888373",
            "extra": "mean: 29.76159005986355 usec\nrounds: 16861"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4306542.551914442,
            "unit": "iter/sec",
            "range": "stddev: 4.954152866539201e-8",
            "extra": "mean: 232.20483437593427 nsec\nrounds: 195351"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 544687.770573718,
            "unit": "iter/sec",
            "range": "stddev: 6.41391515294184e-7",
            "extra": "mean: 1.8359141769360832 usec\nrounds: 185529"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1072422.6918633012,
            "unit": "iter/sec",
            "range": "stddev: 4.692559026761605e-7",
            "extra": "mean: 932.468146736555 nsec\nrounds: 10360"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 618123.8681376631,
            "unit": "iter/sec",
            "range": "stddev: 3.8496978056754096e-7",
            "extra": "mean: 1.6177987156731 usec\nrounds: 162576"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2174459.0555708846,
            "unit": "iter/sec",
            "range": "stddev: 3.7900646054984734e-7",
            "extra": "mean: 459.8844928526185 nsec\nrounds: 126503"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1133909.4841305378,
            "unit": "iter/sec",
            "range": "stddev: 3.0500291346619674e-7",
            "extra": "mean: 881.9046087852264 nsec\nrounds: 169177"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29935.771860679866,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022181547281561597",
            "extra": "mean: 33.404851047568386 usec\nrounds: 17039"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2519401.551472559,
            "unit": "iter/sec",
            "range": "stddev: 4.288264501665874e-8",
            "extra": "mean: 396.9196571368463 nsec\nrounds: 104298"
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
          "id": "c4c1ab8379def38c7b26103e1055cb3a6d2ae3dd",
          "message": "chore: bump version to v0.3.6 (qa & security sprint)",
          "timestamp": "2026-03-05T17:55:18-03:00",
          "tree_id": "762d22231a0ec069bdf8be15329d16d60d452f19",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/c4c1ab8379def38c7b26103e1055cb3a6d2ae3dd"
        },
        "date": 1772744159308,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 197283.58151932564,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012001292894730347",
            "extra": "mean: 5.068845528344391 usec\nrounds: 123"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 156049.5213913616,
            "unit": "iter/sec",
            "range": "stddev: 8.096980322971022e-7",
            "extra": "mean: 6.408222153351357 usec\nrounds: 61309"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53769.30066560721,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015361228191919773",
            "extra": "mean: 18.59797296265815 usec\nrounds: 31438"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 165720.57059472232,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010535093474178266",
            "extra": "mean: 6.034253903491248 usec\nrounds: 11272"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 98652.69392482907,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029747575302327403",
            "extra": "mean: 10.136570631938094 usec\nrounds: 40527"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 17300.123711404358,
            "unit": "iter/sec",
            "range": "stddev: 0.000017441861630411352",
            "extra": "mean: 57.8030548614397 usec\nrounds: 10645"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33543.08884632408,
            "unit": "iter/sec",
            "range": "stddev: 0.000015840521934905947",
            "extra": "mean: 29.812400538944047 usec\nrounds: 16700"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4417924.769010385,
            "unit": "iter/sec",
            "range": "stddev: 2.874505227380102e-8",
            "extra": "mean: 226.35061760540208 nsec\nrounds: 198413"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 564449.6446020977,
            "unit": "iter/sec",
            "range": "stddev: 4.844292641590883e-7",
            "extra": "mean: 1.7716372214299796 usec\nrounds: 117427"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1076121.4388533854,
            "unit": "iter/sec",
            "range": "stddev: 3.546480941939706e-7",
            "extra": "mean: 929.263151810735 nsec\nrounds: 8573"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 620665.5202916204,
            "unit": "iter/sec",
            "range": "stddev: 3.6901384600612105e-7",
            "extra": "mean: 1.611173759950688 usec\nrounds: 158178"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2960406.1814543456,
            "unit": "iter/sec",
            "range": "stddev: 3.8009526382076414e-8",
            "extra": "mean: 337.79148492011285 nsec\nrounds: 108484"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1113338.4908588717,
            "unit": "iter/sec",
            "range": "stddev: 2.892996907308927e-7",
            "extra": "mean: 898.1994318983454 nsec\nrounds: 155958"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29236.364332782665,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030493607369810364",
            "extra": "mean: 34.20397928475335 usec\nrounds: 15882"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2511030.4092553235,
            "unit": "iter/sec",
            "range": "stddev: 4.424523123707529e-8",
            "extra": "mean: 398.2428871885535 nsec\nrounds: 76313"
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
          "id": "bc833e79be8b2920f14ad707d23c7286fc9a067d",
          "message": "style: run ruff format to fix CI",
          "timestamp": "2026-03-05T17:59:13-03:00",
          "tree_id": "02ee7b631003550f750a6a20938005d6d7f12e84",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/bc833e79be8b2920f14ad707d23c7286fc9a067d"
        },
        "date": 1772744389217,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 179870.08908817917,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015485973484038115",
            "extra": "mean: 5.559568047524354 usec\nrounds: 169"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154751.6363827006,
            "unit": "iter/sec",
            "range": "stddev: 8.882443892633126e-7",
            "extra": "mean: 6.461967210007403 usec\nrounds: 63739"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 47877.72043878768,
            "unit": "iter/sec",
            "range": "stddev: 0.000005222071343448729",
            "extra": "mean: 20.886541607145094 usec\nrounds: 30788"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163156.31850518245,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012463737297657887",
            "extra": "mean: 6.129091469836249 usec\nrounds: 10375"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108413.51568771533,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011759959037438526",
            "extra": "mean: 9.223942177841513 usec\nrounds: 41178"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19485.562629359367,
            "unit": "iter/sec",
            "range": "stddev: 0.000006164619979286931",
            "extra": "mean: 51.32004751524474 usec\nrounds: 6882"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34072.350621302394,
            "unit": "iter/sec",
            "range": "stddev: 0.000015488105715833905",
            "extra": "mean: 29.349310563116518 usec\nrounds: 16425"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4024871.7409462724,
            "unit": "iter/sec",
            "range": "stddev: 1.1746024692861343e-7",
            "extra": "mean: 248.45512214133197 nsec\nrounds: 88176"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590149.4722552,
            "unit": "iter/sec",
            "range": "stddev: 2.4822526858157434e-7",
            "extra": "mean: 1.6944859684082916 usec\nrounds: 181127"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1057578.7392286847,
            "unit": "iter/sec",
            "range": "stddev: 4.2200963327428324e-7",
            "extra": "mean: 945.5560734223172 nsec\nrounds: 10085"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 592626.5666210064,
            "unit": "iter/sec",
            "range": "stddev: 4.251795657418646e-7",
            "extra": "mean: 1.687403259191914 usec\nrounds: 142980"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2917844.782663431,
            "unit": "iter/sec",
            "range": "stddev: 4.400222905637043e-8",
            "extra": "mean: 342.71871003614126 nsec\nrounds: 35497"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1128996.6584970693,
            "unit": "iter/sec",
            "range": "stddev: 2.9660867523907607e-7",
            "extra": "mean: 885.7422140922979 nsec\nrounds: 124456"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29753.216300671746,
            "unit": "iter/sec",
            "range": "stddev: 0.000002245754436571775",
            "extra": "mean: 33.60981178957189 usec\nrounds: 18474"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2492522.369169894,
            "unit": "iter/sec",
            "range": "stddev: 4.412500302466805e-8",
            "extra": "mean: 401.2000102261896 nsec\nrounds: 34231"
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
          "id": "7a735c602aaf7d6dda4aa10c5267e1528a3e9bd0",
          "message": "docs: fix missing v0.3.6 release notes formatting in changelog",
          "timestamp": "2026-03-05T18:05:24-03:00",
          "tree_id": "042878f382f1fe97c2045be51a4f038fbedeaea2",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/7a735c602aaf7d6dda4aa10c5267e1528a3e9bd0"
        },
        "date": 1772744767133,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 191137.3157401579,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016924624359702386",
            "extra": "mean: 5.231840763942988 usec\nrounds: 157"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 149194.4302274755,
            "unit": "iter/sec",
            "range": "stddev: 0.000001292904463912404",
            "extra": "mean: 6.702663085178906 usec\nrounds: 67756"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52716.053790627055,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031709777827719527",
            "extra": "mean: 18.96955344896853 usec\nrounds: 31647"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164287.68972802898,
            "unit": "iter/sec",
            "range": "stddev: 9.955270649030332e-7",
            "extra": "mean: 6.086883330427592 usec\nrounds: 11374"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109093.91999396082,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011651019056117089",
            "extra": "mean: 9.166413674156706 usec\nrounds: 43191"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19600.233007344323,
            "unit": "iter/sec",
            "range": "stddev: 0.000003507736908435216",
            "extra": "mean: 51.01980163324049 usec\nrounds: 9674"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33470.47621555246,
            "unit": "iter/sec",
            "range": "stddev: 0.000015192803048316653",
            "extra": "mean: 29.877077145838097 usec\nrounds: 17266"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4415323.748966204,
            "unit": "iter/sec",
            "range": "stddev: 2.9917859183186666e-8",
            "extra": "mean: 226.48395833581063 nsec\nrounds: 150106"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 591264.7991843936,
            "unit": "iter/sec",
            "range": "stddev: 2.2824734372196111e-7",
            "extra": "mean: 1.6912895903483451 usec\nrounds: 189036"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1050573.3258102997,
            "unit": "iter/sec",
            "range": "stddev: 4.62237995244324e-7",
            "extra": "mean: 951.8612127608582 nsec\nrounds: 10109"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 624117.9277877727,
            "unit": "iter/sec",
            "range": "stddev: 3.6345638840227307e-7",
            "extra": "mean: 1.6022612962658613 usec\nrounds: 156202"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2969968.805746217,
            "unit": "iter/sec",
            "range": "stddev: 4.8814628525101034e-8",
            "extra": "mean: 336.70387313993746 nsec\nrounds: 110169"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1131051.2643286088,
            "unit": "iter/sec",
            "range": "stddev: 2.6000955449181717e-7",
            "extra": "mean: 884.133223257214 nsec\nrounds: 137476"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29793.106113285707,
            "unit": "iter/sec",
            "range": "stddev: 0.00000210947533428224",
            "extra": "mean: 33.564811812423535 usec\nrounds: 17998"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2495857.339356079,
            "unit": "iter/sec",
            "range": "stddev: 4.373525516977478e-8",
            "extra": "mean: 400.663925870908 nsec\nrounds: 102902"
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
          "id": "1036ebf5c0048e744afee924c9d2df7623153636",
          "message": "Merge pull request #147 from gabrielima7/jules/test-guards-normalize-ext-6133573466907181237\n\n🧪 Add test coverage for normalize_ext in guards.py",
          "timestamp": "2026-03-06T14:15:59Z",
          "tree_id": "1e66a88eb91ef759022d6ece733402fc1fe5bf0e",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/1036ebf5c0048e744afee924c9d2df7623153636"
        },
        "date": 1772806600694,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 172951.80900362393,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025397555311581702",
            "extra": "mean: 5.781957446765108 usec\nrounds: 188"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154570.2717690458,
            "unit": "iter/sec",
            "range": "stddev: 8.275878118782141e-7",
            "extra": "mean: 6.469549341895249 usec\nrounds: 61388"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54224.912857549316,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014464991486277907",
            "extra": "mean: 18.44170782951803 usec\nrounds: 32748"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163791.56925750463,
            "unit": "iter/sec",
            "range": "stddev: 9.14361818507312e-7",
            "extra": "mean: 6.105320344222674 usec\nrounds: 8366"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109462.0561767582,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012742066278684828",
            "extra": "mean: 9.135585744755337 usec\nrounds: 41711"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19088.956942326906,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036634071949631815",
            "extra": "mean: 52.38630916405127 usec\nrounds: 10192"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 29840.249119521646,
            "unit": "iter/sec",
            "range": "stddev: 0.000018475284834157534",
            "extra": "mean: 33.511784569713754 usec\nrounds: 16850"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4199091.205548463,
            "unit": "iter/sec",
            "range": "stddev: 7.944672231158997e-8",
            "extra": "mean: 238.1467682052249 nsec\nrounds: 89687"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 588091.0847624402,
            "unit": "iter/sec",
            "range": "stddev: 3.4305985639326073e-7",
            "extra": "mean: 1.7004168672339273 usec\nrounds: 182816"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1092050.242459244,
            "unit": "iter/sec",
            "range": "stddev: 3.711154533360478e-7",
            "extra": "mean: 915.7087843761186 nsec\nrounds: 10439"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 596825.7710817322,
            "unit": "iter/sec",
            "range": "stddev: 3.640534683429848e-7",
            "extra": "mean: 1.675530864204346 usec\nrounds: 151470"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2948684.781754036,
            "unit": "iter/sec",
            "range": "stddev: 4.5149547911216606e-8",
            "extra": "mean: 339.1342493398081 nsec\nrounds: 114719"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1137837.5105430128,
            "unit": "iter/sec",
            "range": "stddev: 2.749343757124692e-7",
            "extra": "mean: 878.8601102830296 nsec\nrounds: 175717"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30464.539078098645,
            "unit": "iter/sec",
            "range": "stddev: 0.000003216638379758585",
            "extra": "mean: 32.82504939386767 usec\nrounds: 18808"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2518510.8595221285,
            "unit": "iter/sec",
            "range": "stddev: 4.4007261238805334e-8",
            "extra": "mean: 397.0600310177553 nsec\nrounds: 105742"
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
          "id": "6f1c90fe489be59f592637b3668a8631c065b4a7",
          "message": "Merge pull request #146 from gabrielima7/fix-check-command-exists-edge-cases-8495354416869461807\n\n🧪 [testing improvement] fix edge cases in check_command_exists",
          "timestamp": "2026-03-06T14:16:01Z",
          "tree_id": "9db68bc787c18e5ef6cc7dc51881bf356e59334a",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/6f1c90fe489be59f592637b3668a8631c065b4a7"
        },
        "date": 1772806609358,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 180123.692518312,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026471654121659966",
            "extra": "mean: 5.551740506864951 usec\nrounds: 158"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155314.12659393687,
            "unit": "iter/sec",
            "range": "stddev: 8.305225350065753e-7",
            "extra": "mean: 6.438564359406042 usec\nrounds: 62384"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54043.65090530661,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016590304458573756",
            "extra": "mean: 18.503561163034025 usec\nrounds: 25424"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 159402.92722393264,
            "unit": "iter/sec",
            "range": "stddev: 8.891135431598935e-7",
            "extra": "mean: 6.2734105164529295 usec\nrounds: 11354"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110527.28451073328,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014835994369716945",
            "extra": "mean: 9.047539749362883 usec\nrounds: 32013"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19372.273791008178,
            "unit": "iter/sec",
            "range": "stddev: 0.000004537357259358096",
            "extra": "mean: 51.62016657353663 usec\nrounds: 10740"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33368.15199888696,
            "unit": "iter/sec",
            "range": "stddev: 0.000014462048710046498",
            "extra": "mean: 29.968695900011376 usec\nrounds: 17366"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4487773.116617058,
            "unit": "iter/sec",
            "range": "stddev: 2.8469034534201094e-8",
            "extra": "mean: 222.82766396925533 nsec\nrounds: 196464"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590388.926998284,
            "unit": "iter/sec",
            "range": "stddev: 2.932163292175628e-7",
            "extra": "mean: 1.6937987050067367 usec\nrounds: 185840"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1044546.3247927644,
            "unit": "iter/sec",
            "range": "stddev: 4.6185723122577255e-7",
            "extra": "mean: 957.3534234572103 nsec\nrounds: 10121"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 612401.2985991908,
            "unit": "iter/sec",
            "range": "stddev: 3.893476960884329e-7",
            "extra": "mean: 1.632916197740606 usec\nrounds: 155473"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2866634.45465905,
            "unit": "iter/sec",
            "range": "stddev: 1.1775968219156581e-7",
            "extra": "mean: 348.8411291417879 nsec\nrounds: 112537"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1142828.7811912412,
            "unit": "iter/sec",
            "range": "stddev: 2.5356772908158455e-7",
            "extra": "mean: 875.0217149393437 nsec\nrounds: 177620"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29395.08831297144,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021320025612329556",
            "extra": "mean: 34.01928884693029 usec\nrounds: 18515"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2468373.6769876108,
            "unit": "iter/sec",
            "range": "stddev: 6.202339138837015e-8",
            "extra": "mean: 405.12504622897563 nsec\nrounds: 78413"
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
          "id": "c60194c352b3ef2187af237b23b7e3e24f01d518",
          "message": "Merge pull request #145 from gabrielima7/optimize-guard-path-traversal-lowercasing-16828600138685644971\n\n⚡ Optimize redundant string lowercasing inside guard_path_traversal",
          "timestamp": "2026-03-06T14:16:05Z",
          "tree_id": "dadc9a52161661199d174da2332c1c9664d3d687",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/c60194c352b3ef2187af237b23b7e3e24f01d518"
        },
        "date": 1772806638851,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 177743.19795882542,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015202735205768165",
            "extra": "mean: 5.626094339945723 usec\nrounds: 159"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155450.91264423763,
            "unit": "iter/sec",
            "range": "stddev: 9.10646958700293e-7",
            "extra": "mean: 6.432898868137129 usec\nrounds: 67852"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54368.25846292472,
            "unit": "iter/sec",
            "range": "stddev: 0.000001626284824152249",
            "extra": "mean: 18.393085014520537 usec\nrounds: 18291"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 160333.0577760632,
            "unit": "iter/sec",
            "range": "stddev: 0.000001316549096854875",
            "extra": "mean: 6.237016956270476 usec\nrounds: 11913"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 106619.85143540899,
            "unit": "iter/sec",
            "range": "stddev: 0.000001283383437574832",
            "extra": "mean: 9.379116426604726 usec\nrounds: 41451"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 18894.49199393921,
            "unit": "iter/sec",
            "range": "stddev: 0.000003966317183822368",
            "extra": "mean: 52.92547692315677 usec\nrounds: 10465"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 32623.053854473535,
            "unit": "iter/sec",
            "range": "stddev: 0.000017230738023512034",
            "extra": "mean: 30.653169518121985 usec\nrounds: 12099"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4442828.241813663,
            "unit": "iter/sec",
            "range": "stddev: 3.6500772246510765e-8",
            "extra": "mean: 225.0818500225131 nsec\nrounds: 154036"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 589225.1709279672,
            "unit": "iter/sec",
            "range": "stddev: 2.6832344508756236e-7",
            "extra": "mean: 1.697144061963791 usec\nrounds: 189754"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1058216.2624874546,
            "unit": "iter/sec",
            "range": "stddev: 4.5543547969534895e-7",
            "extra": "mean: 944.9864223872247 nsec\nrounds: 10753"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 568068.501714772,
            "unit": "iter/sec",
            "range": "stddev: 5.796599888568835e-7",
            "extra": "mean: 1.7603510791064796 usec\nrounds: 152393"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2917971.0329095256,
            "unit": "iter/sec",
            "range": "stddev: 4.161253591162447e-8",
            "extra": "mean: 342.7038818143017 nsec\nrounds: 110657"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1139705.295617995,
            "unit": "iter/sec",
            "range": "stddev: 2.645386711573463e-7",
            "extra": "mean: 877.4198065454798 nsec\nrounds: 176679"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29702.83415624914,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021311034001954315",
            "extra": "mean: 33.66682097538531 usec\nrounds: 23170"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2482753.819914116,
            "unit": "iter/sec",
            "range": "stddev: 5.1767677917440057e-8",
            "extra": "mean: 402.77855660879004 nsec\nrounds: 105065"
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
          "id": "21abf67ef4afbfab52186557e489b71a5a66e98c",
          "message": "Merge pull request #143 from gabrielima7/perf-decorator-signature-11545019226676940765\n\n⚡ Cache `inspect.signature` in decorators to improve performance",
          "timestamp": "2026-03-06T14:16:08Z",
          "tree_id": "9965bf405bf259958c8f79686e33eac865e1824b",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/21abf67ef4afbfab52186557e489b71a5a66e98c"
        },
        "date": 1772806650582,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 217688.89510343104,
            "unit": "iter/sec",
            "range": "stddev: 8.916160807873123e-7",
            "extra": "mean: 4.593711587928578 usec\nrounds: 1959"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 152824.41620998667,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011619695323144973",
            "extra": "mean: 6.543457026041972 usec\nrounds: 62224"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53658.16732906169,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022568398604608464",
            "extra": "mean: 18.636491885148526 usec\nrounds: 24892"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 162884.82439423064,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011039289495332113",
            "extra": "mean: 6.139307352412995 usec\nrounds: 11098"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108451.56228056554,
            "unit": "iter/sec",
            "range": "stddev: 0.000001586302176402893",
            "extra": "mean: 9.220706267125848 usec\nrounds: 42205"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19568.796294116648,
            "unit": "iter/sec",
            "range": "stddev: 0.000003947815775915762",
            "extra": "mean: 51.101763489696594 usec\nrounds: 10545"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 32606.58867377075,
            "unit": "iter/sec",
            "range": "stddev: 0.000016701091797999234",
            "extra": "mean: 30.668648290841162 usec\nrounds: 16471"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4466368.429431728,
            "unit": "iter/sec",
            "range": "stddev: 3.2461602315532044e-8",
            "extra": "mean: 223.8955464153713 nsec\nrounds: 146994"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 563383.0305709002,
            "unit": "iter/sec",
            "range": "stddev: 5.242888683541629e-7",
            "extra": "mean: 1.7749913393498153 usec\nrounds: 163613"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 880615.3465638196,
            "unit": "iter/sec",
            "range": "stddev: 8.382813988492797e-7",
            "extra": "mean: 1.1355695808641333 usec\nrounds: 7653"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 584627.2580093017,
            "unit": "iter/sec",
            "range": "stddev: 5.759287727973935e-7",
            "extra": "mean: 1.7104915761284765 usec\nrounds: 107910"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2176926.619711581,
            "unit": "iter/sec",
            "range": "stddev: 1.8821350910628094e-7",
            "extra": "mean: 459.3632100160037 nsec\nrounds: 191242"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1132291.2227775776,
            "unit": "iter/sec",
            "range": "stddev: 3.478139828609879e-7",
            "extra": "mean: 883.16501963774 nsec\nrounds: 166362"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30654.339526327472,
            "unit": "iter/sec",
            "range": "stddev: 0.000001977416406934452",
            "extra": "mean: 32.621808704805076 usec\nrounds: 13555"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2515730.7669642246,
            "unit": "iter/sec",
            "range": "stddev: 4.8378766499938034e-8",
            "extra": "mean: 397.4988155058946 nsec\nrounds: 73660"
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
          "id": "e0dba90b9308a3d5e86ddf757287945672fc696e",
          "message": "Merge pull request #141 from gabrielima7/refactor/retry-duplication-9356271487030747525\n\n🧹 Extract duplicated RetryError logic in retry decorators",
          "timestamp": "2026-03-06T14:16:13Z",
          "tree_id": "f4fe36d0f49b531cd2caf61bafa1c2960416df14",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/e0dba90b9308a3d5e86ddf757287945672fc696e"
        },
        "date": 1772806663512,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 185141.21918710257,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013968970907874782",
            "extra": "mean: 5.401282352955698 usec\nrounds: 170"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 169438.5560664057,
            "unit": "iter/sec",
            "range": "stddev: 6.282585521155022e-7",
            "extra": "mean: 5.901844439751268 usec\nrounds: 52057"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 58918.632886695574,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010808128941399418",
            "extra": "mean: 16.972559460486227 usec\nrounds: 24983"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 176294.91289995186,
            "unit": "iter/sec",
            "range": "stddev: 7.133058208601389e-7",
            "extra": "mean: 5.6723134181841335 usec\nrounds: 9189"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 125863.75011227248,
            "unit": "iter/sec",
            "range": "stddev: 7.688672099017628e-7",
            "extra": "mean: 7.945099356311757 usec\nrounds: 28896"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 22394.93199227558,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024587954534624715",
            "extra": "mean: 44.652959890430495 usec\nrounds: 11319"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 39231.516127463095,
            "unit": "iter/sec",
            "range": "stddev: 0.000014959330026403541",
            "extra": "mean: 25.4897107914719 usec\nrounds: 17866"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4547897.981702869,
            "unit": "iter/sec",
            "range": "stddev: 2.5640483790847983e-8",
            "extra": "mean: 219.88180122391495 nsec\nrounds: 149032"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 627414.1102227654,
            "unit": "iter/sec",
            "range": "stddev: 1.9886155445952032e-7",
            "extra": "mean: 1.5938436571739718 usec\nrounds: 188076"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1322268.2984765468,
            "unit": "iter/sec",
            "range": "stddev: 2.484666649484576e-7",
            "extra": "mean: 756.2761666086614 nsec\nrounds: 11551"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 647049.3838063573,
            "unit": "iter/sec",
            "range": "stddev: 2.599291798031964e-7",
            "extra": "mean: 1.5454770918988625 usec\nrounds: 78444"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2186896.001458996,
            "unit": "iter/sec",
            "range": "stddev: 2.0786286671941558e-7",
            "extra": "mean: 457.26911537304295 nsec\nrounds: 197629"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1167449.69444795,
            "unit": "iter/sec",
            "range": "stddev: 1.8980012244016685e-7",
            "extra": "mean: 856.5679572796226 nsec\nrounds: 154656"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 31418.329849493704,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015037222653724066",
            "extra": "mean: 31.828553738865107 usec\nrounds: 17064"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2600248.6322187954,
            "unit": "iter/sec",
            "range": "stddev: 3.3835070204505955e-8",
            "extra": "mean: 384.5786082182027 nsec\nrounds: 98435"
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
          "id": "e9032e1dd19f5fd8e5be1f0e80ef1673e3c08778",
          "message": "🛡️ Sentinel: [HIGH] Fix path traversal via symlink resolution bypass (#150)\n\nCo-authored-by: google-labs-jules[bot] <161369871+google-labs-jules[bot]@users.noreply.github.com>\nCo-authored-by: gabrielima7 <230595838+gabrielima7@users.noreply.github.com>",
          "timestamp": "2026-03-09T11:26:12-03:00",
          "tree_id": "0067d5e6dd84460786eb82c18dbe71708d0b2bff",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/e9032e1dd19f5fd8e5be1f0e80ef1673e3c08778"
        },
        "date": 1773066409235,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 212570.14516605347,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015113789381269847",
            "extra": "mean: 4.7043294777769935 usec\nrounds: 173"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 153151.81962904634,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011587546910861698",
            "extra": "mean: 6.529468617624853 usec\nrounds: 64272"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53980.73465932761,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015067754243813488",
            "extra": "mean: 18.525127646205625 usec\nrounds: 32261"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 161005.1974528168,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012416521365572625",
            "extra": "mean: 6.210979619419144 usec\nrounds: 11285"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108660.84400054309,
            "unit": "iter/sec",
            "range": "stddev: 0.000001505504289861049",
            "extra": "mean: 9.202947107561597 usec\nrounds: 44619"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19543.66962349824,
            "unit": "iter/sec",
            "range": "stddev: 0.000004091238999606865",
            "extra": "mean: 51.16746339170892 usec\nrounds: 10503"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33641.724327146396,
            "unit": "iter/sec",
            "range": "stddev: 0.000016725571660541726",
            "extra": "mean: 29.72499240156586 usec\nrounds: 13029"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4518161.188350103,
            "unit": "iter/sec",
            "range": "stddev: 3.06438159059966e-8",
            "extra": "mean: 221.32897838580558 nsec\nrounds: 148766"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 563360.9495807124,
            "unit": "iter/sec",
            "range": "stddev: 6.047645555831994e-7",
            "extra": "mean: 1.7750609103173747 usec\nrounds: 123214"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1066498.2231223977,
            "unit": "iter/sec",
            "range": "stddev: 3.6356157476407205e-7",
            "extra": "mean: 937.6480694663419 nsec\nrounds: 10360"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 620633.2312639224,
            "unit": "iter/sec",
            "range": "stddev: 3.912739533529953e-7",
            "extra": "mean: 1.611257582781211 usec\nrounds: 153799"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2193610.833980228,
            "unit": "iter/sec",
            "range": "stddev: 1.759276297464145e-7",
            "extra": "mean: 455.8693750547977 nsec\nrounds: 181160"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1146446.3072138573,
            "unit": "iter/sec",
            "range": "stddev: 2.7539530795720627e-7",
            "extra": "mean: 872.2606490226678 nsec\nrounds: 166918"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29643.490876346863,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022935245217861377",
            "extra": "mean: 33.73421855648992 usec\nrounds: 22063"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2455583.360055895,
            "unit": "iter/sec",
            "range": "stddev: 4.289024261071637e-8",
            "extra": "mean: 407.23520783967376 nsec\nrounds: 100817"
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
          "id": "f63eff063baa3c7003fbb60814e11f479f39d6d2",
          "message": "chore: release v0.3.7 with path traversal security fix",
          "timestamp": "2026-03-09T11:32:10-03:00",
          "tree_id": "d25acb6b849f4f0f926f0c75a9dc3dc8806a3961",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/f63eff063baa3c7003fbb60814e11f479f39d6d2"
        },
        "date": 1773066774400,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 184087.95122528565,
            "unit": "iter/sec",
            "range": "stddev: 0.000002007888990791068",
            "extra": "mean: 5.4321860466370575 usec\nrounds: 172"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 151189.70013014835,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017930362720686375",
            "extra": "mean: 6.6142071790550006 usec\nrounds: 64688"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 50116.31431748532,
            "unit": "iter/sec",
            "range": "stddev: 0.000005479573301855523",
            "extra": "mean: 19.953582253974837 usec\nrounds: 26868"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 141411.78934966764,
            "unit": "iter/sec",
            "range": "stddev: 0.000002619444926532831",
            "extra": "mean: 7.071546188608852 usec\nrounds: 11518"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 101100.1518938299,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027972465360812808",
            "extra": "mean: 9.8911819741888 usec\nrounds: 31466"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19166.266317761845,
            "unit": "iter/sec",
            "range": "stddev: 0.00000384509215808749",
            "extra": "mean: 52.17500286288288 usec\nrounds: 10479"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 32864.51912329317,
            "unit": "iter/sec",
            "range": "stddev: 0.000013739644832752245",
            "extra": "mean: 30.42795168395562 usec\nrounds: 17489"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4446577.650861516,
            "unit": "iter/sec",
            "range": "stddev: 2.831371310702899e-8",
            "extra": "mean: 224.8920582340942 nsec\nrounds: 194932"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 589122.3666859028,
            "unit": "iter/sec",
            "range": "stddev: 3.752974662172191e-7",
            "extra": "mean: 1.6974402204850176 usec\nrounds: 185529"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1077831.8366489252,
            "unit": "iter/sec",
            "range": "stddev: 2.9715431997308297e-7",
            "extra": "mean: 927.7885157939747 nsec\nrounds: 10275"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 607430.8783444315,
            "unit": "iter/sec",
            "range": "stddev: 5.634780213031874e-7",
            "extra": "mean: 1.6462778493011845 usec\nrounds: 157679"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2933990.373995452,
            "unit": "iter/sec",
            "range": "stddev: 4.4303209629566006e-8",
            "extra": "mean: 340.83274739511626 nsec\nrounds: 116878"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1129155.3461394468,
            "unit": "iter/sec",
            "range": "stddev: 2.926532117587778e-7",
            "extra": "mean: 885.6177349015567 nsec\nrounds: 191205"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29015.738691202332,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020834442563414003",
            "extra": "mean: 34.46405451339425 usec\nrounds: 12474"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2455777.9188686647,
            "unit": "iter/sec",
            "range": "stddev: 4.1921918983338604e-8",
            "extra": "mean: 407.2029446619698 nsec\nrounds: 94527"
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
          "id": "46af4b2ea623fe83d9a3f5037e14a0889128898f",
          "message": "fix(docs): resolve GitHub Pages race condition using concurrency groups",
          "timestamp": "2026-03-09T11:41:31-03:00",
          "tree_id": "8642a5418474972c8a8e650d5ab3da7866ce979d",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/46af4b2ea623fe83d9a3f5037e14a0889128898f"
        },
        "date": 1773067331501,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 170102.55021268778,
            "unit": "iter/sec",
            "range": "stddev: 0.000002637453762100704",
            "extra": "mean: 5.878806630174854 usec\nrounds: 181"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 169152.8958323379,
            "unit": "iter/sec",
            "range": "stddev: 8.233697731357574e-7",
            "extra": "mean: 5.911811294032984 usec\nrounds: 58562"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 55568.31662450282,
            "unit": "iter/sec",
            "range": "stddev: 0.000005571770172555463",
            "extra": "mean: 17.995866363154335 usec\nrounds: 23504"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 173205.24606167042,
            "unit": "iter/sec",
            "range": "stddev: 7.51101740458212e-7",
            "extra": "mean: 5.773497181742094 usec\nrounds: 12064"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 124514.04080105132,
            "unit": "iter/sec",
            "range": "stddev: 7.151238558931838e-7",
            "extra": "mean: 8.031222772681526 usec\nrounds: 40364"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 22308.379026040097,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024646013016906516",
            "extra": "mean: 44.826206280282456 usec\nrounds: 8280"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 39247.17364413967,
            "unit": "iter/sec",
            "range": "stddev: 0.000014013484418269464",
            "extra": "mean: 25.47954176438686 usec\nrounds: 17910"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4628185.652121803,
            "unit": "iter/sec",
            "range": "stddev: 2.408402167918564e-8",
            "extra": "mean: 216.0673912338758 nsec\nrounds: 155449"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 629938.6574545822,
            "unit": "iter/sec",
            "range": "stddev: 1.6754787242030174e-7",
            "extra": "mean: 1.5874561565100935 usec\nrounds: 180213"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1283933.574955378,
            "unit": "iter/sec",
            "range": "stddev: 3.315816349822489e-7",
            "extra": "mean: 778.8564918825758 nsec\nrounds: 11191"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 635697.5620391178,
            "unit": "iter/sec",
            "range": "stddev: 2.6600069426141327e-7",
            "extra": "mean: 1.5730750906017552 usec\nrounds: 137647"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 3004561.6403322243,
            "unit": "iter/sec",
            "range": "stddev: 5.0526168566666675e-8",
            "extra": "mean: 332.8272539249469 nsec\nrounds: 113624"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1142826.2969684668,
            "unit": "iter/sec",
            "range": "stddev: 2.849443990583404e-7",
            "extra": "mean: 875.0236170209445 nsec\nrounds: 140746"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 31598.013490515437,
            "unit": "iter/sec",
            "range": "stddev: 0.000003312180162176565",
            "extra": "mean: 31.647559119504876 usec\nrounds: 20171"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2587352.3465338307,
            "unit": "iter/sec",
            "range": "stddev: 5.7221064686608415e-8",
            "extra": "mean: 386.4954849847338 nsec\nrounds: 90188"
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
          "id": "2f1a52fba8d639e7f67c8f4ed1df114feb2bc3ac",
          "message": "Merge pull request #153 from gabrielima7/testing/add-get-file-hash-traversal-test-14606182429055395803\n\n🧪 [testing] Add test for get_file_hash path traversal block",
          "timestamp": "2026-03-10T11:16:23-03:00",
          "tree_id": "481ca2f262c1521a5fc6a3d9749974c6c2c29ecb",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/2f1a52fba8d639e7f67c8f4ed1df114feb2bc3ac"
        },
        "date": 1773152483926,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 180321.18813550248,
            "unit": "iter/sec",
            "range": "stddev: 0.000002172128192223558",
            "extra": "mean: 5.545659998915653 usec\nrounds: 100"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154837.9584377506,
            "unit": "iter/sec",
            "range": "stddev: 7.917465050414711e-7",
            "extra": "mean: 6.458364667744112 usec\nrounds: 68838"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53923.339832692705,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013928171988494984",
            "extra": "mean: 18.544845387965356 usec\nrounds: 28924"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 162751.81025117767,
            "unit": "iter/sec",
            "range": "stddev: 9.323829873968006e-7",
            "extra": "mean: 6.144324898486123 usec\nrounds: 10868"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108442.50695013192,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011069198278791994",
            "extra": "mean: 9.221476228503803 usec\nrounds: 42404"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19446.656234958784,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035078386668249364",
            "extra": "mean: 51.42272213370668 usec\nrounds: 10685"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33051.16169541761,
            "unit": "iter/sec",
            "range": "stddev: 0.000014030728488802025",
            "extra": "mean: 30.25612259004637 usec\nrounds: 16910"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4474497.139834439,
            "unit": "iter/sec",
            "range": "stddev: 2.855742984552709e-8",
            "extra": "mean: 223.48880080785383 nsec\nrounds: 199641"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590616.4790712293,
            "unit": "iter/sec",
            "range": "stddev: 2.578406287652937e-7",
            "extra": "mean: 1.6931461200888687 usec\nrounds: 186568"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1033212.1126596696,
            "unit": "iter/sec",
            "range": "stddev: 3.7259714804610715e-7",
            "extra": "mean: 967.8554749283999 nsec\nrounds: 9507"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 603490.0880642068,
            "unit": "iter/sec",
            "range": "stddev: 3.684782291480516e-7",
            "extra": "mean: 1.657028043671212 usec\nrounds: 149410"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2944228.1941173766,
            "unit": "iter/sec",
            "range": "stddev: 4.110200396556439e-8",
            "extra": "mean: 339.64758641943865 nsec\nrounds: 111038"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1135383.3736226251,
            "unit": "iter/sec",
            "range": "stddev: 2.538941118943291e-7",
            "extra": "mean: 880.7597708687045 nsec\nrounds: 174217"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29257.041549772068,
            "unit": "iter/sec",
            "range": "stddev: 0.00000233896767904693",
            "extra": "mean: 34.17980585285086 usec\nrounds: 16436"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2447657.7820549905,
            "unit": "iter/sec",
            "range": "stddev: 4.414824980427593e-8",
            "extra": "mean: 408.55384577512916 nsec\nrounds: 92166"
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
          "id": "91f26170be95607f6c049e38f9acbd41e9ab3b6b",
          "message": "Merge pull request #158 from gabrielima7/refactor-pre-commit-generator-13053430366451289637\n\n🧹 Refactor pre-commit configuration generator",
          "timestamp": "2026-03-10T11:16:45-03:00",
          "tree_id": "26133d93f6b1ddec9ce4fd886c478c0370f927f1",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/91f26170be95607f6c049e38f9acbd41e9ab3b6b"
        },
        "date": 1773152535831,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 222367.69406305134,
            "unit": "iter/sec",
            "range": "stddev: 0.000001869688799534494",
            "extra": "mean: 4.497056122354062 usec\nrounds: 196"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 164713.40755312337,
            "unit": "iter/sec",
            "range": "stddev: 6.358553543132701e-7",
            "extra": "mean: 6.071151188329827 usec\nrounds: 61010"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 56943.79868612502,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013688527735884095",
            "extra": "mean: 17.561174756043467 usec\nrounds: 15370"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 175309.38212494334,
            "unit": "iter/sec",
            "range": "stddev: 8.460218207865194e-7",
            "extra": "mean: 5.704201269087231 usec\nrounds: 9455"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 126416.7296169564,
            "unit": "iter/sec",
            "range": "stddev: 7.45005079958104e-7",
            "extra": "mean: 7.910345434738006 usec\nrounds: 40436"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 21964.68962362061,
            "unit": "iter/sec",
            "range": "stddev: 0.0000039650412142573675",
            "extra": "mean: 45.52761806042595 usec\nrounds: 7043"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 39508.699936251,
            "unit": "iter/sec",
            "range": "stddev: 0.000014946533942427167",
            "extra": "mean: 25.310880935427974 usec\nrounds: 16806"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4632313.102768353,
            "unit": "iter/sec",
            "range": "stddev: 2.020098152749482e-8",
            "extra": "mean: 215.87487240497197 nsec\nrounds: 111682"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 629242.6755644934,
            "unit": "iter/sec",
            "range": "stddev: 1.6676980134328734e-7",
            "extra": "mean: 1.5892119826471454 usec\nrounds: 188289"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1320639.401386049,
            "unit": "iter/sec",
            "range": "stddev: 2.1133496651049941e-7",
            "extra": "mean: 757.2089693450545 nsec\nrounds: 9566"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 652717.2897149108,
            "unit": "iter/sec",
            "range": "stddev: 3.4520305874724974e-7",
            "extra": "mean: 1.532056857934272 usec\nrounds: 129551"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 3038953.8395660007,
            "unit": "iter/sec",
            "range": "stddev: 2.7997959443737936e-8",
            "extra": "mean: 329.0606086148319 nsec\nrounds: 118022"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1170154.0369652335,
            "unit": "iter/sec",
            "range": "stddev: 2.3169620358209322e-7",
            "extra": "mean: 854.5883434231241 nsec\nrounds: 182283"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 32161.778409022274,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017315043855989294",
            "extra": "mean: 31.092807968587714 usec\nrounds: 19627"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2456931.084031186,
            "unit": "iter/sec",
            "range": "stddev: 7.98390679776645e-8",
            "extra": "mean: 407.0118232047338 nsec\nrounds: 180408"
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
          "id": "0c30891fbe94db944577c26f0ad4bf2276831761",
          "message": "feat: release TaipanStack v0.3.8 with Bulkhead and SecureBaseModel",
          "timestamp": "2026-03-10T12:02:15-03:00",
          "tree_id": "2b2dc630f22c2537a5d1de94f192deb5ddb30265",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/0c30891fbe94db944577c26f0ad4bf2276831761"
        },
        "date": 1773154978710,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 145380.88003908546,
            "unit": "iter/sec",
            "range": "stddev: 0.000002380884925753667",
            "extra": "mean: 6.8784836061740116 usec\nrounds: 122"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 151462.6624712001,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010153010222023872",
            "extra": "mean: 6.60228721510917 usec\nrounds: 63012"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52946.05340826428,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018340714866578344",
            "extra": "mean: 18.887149005971263 usec\nrounds: 25905"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 162183.8849285248,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012612314867039294",
            "extra": "mean: 6.165840708777599 usec\nrounds: 10440"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 107444.12683210435,
            "unit": "iter/sec",
            "range": "stddev: 0.000001833402976209228",
            "extra": "mean: 9.307162983069631 usec\nrounds: 40857"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 15328.687354619431,
            "unit": "iter/sec",
            "range": "stddev: 0.00002159186805014401",
            "extra": "mean: 65.23715807268006 usec\nrounds: 5915"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33869.44398336645,
            "unit": "iter/sec",
            "range": "stddev: 0.000015907845549317953",
            "extra": "mean: 29.525137775840303 usec\nrounds: 16222"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4419451.120010777,
            "unit": "iter/sec",
            "range": "stddev: 3.3455483960480294e-8",
            "extra": "mean: 226.27244262803077 nsec\nrounds: 148766"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590135.8228896,
            "unit": "iter/sec",
            "range": "stddev: 2.5483800430010307e-7",
            "extra": "mean: 1.694525160502008 usec\nrounds: 186602"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1045144.9739496736,
            "unit": "iter/sec",
            "range": "stddev: 4.3240368044173297e-7",
            "extra": "mean: 956.8050604701588 nsec\nrounds: 10829"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 586698.5023312196,
            "unit": "iter/sec",
            "range": "stddev: 3.966543670986419e-7",
            "extra": "mean: 1.7044529618305582 usec\nrounds: 147646"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2944407.04636923,
            "unit": "iter/sec",
            "range": "stddev: 3.991145545461165e-8",
            "extra": "mean: 339.6269551905259 nsec\nrounds: 111025"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1127097.1250270966,
            "unit": "iter/sec",
            "range": "stddev: 2.824456767252811e-7",
            "extra": "mean: 887.2349842751652 nsec\nrounds: 194213"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29333.370523566453,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022964541917335618",
            "extra": "mean: 34.090865868843785 usec\nrounds: 17632"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2438299.6723953476,
            "unit": "iter/sec",
            "range": "stddev: 5.622835253009323e-8",
            "extra": "mean: 410.1218612795331 nsec\nrounds: 51932"
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
          "id": "4633605cfd3b59a68263ef0375664e37496de36c",
          "message": "docs: merge v0.3.8 release notes with prior PR changes",
          "timestamp": "2026-03-10T12:05:16-03:00",
          "tree_id": "e19497a425549ecfc9c98f13053632260372ff29",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/4633605cfd3b59a68263ef0375664e37496de36c"
        },
        "date": 1773155206384,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 188251.7900161672,
            "unit": "iter/sec",
            "range": "stddev: 0.000003530203756258611",
            "extra": "mean: 5.312034482721888 usec\nrounds: 58"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 153578.32706551216,
            "unit": "iter/sec",
            "range": "stddev: 0.000001210291674646076",
            "extra": "mean: 6.511335415012227 usec\nrounds: 61649"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54085.6846892866,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018880296159029538",
            "extra": "mean: 18.489180746159285 usec\nrounds: 27475"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163484.73877689382,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011726483754093656",
            "extra": "mean: 6.116778896192208 usec\nrounds: 11325"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110245.27263264137,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011868207786345727",
            "extra": "mean: 9.070683722940156 usec\nrounds: 43933"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19492.104075948184,
            "unit": "iter/sec",
            "range": "stddev: 0.000021018246884511283",
            "extra": "mean: 51.302824779902856 usec\nrounds: 9314"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33461.93051833457,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032603811478790686",
            "extra": "mean: 29.88470732291064 usec\nrounds: 16619"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4428153.926437941,
            "unit": "iter/sec",
            "range": "stddev: 3.1113885454599204e-8",
            "extra": "mean: 225.8277414500186 nsec\nrounds: 149410"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 593321.3095803587,
            "unit": "iter/sec",
            "range": "stddev: 2.430874441272015e-7",
            "extra": "mean: 1.6854274131957054 usec\nrounds: 185874"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1065376.6999997513,
            "unit": "iter/sec",
            "range": "stddev: 4.3652753230978155e-7",
            "extra": "mean: 938.6351325312761 nsec\nrounds: 10486"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 614357.7874708836,
            "unit": "iter/sec",
            "range": "stddev: 4.045319428262782e-7",
            "extra": "mean: 1.6277159993636336 usec\nrounds: 139218"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2225654.1557966624,
            "unit": "iter/sec",
            "range": "stddev: 1.8723450370947283e-7",
            "extra": "mean: 449.30610508174607 nsec\nrounds: 178540"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1141566.9820707373,
            "unit": "iter/sec",
            "range": "stddev: 2.925446201740251e-7",
            "extra": "mean: 875.9888957072473 nsec\nrounds: 185874"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29731.049961644057,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021983955460240245",
            "extra": "mean: 33.6348699857589 usec\nrounds: 16852"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2490166.4691063194,
            "unit": "iter/sec",
            "range": "stddev: 4.301666942376098e-8",
            "extra": "mean: 401.57957807498894 nsec\nrounds: 78450"
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
          "id": "c35c23fde6f41be7605c93966fe0dde95c6a2956",
          "message": "Merge pull request #169 from gabrielima7/perf-jwt-alg-check-optimization-15410613442699169237\n\n⚡ Optimize JWT algorithm check efficiency",
          "timestamp": "2026-03-11T13:00:41-03:00",
          "tree_id": "ff1a44809948816fcb6d80cbf7725377a8cca3dd",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/c35c23fde6f41be7605c93966fe0dde95c6a2956"
        },
        "date": 1773244880277,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 182563.4703301602,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030465681613697627",
            "extra": "mean: 5.4775470590668105 usec\nrounds: 170"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 148717.4800415141,
            "unit": "iter/sec",
            "range": "stddev: 8.867848789311807e-7",
            "extra": "mean: 6.72415912185207 usec\nrounds: 68325"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 50415.651636436734,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015139696593041598",
            "extra": "mean: 19.835110080720913 usec\nrounds: 20812"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 163486.10450201036,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013584299023410701",
            "extra": "mean: 6.116727798035601 usec\nrounds: 11767"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 107450.65424518433,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011347291221028964",
            "extra": "mean: 9.306597591468995 usec\nrounds: 42765"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19251.248409706932,
            "unit": "iter/sec",
            "range": "stddev: 0.000018711956357000795",
            "extra": "mean: 51.944683207961546 usec\nrounds: 10237"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33472.18357807839,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029511126464601616",
            "extra": "mean: 29.8755531639388 usec\nrounds: 17004"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 2889491.019977714,
            "unit": "iter/sec",
            "range": "stddev: 2.8416985583128363e-7",
            "extra": "mean: 346.0817123452119 nsec\nrounds: 175408"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 559410.6245354763,
            "unit": "iter/sec",
            "range": "stddev: 8.83718487539618e-7",
            "extra": "mean: 1.7875956518172493 usec\nrounds: 187266"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 772946.9815621958,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013422698057944778",
            "extra": "mean: 1.2937497963688394 usec\nrounds: 7366"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 553105.5740341566,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011812386337151979",
            "extra": "mean: 1.8079731012406066 usec\nrounds: 153799"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2207168.2797267986,
            "unit": "iter/sec",
            "range": "stddev: 2.0110477381376975e-7",
            "extra": "mean: 453.0692150594785 nsec\nrounds: 159185"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1133688.8937550471,
            "unit": "iter/sec",
            "range": "stddev: 2.842320727432356e-7",
            "extra": "mean: 882.0762075985083 nsec\nrounds: 182449"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29968.767450395942,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033185420778730743",
            "extra": "mean: 33.3680723324772 usec\nrounds: 13908"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2346042.5782604166,
            "unit": "iter/sec",
            "range": "stddev: 1.0301223270916496e-7",
            "extra": "mean: 426.2497233707872 nsec\nrounds: 157431"
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
          "id": "c38837fbeb4bba5cb30739aa15495db3a3118f10",
          "message": "Merge pull request #159 from gabrielima7/testing-improvement-app-main-5599066362647940332\n\n🧪 [testing improvement] Add tests for app.main module",
          "timestamp": "2026-03-11T13:01:19-03:00",
          "tree_id": "a8b30a0213121daa45cf59ea86fd9a17d74b1075",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/c38837fbeb4bba5cb30739aa15495db3a3118f10"
        },
        "date": 1773245432533,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 169552.74934131285,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022497562451390646",
            "extra": "mean: 5.897869564987008 usec\nrounds: 161"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 156047.19012744701,
            "unit": "iter/sec",
            "range": "stddev: 7.888402882141108e-7",
            "extra": "mean: 6.4083178888596395 usec\nrounds: 64856"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52927.47628043045,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014420947955232525",
            "extra": "mean: 18.893778246701377 usec\nrounds: 30092"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 144527.31290864584,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028164943366769155",
            "extra": "mean: 6.9191073982818 usec\nrounds: 8948"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 104121.6986368488,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024801655543110845",
            "extra": "mean: 9.604146043446306 usec\nrounds: 44028"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 17695.70579949375,
            "unit": "iter/sec",
            "range": "stddev: 0.00001406656122911653",
            "extra": "mean: 56.510885258309884 usec\nrounds: 9212"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33503.89526022294,
            "unit": "iter/sec",
            "range": "stddev: 0.00001633166976953797",
            "extra": "mean: 29.84727573415133 usec\nrounds: 16447"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4448676.725901166,
            "unit": "iter/sec",
            "range": "stddev: 2.9539470993754742e-8",
            "extra": "mean: 224.78594458825407 nsec\nrounds: 145709"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 561367.6911839449,
            "unit": "iter/sec",
            "range": "stddev: 6.671610889406246e-7",
            "extra": "mean: 1.7813636511409545 usec\nrounds: 172088"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1076255.303425778,
            "unit": "iter/sec",
            "range": "stddev: 3.4397047599921814e-7",
            "extra": "mean: 929.1475701136586 nsec\nrounds: 10700"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 596943.5708100132,
            "unit": "iter/sec",
            "range": "stddev: 3.978869138942875e-7",
            "extra": "mean: 1.6752002180759997 usec\nrounds: 154991"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2936768.732564408,
            "unit": "iter/sec",
            "range": "stddev: 4.171976046812431e-8",
            "extra": "mean: 340.5102992657185 nsec\nrounds: 115115"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1039865.7296689654,
            "unit": "iter/sec",
            "range": "stddev: 2.846634762935873e-7",
            "extra": "mean: 961.6626180366032 nsec\nrounds: 176026"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29032.495027407513,
            "unit": "iter/sec",
            "range": "stddev: 0.00000279007611651511",
            "extra": "mean: 34.444163309284 usec\nrounds: 15786"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2434613.6975037367,
            "unit": "iter/sec",
            "range": "stddev: 7.065608689160434e-8",
            "extra": "mean: 410.74278068236856 nsec\nrounds: 52782"
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
          "id": "e16390c4950423e43900f115d83458299019026b",
          "message": "Merge pull request #170 from gabrielima7/refactor-unused-logging-params-10525564069122353476\n\n🧹 Refactor: rename unused structlog processor parameters",
          "timestamp": "2026-03-11T13:20:48-03:00",
          "tree_id": "29fc40cabda46f5f6cd14994fecb52c87a332eed",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/e16390c4950423e43900f115d83458299019026b"
        },
        "date": 1773246091868,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 205968.88490977953,
            "unit": "iter/sec",
            "range": "stddev: 7.969627405685926e-7",
            "extra": "mean: 4.855102266723586 usec\nrounds: 1897"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 150015.39737295368,
            "unit": "iter/sec",
            "range": "stddev: 8.866794058335794e-7",
            "extra": "mean: 6.665982409218285 usec\nrounds: 60202"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 51941.52581373065,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017948622296945184",
            "extra": "mean: 19.252418644499116 usec\nrounds: 26839"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 158019.1577098496,
            "unit": "iter/sec",
            "range": "stddev: 0.000001152881368553196",
            "extra": "mean: 6.328346603619876 usec\nrounds: 8038"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108750.46116298556,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012847174158403432",
            "extra": "mean: 9.195363305184411 usec\nrounds: 38703"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 18960.732084356143,
            "unit": "iter/sec",
            "range": "stddev: 0.00000410083212431091",
            "extra": "mean: 52.74057961216941 usec\nrounds: 9025"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33621.49461268185,
            "unit": "iter/sec",
            "range": "stddev: 0.000017405378219479482",
            "extra": "mean: 29.74287762991968 usec\nrounds: 17063"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4440728.4595940225,
            "unit": "iter/sec",
            "range": "stddev: 4.039912302120779e-8",
            "extra": "mean: 225.1882791525714 nsec\nrounds: 150083"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 588662.4307438688,
            "unit": "iter/sec",
            "range": "stddev: 3.103949304760789e-7",
            "extra": "mean: 1.698766470855631 usec\nrounds: 186916"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1058267.7192117898,
            "unit": "iter/sec",
            "range": "stddev: 4.32331380742036e-7",
            "extra": "mean: 944.9404738007238 nsec\nrounds: 9626"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 620489.1597599805,
            "unit": "iter/sec",
            "range": "stddev: 3.993738184537399e-7",
            "extra": "mean: 1.611631701006385 usec\nrounds: 153093"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2670415.8581732986,
            "unit": "iter/sec",
            "range": "stddev: 1.4539945208728983e-7",
            "extra": "mean: 374.4735101610354 nsec\nrounds: 107562"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1129397.839461649,
            "unit": "iter/sec",
            "range": "stddev: 3.1471098508754585e-7",
            "extra": "mean: 885.4275836729693 nsec\nrounds: 133637"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29282.992601834576,
            "unit": "iter/sec",
            "range": "stddev: 0.000003254470541826997",
            "extra": "mean: 34.14951516729032 usec\nrounds: 13483"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2446819.825235007,
            "unit": "iter/sec",
            "range": "stddev: 4.988295559566641e-8",
            "extra": "mean: 408.69376228148263 nsec\nrounds: 27991"
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
          "id": "d8b647d14cabef760364f789e4d9b0e0413277ae",
          "message": "Merge pull request #171 from gabrielima7/fix-pre-commit-testing-improvement-3744193781306393561\n\n🧪 [testing improvement] Add coverage for pre-commit setup",
          "timestamp": "2026-03-11T13:20:51-03:00",
          "tree_id": "37044261a131443902b9c6ac973933db9915f598",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/d8b647d14cabef760364f789e4d9b0e0413277ae"
        },
        "date": 1773246139240,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 185576.11727132424,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010815631528764334",
            "extra": "mean: 5.388624434565228 usec\nrounds: 221"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 154851.65013094904,
            "unit": "iter/sec",
            "range": "stddev: 8.438680799616535e-7",
            "extra": "mean: 6.457793631222903 usec\nrounds: 62461"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 54099.65487139073,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016562249881532004",
            "extra": "mean: 18.484406275368407 usec\nrounds: 23425"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164114.0382501399,
            "unit": "iter/sec",
            "range": "stddev: 9.895289304233504e-7",
            "extra": "mean: 6.093323951213829 usec\nrounds: 11227"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 109719.90165409796,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014026049156156818",
            "extra": "mean: 9.114116809479027 usec\nrounds: 38627"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19531.825500588762,
            "unit": "iter/sec",
            "range": "stddev: 0.000020840215163660283",
            "extra": "mean: 51.19849140418832 usec\nrounds: 10063"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33765.118820853546,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030637539000072733",
            "extra": "mean: 29.616362533941203 usec\nrounds: 16575"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4536126.941560342,
            "unit": "iter/sec",
            "range": "stddev: 3.087992001599809e-8",
            "extra": "mean: 220.45238435390436 nsec\nrounds: 151907"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 582442.0797314413,
            "unit": "iter/sec",
            "range": "stddev: 3.330018148489775e-7",
            "extra": "mean: 1.7169089164388351 usec\nrounds: 187231"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 2138311.8264633003,
            "unit": "iter/sec",
            "range": "stddev: 2.2306900030418578e-7",
            "extra": "mean: 467.65863969146545 nsec\nrounds: 167477"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 644524.0798437222,
            "unit": "iter/sec",
            "range": "stddev: 3.877459826684365e-7",
            "extra": "mean: 1.5515324117020892 usec\nrounds: 144238"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2626042.2180571905,
            "unit": "iter/sec",
            "range": "stddev: 1.226939292305733e-7",
            "extra": "mean: 380.80118938064004 nsec\nrounds: 111907"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1136798.906141445,
            "unit": "iter/sec",
            "range": "stddev: 2.7775888760869895e-7",
            "extra": "mean: 879.6630561461643 nsec\nrounds: 167197"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29702.13440609929,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022351380119815082",
            "extra": "mean: 33.667614129261075 usec\nrounds: 13787"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2450130.9658859354,
            "unit": "iter/sec",
            "range": "stddev: 4.450584260119183e-8",
            "extra": "mean: 408.1414479156377 nsec\nrounds: 78285"
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
          "id": "9e834337132b3ccbd466b7642ae37e007cfa91ef",
          "message": "docs: finalize v0.3.9 English release notes, CHANGELOG, and fix duplicate conflict markers",
          "timestamp": "2026-03-11T15:24:09-03:00",
          "tree_id": "681f7793962538e51c7774ac2867977e8de09356",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/9e834337132b3ccbd466b7642ae37e007cfa91ef"
        },
        "date": 1773253561886,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 227295.73235698813,
            "unit": "iter/sec",
            "range": "stddev: 8.016330392802555e-7",
            "extra": "mean: 4.399554666646408 usec\nrounds: 2250"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 160861.97919487496,
            "unit": "iter/sec",
            "range": "stddev: 8.391086797614383e-7",
            "extra": "mean: 6.216509364146005 usec\nrounds: 67331"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 56809.900861899616,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016254757423342555",
            "extra": "mean: 17.602565482923847 usec\nrounds: 21120"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164170.8390168123,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010592393394557944",
            "extra": "mean: 6.091215748112201 usec\nrounds: 10795"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 117401.90504071533,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011119164234566501",
            "extra": "mean: 8.517749347024624 usec\nrounds: 44799"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 20166.56232502896,
            "unit": "iter/sec",
            "range": "stddev: 0.00002060787902868795",
            "extra": "mean: 49.5870334211046 usec\nrounds: 10263"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 36007.24227734948,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021316384626329933",
            "extra": "mean: 27.772190724782455 usec\nrounds: 18005"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4263362.453956277,
            "unit": "iter/sec",
            "range": "stddev: 3.8853315601457167e-8",
            "extra": "mean: 234.55664649684272 nsec\nrounds: 152208"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 543794.1949713465,
            "unit": "iter/sec",
            "range": "stddev: 2.8719972668897103e-7",
            "extra": "mean: 1.8389309949377055 usec\nrounds: 169234"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 2522759.7337533217,
            "unit": "iter/sec",
            "range": "stddev: 1.8565371649059746e-7",
            "extra": "mean: 396.39129585765824 nsec\nrounds: 143679"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 669681.362134989,
            "unit": "iter/sec",
            "range": "stddev: 5.063696548499648e-7",
            "extra": "mean: 1.4932474704267311 usec\nrounds: 127195"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2179263.1915037306,
            "unit": "iter/sec",
            "range": "stddev: 6.407789186094287e-7",
            "extra": "mean: 458.87068799156015 nsec\nrounds: 180571"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1086380.1558247877,
            "unit": "iter/sec",
            "range": "stddev: 0.000001106942586307648",
            "extra": "mean: 920.4880949254755 nsec\nrounds: 158756"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 33876.46755467381,
            "unit": "iter/sec",
            "range": "stddev: 0.000002405717478769976",
            "extra": "mean: 29.519016361020615 usec\nrounds: 15708"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2828936.6071835076,
            "unit": "iter/sec",
            "range": "stddev: 5.614845984757306e-8",
            "extra": "mean: 353.48971675818393 nsec\nrounds: 75307"
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
          "id": "b0895afced8ec86d86da72976fb5230215861410",
          "message": "feat: restore SafeHtml, SafeSqlIdentifier, resilience, cache, and context modules lost in rebase",
          "timestamp": "2026-03-11T15:42:52-03:00",
          "tree_id": "c070a5ab9260f1e5b807ead5badc6323ebc0f473",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/b0895afced8ec86d86da72976fb5230215861410"
        },
        "date": 1773254614750,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 191669.2167736019,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017697257832259899",
            "extra": "mean: 5.217321888371839 usec\nrounds: 233"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155517.31389535088,
            "unit": "iter/sec",
            "range": "stddev: 8.20185710849422e-7",
            "extra": "mean: 6.430152212331225 usec\nrounds: 65067"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53091.05919451141,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015771013091694215",
            "extra": "mean: 18.83556318468366 usec\nrounds: 27293"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164384.51361155257,
            "unit": "iter/sec",
            "range": "stddev: 9.55244503552818e-7",
            "extra": "mean: 6.083298104120936 usec\nrounds: 9547"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110068.45065129324,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010760294847754031",
            "extra": "mean: 9.085255530379817 usec\nrounds: 42402"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19579.773590471283,
            "unit": "iter/sec",
            "range": "stddev: 0.00002050002625297888",
            "extra": "mean: 51.07311355666856 usec\nrounds: 10268"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33419.730760468155,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028316049947496227",
            "extra": "mean: 29.92244333646426 usec\nrounds: 12636"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 3939061.8749840087,
            "unit": "iter/sec",
            "range": "stddev: 8.232638003588061e-8",
            "extra": "mean: 253.86755317312995 nsec\nrounds: 143823"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 590021.0749124418,
            "unit": "iter/sec",
            "range": "stddev: 2.497431497618112e-7",
            "extra": "mean: 1.6948547137039434 usec\nrounds: 186916"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 2131562.756519255,
            "unit": "iter/sec",
            "range": "stddev: 2.0438616142308538e-7",
            "extra": "mean: 469.13936591430894 nsec\nrounds: 157456"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 648570.0642907127,
            "unit": "iter/sec",
            "range": "stddev: 3.627533463065533e-7",
            "extra": "mean: 1.5418534635785526 usec\nrounds: 144865"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2955083.984948879,
            "unit": "iter/sec",
            "range": "stddev: 3.786226514365793e-8",
            "extra": "mean: 338.39985770056524 nsec\nrounds: 112791"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1131889.7894268208,
            "unit": "iter/sec",
            "range": "stddev: 2.8041265941591146e-7",
            "extra": "mean: 883.4782408509853 nsec\nrounds: 97752"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30788.76551913776,
            "unit": "iter/sec",
            "range": "stddev: 0.000002012467043693857",
            "extra": "mean: 32.47937951193325 usec\nrounds: 12661"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2566393.883994994,
            "unit": "iter/sec",
            "range": "stddev: 4.261808138084172e-8",
            "extra": "mean: 389.6518013998483 nsec\nrounds: 108027"
          }
        ]
      }
    ]
  }
}