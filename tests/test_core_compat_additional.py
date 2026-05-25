from unittest.mock import patch


def test_core_compat_additional_core_compat_check_jit_available_attribute_error():
    from taipanstack.core.compat import _check_jit_available

    class MockFlags:
        @property
        def __class__(self):
            raise AttributeError("mocked")

    with patch("taipanstack.core.compat.sys", type("MockSys", (), {"flags": MockFlags()})):
        assert _check_jit_available() is False

def test_core_compat_additional_core_compat_check_free_threading_available_type_error():
    from taipanstack.core.compat import _check_free_threading_available

    class MockSys:
        @property
        def flags(self):
            raise TypeError("mocked")

    with patch("taipanstack.core.compat.sys", MockSys()):
        assert _check_free_threading_available() is False

def test_core_compat_additional_core_compat_check_free_threading_available_config_vars_error():
    from taipanstack.core.compat import _check_free_threading_available
    class MockSysNoFlags:
        pass

    with patch("taipanstack.core.compat.sys", MockSysNoFlags()):
        with patch("sysconfig.get_config_var", side_effect=TypeError("mocked")):
            assert _check_free_threading_available() is False

def test_core_compat_additional_core_compat_check_mimalloc_available_error():
    from taipanstack.core.compat import _check_mimalloc_available
    with patch("sysconfig.get_config_var", side_effect=TypeError("mock")):
        assert _check_mimalloc_available() is False
