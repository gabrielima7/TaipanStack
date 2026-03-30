from taipanstack.security.sanitizers import sanitize_filename
import timeit
import cProfile

cProfile.run("[sanitize_filename('my/../file<>:name.txt') for _ in range(1000000)]", sort='tottime')
