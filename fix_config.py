import re

with open("src/taipanstack/resilience/watchdogs/config_watcher.py", "r") as f:
    content = f.read()

content = content.replace("from typing import Any", "from typing import Any, TypeVar")

content = content.replace("class ConfigWatcher(BaseWatcher):", "TModel = TypeVar(\"TModel\", bound=BaseModel)\n\nclass ConfigWatcher(BaseWatcher, Generic[TModel]):")
content = content.replace("from typing import Any, TypeVar", "from typing import Any, Generic, TypeVar")
content = content.replace("config_model: type[BaseModel]", "config_model: type[TModel]")
content = content.replace("def _validate_and_apply(self, path: Path) -> Result[BaseModel, Exception]:", "def _validate_and_apply(self, path: Path) -> Result[TModel, Exception]:")
content = content.replace("Callable[[BaseModel], None]", "Callable[[TModel], None]")

content = content.replace("def validate_config(\n    data: dict[str, Any],\n    model: type[BaseModel],\n) -> Result[BaseModel, Exception]:", "def validate_config(\n    data: dict[str, Any],\n    model: type[TModel],\n) -> Result[TModel, Exception]:")

with open("src/taipanstack/resilience/watchdogs/config_watcher.py", "w") as f:
    f.write(content)
