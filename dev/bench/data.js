window.BENCHMARK_DATA = {
  "lastUpdate": 1772214816521,
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
          "id": "40999c1c0329a6e96666e8c78fb070b0b501603d",
          "message": "feat(docs): add MkDocs Material documentation portal\n\n- Add mkdocs-material + mkdocstrings[python] to pyproject.toml [docs group]\n\n- Create mkdocs.yml with dark/light theme toggle, tabbed nav, mermaid support\n\n- Create docs/index.md, docs/architecture.md, docs/api/{core,security,utils}.md\n\n- Auto-generate API reference from docstrings via mkdocstrings\n\n- Reorganize docs/FEATURES_* into docs/releases/v0.3.{0,1}.md\n\n- Add .github/workflows/docs.yml with keep_files: true to preserve htmlcov/ and dev/bench/\n\n- Update Documentation URL to https://gabrielima7.github.io/TaipanStack/",
          "timestamp": "2026-02-27T12:07:08-03:00",
          "tree_id": "990ee1650009899279f57a60cc3240d5bc2874ac",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/40999c1c0329a6e96666e8c78fb070b0b501603d"
        },
        "date": 1772204879750,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 220524.21105679582,
            "unit": "iter/sec",
            "range": "stddev: 8.911632159721471e-7",
            "extra": "mean: 4.5346494845522916 usec\nrounds: 1843"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 155377.553481461,
            "unit": "iter/sec",
            "range": "stddev: 9.219994685892952e-7",
            "extra": "mean: 6.435936064080941 usec\nrounds: 70993"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 53482.297195361374,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015828639950572305",
            "extra": "mean: 18.697775758344424 usec\nrounds: 28117"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 167064.94238164366,
            "unit": "iter/sec",
            "range": "stddev: 9.71776506623967e-7",
            "extra": "mean: 5.985696255265793 usec\nrounds: 11750"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 110713.11735871647,
            "unit": "iter/sec",
            "range": "stddev: 0.000001155255583138454",
            "extra": "mean: 9.03235338193889 usec\nrounds: 43644"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19760.36470200853,
            "unit": "iter/sec",
            "range": "stddev: 0.000003964432021608113",
            "extra": "mean: 50.60635342921356 usec\nrounds: 9040"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33842.53133473145,
            "unit": "iter/sec",
            "range": "stddev: 0.000015242373305474268",
            "extra": "mean: 29.548617096905325 usec\nrounds: 16892"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4501736.212441592,
            "unit": "iter/sec",
            "range": "stddev: 3.136474309601278e-8",
            "extra": "mean: 222.13651640364785 nsec\nrounds: 151447"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 589742.1842154455,
            "unit": "iter/sec",
            "range": "stddev: 2.412545952082135e-7",
            "extra": "mean: 1.6956562151482784 usec\nrounds: 185874"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 1087710.2111803412,
            "unit": "iter/sec",
            "range": "stddev: 3.1546864923776837e-7",
            "extra": "mean: 919.3625192824461 nsec\nrounds: 10907"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 602588.8427668555,
            "unit": "iter/sec",
            "range": "stddev: 3.867301924700359e-7",
            "extra": "mean: 1.6595063317275935 usec\nrounds: 164963"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2938326.9936608006,
            "unit": "iter/sec",
            "range": "stddev: 4.182072237185509e-8",
            "extra": "mean: 340.3297189718492 nsec\nrounds: 112906"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1152010.6721042763,
            "unit": "iter/sec",
            "range": "stddev: 3.1853357751532827e-7",
            "extra": "mean: 868.0475139812621 nsec\nrounds: 185840"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 30138.962107178395,
            "unit": "iter/sec",
            "range": "stddev: 0.000002477793861221625",
            "extra": "mean: 33.179642896920576 usec\nrounds: 19801"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2511013.5223886375,
            "unit": "iter/sec",
            "range": "stddev: 4.481692237992096e-8",
            "extra": "mean: 398.2455654196381 nsec\nrounds: 80109"
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
          "id": "9fd5dbc31597293fa763e59992f7df28673ba536",
          "message": "fix(docs): correct bugs and fill incomplete content across portal\n\nci.yml: add --cov-report=html + upload htmlcov artifact for gh-pages\n\ndocs.yml: add workflow_run trigger + download htmlcov artifact + actions:read\n\narchitecture.md: rewrite with mermaid graph, import contracts table, full project structure\n\ndocs/api/config.md: new page for config package (models, generators, version_config)\n\nmkdocs.yml: add Config to nav\n\nindex.md: add Live Reports section (Coverage + Benchmarks links)\n\nreleases/v0.3.1.md: fix test count (664→683), add Reports links",
          "timestamp": "2026-02-27T14:42:33-03:00",
          "tree_id": "62ff27d59e1f79b49cee0132f60b4cec11e7a796",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/9fd5dbc31597293fa763e59992f7df28673ba536"
        },
        "date": 1772214192218,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 172284.86715800042,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016964946631325837",
            "extra": "mean: 5.804340314363837 usec\nrounds: 191"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 136251.87736124411,
            "unit": "iter/sec",
            "range": "stddev: 8.914780719873251e-7",
            "extra": "mean: 7.339348413884262 usec\nrounds: 63614"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 52837.17829107239,
            "unit": "iter/sec",
            "range": "stddev: 0.000004451529539869047",
            "extra": "mean: 18.926067446129395 usec\nrounds: 33271"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 157942.4777858523,
            "unit": "iter/sec",
            "range": "stddev: 0.000001929144368919098",
            "extra": "mean: 6.331418969859767 usec\nrounds: 11144"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 102507.86045382316,
            "unit": "iter/sec",
            "range": "stddev: 0.000002791357117937871",
            "extra": "mean: 9.755349449035386 usec\nrounds: 44739"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19751.665642570973,
            "unit": "iter/sec",
            "range": "stddev: 0.000004570560578973031",
            "extra": "mean: 50.628641558446056 usec\nrounds: 11165"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 34521.911567993906,
            "unit": "iter/sec",
            "range": "stddev: 0.000014557466867501993",
            "extra": "mean: 28.96710971611213 usec\nrounds: 17682"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4495500.909258273,
            "unit": "iter/sec",
            "range": "stddev: 3.214465583442374e-8",
            "extra": "mean: 222.44462189755635 nsec\nrounds: 93546"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 562842.0968884667,
            "unit": "iter/sec",
            "range": "stddev: 4.789731325302263e-7",
            "extra": "mean: 1.7766972398266805 usec\nrounds: 163106"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 755520.4623128648,
            "unit": "iter/sec",
            "range": "stddev: 9.785499550264375e-7",
            "extra": "mean: 1.3235908885097742 usec\nrounds: 6629"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 622158.9076236896,
            "unit": "iter/sec",
            "range": "stddev: 4.1071909659165576e-7",
            "extra": "mean: 1.6073064095786378 usec\nrounds: 112020"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2906537.50562818,
            "unit": "iter/sec",
            "range": "stddev: 4.259322144264771e-8",
            "extra": "mean: 344.0519855888351 nsec\nrounds: 111025"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1114797.0674485653,
            "unit": "iter/sec",
            "range": "stddev: 2.643768072919963e-7",
            "extra": "mean: 897.0242470126861 nsec\nrounds: 173011"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 29433.060031312172,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021299166284141965",
            "extra": "mean: 33.975400414912905 usec\nrounds: 18316"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2484827.0534172775,
            "unit": "iter/sec",
            "range": "stddev: 5.424978335684361e-8",
            "extra": "mean: 402.44249539418496 nsec\nrounds: 76553"
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
          "id": "dd537ce8c60c4c4d88b103cb12d0b27eba7c8637",
          "message": "fix(docs+ci): fix XSS in security docstring and relax benchmark threshold\n\nXSS: sanitizers.py docstrings had raw <script>alert('xss')</script> and\n\n<>: characters in '>>>' examples that mkdocstrings rendered as real HTML.\n\nFixed by wrapping examples in fenced python code blocks.\n\nBenchmark: threshold 105% -> 130% to account for GitHub Actions runner\n\nvariance (10-30% natural noise). Prevents false performance alerts.",
          "timestamp": "2026-02-27T14:53:03-03:00",
          "tree_id": "7bd13406ab4ee522d2c1cc83bb14d62e0ac49514",
          "url": "https://github.com/gabrielima7/TaipanStack/commit/dd537ce8c60c4c4d88b103cb12d0b27eba7c8637"
        },
        "date": 1772214816127,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_simple",
            "value": 209546.8195213421,
            "unit": "iter/sec",
            "range": "stddev: 8.104048126259116e-7",
            "extra": "mean: 4.7722031872602635 usec\nrounds: 1757"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_xss",
            "value": 151840.53593935806,
            "unit": "iter/sec",
            "range": "stddev: 9.13684750930952e-7",
            "extra": "mean: 6.585856627899279 usec\nrounds: 66854"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_string_unicode",
            "value": 51480.611076031964,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024858808169606104",
            "extra": "mean: 19.424788849594172 usec\nrounds: 24627"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_complex",
            "value": 164238.5561179249,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013518596349285038",
            "extra": "mean: 6.088704282580213 usec\nrounds: 8126"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_filename_long",
            "value": 108433.04299410383,
            "unit": "iter/sec",
            "range": "stddev: 0.000001819979848784642",
            "extra": "mean: 9.222281072148608 usec\nrounds: 45515"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_nested",
            "value": 19118.317703809353,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035008972328802387",
            "extra": "mean: 52.305857423885605 usec\nrounds: 9658"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_path_traversal",
            "value": 33138.757114571235,
            "unit": "iter/sec",
            "range": "stddev: 0.000013581369126001032",
            "extra": "mean: 30.17614681632994 usec\nrounds: 16742"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_standard",
            "value": 4479076.271483064,
            "unit": "iter/sec",
            "range": "stddev: 3.011526997973409e-8",
            "extra": "mean: 223.26031962580578 nsec\nrounds: 151677"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_env_value_large",
            "value": 560471.5821195744,
            "unit": "iter/sec",
            "range": "stddev: 4.804596247992506e-7",
            "extra": "mean: 1.784211781475575 usec\nrounds: 161525"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier",
            "value": 780016.5892098092,
            "unit": "iter/sec",
            "range": "stddev: 9.083803414317024e-7",
            "extra": "mean: 1.2820240156854146 usec\nrounds: 7162"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_sanitize_sql_identifier_dirty",
            "value": 616420.5080101981,
            "unit": "iter/sec",
            "range": "stddev: 4.422145556349293e-7",
            "extra": "mean: 1.6222691928728885 usec\nrounds: 151241"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_ok",
            "value": 2266186.4434857047,
            "unit": "iter/sec",
            "range": "stddev: 1.9900255985058187e-7",
            "extra": "mean: 441.26995943981706 nsec\nrounds: 199204"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_safe_decorator_err",
            "value": 1121960.3259046818,
            "unit": "iter/sec",
            "range": "stddev: 2.6645005117275743e-7",
            "extra": "mean: 891.2971135531549 nsec\nrounds: 172981"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_collect_results_100",
            "value": 28449.817868862636,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019719905159215985",
            "extra": "mean: 35.14960990644745 usec\nrounds: 17201"
          },
          {
            "name": "tests/test_benchmarks.py::test_bench_unwrap_or",
            "value": 2418337.648149449,
            "unit": "iter/sec",
            "range": "stddev: 4.331169050616572e-8",
            "extra": "mean: 413.507187784649 nsec\nrounds: 34816"
          }
        ]
      }
    ]
  }
}