import re
from pathlib import Path

p = Path('src/taipanstack/security/jwt.py')
text = p.read_text()
text = text.replace('from typing import Any, TypeAlias, cast', 'from typing import Any, TypeAlias, cast, TYPE_CHECKING\nif TYPE_CHECKING:\n    import jwt')
text = text.replace('        options=cast(Any, options),', '        options=cast(Any, options),')
p.write_text(text)
