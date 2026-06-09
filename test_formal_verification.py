from taipanstack.core.result import Ok, Err, collect_results

print(collect_results((x for x in [Ok(1), Err(ValueError("err"))])))
print(collect_results((x for x in [Ok(1), Ok(2)])))
