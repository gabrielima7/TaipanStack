from taipanstack.security.sanitizers import sanitize_path
import timeit
import pathlib

# Let's compare parsing a string into Path, and working with parts vs direct string manipulation for sanitize_path
def opt_sanitize_path(path, *, base_dir=None, max_depth=10, resolve=False):
    if type(path) is not pathlib.Path:
        if type(path) is not str:
            raise TypeError("must be str or Path")
        # Removing null bytes
        path_str = path.replace("\x00", "")
        # Then let Path parse it, instead of Path(str(path).replace("\x00", ""))
        path = pathlib.Path(path_str)
    else:
        path = pathlib.Path(str(path).replace("\x00", ""))

    # ...
