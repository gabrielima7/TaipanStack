"""Tests for the _imports lazy import helpers."""
import types

from taipanstack.bridges._imports import get_attr_or_err, require_dependency
from taipanstack.core.result import Err, Ok


class TestRequireDependency:
    """Tests for require_dependency."""

    def test_bridge_imports_existing_module_expected(self) -> None:
        """Returns Ok for installed modules."""
        result = require_dependency("json")
        assert isinstance(result, Ok)
        assert isinstance(result.ok_value, types.ModuleType)

    def test_missing_module_default_hint_expected(self) -> None:
        """Returns Err with install hint for missing module."""
        result = require_dependency("not_a_real_module_xyz")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ImportError)
        assert "pip install not_a_real_module_xyz" in str(result.err_value)

    def test_missing_module_with_extra_expected(self) -> None:
        """Returns Err with pip extra install hint."""
        result = require_dependency("not_a_real_module_xyz", pip_extra="bridges-http")
        assert isinstance(result, Err)
        assert "pip install taipanstack[bridges-http]" in str(result.err_value)

class TestGetAttrOrErr:
    """Tests for get_attr_or_err."""

    def test_bridge_imports_existing_attr_expected(self) -> None:
        """Returns Ok for existing attributes."""
        import json
        result = get_attr_or_err(json, "dumps")
        assert isinstance(result, Ok)
        assert result.ok_value is json.dumps

    def test_bridge_imports_missing_attr_expected(self) -> None:
        """Returns Err for missing attributes."""
        import json
        result = get_attr_or_err(json, "nonexistent_attr_xyz")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, AttributeError)
