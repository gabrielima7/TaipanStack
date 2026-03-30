from taipanstack.security.sanitizers import sanitize_path
import timeit
import cProfile

cProfile.run("[sanitize_path('a/b/c/d/e/f/g/h/file.txt', max_depth=10) for _ in range(100000)]", sort='tottime')
