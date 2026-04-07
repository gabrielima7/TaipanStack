from result import Ok, Err
from taipanstack.core.result import collect_results

results1 = [Ok(1), Err(ValueError("error")), Ok(3)]
print("results1:", collect_results(results1))

results2 = [Ok(1), Err(ValueError("first")), Err(ValueError("second"))]
print("results2:", collect_results(results2))
