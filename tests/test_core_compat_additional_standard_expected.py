from unittest.mock import patch


def test_core_compat_additional_core_compat_check_jit_available_attribute_error_standard_expected():
    from taipanstack.core.compat import _check_jit_available

    class MockFlags:
        @property
        def __class__(self):
            raise AttributeError("mocked")

    with patch(
        "taipanstack.core.compat.sys", type("MockSys", (), {"flags": MockFlags()})
    ):
        assert _check_jit_available() is False


def test_core_compat_additional_core_compat_check_free_threading_available_type_error_standard_expected():
    from taipanstack.core.compat import (
        _check_free_threading_available,
        _check_nogil_flag,
    )

    class MockSys:
        @property
        def flags(self):
            raise TypeError("mocked")

    with patch("taipanstack.core.compat.sys", MockSys()):
        assert _check_nogil_flag() is None
        assert _check_free_threading_available() is False


def test_core_compat_additional_core_compat_check_free_threading_available_config_vars_error_standard_expected():
    from taipanstack.core.compat import (
        _check_disable_gil_config,
        _check_free_threading_available,
    )

    class MockSysNoFlags:
        def __init__(self):
            self.name = "MockSysNoFlags"

    with patch("taipanstack.core.compat.sys", MockSysNoFlags()):
        with patch(
            "taipanstack.core.compat.sysconfig.get_config_var",
            side_effect=TypeError("mocked"),
        ):
            assert _check_disable_gil_config() is False
            assert _check_free_threading_available() is False


def test_core_compat_additional_core_compat_check_nogil_flag_true_standard_expected():
    from taipanstack.core.compat import _check_nogil_flag

    class MockSysTrue:
        class Flags:
            nogil = True

        flags = Flags()

    with patch("taipanstack.core.compat.sys", MockSysTrue()):
        assert _check_nogil_flag() is True


def test_core_compat_additional_core_compat_check_nogil_flag_false_standard_expected():
    from taipanstack.core.compat import _check_nogil_flag

    class MockSysFalse:
        class Flags:
            nogil = False

        flags = Flags()

    with patch("taipanstack.core.compat.sys", MockSysFalse()):
        assert _check_nogil_flag() is False


def test_core_compat_additional_core_compat_check_nogil_flag_none_standard_expected():
    from taipanstack.core.compat import _check_nogil_flag

    class MockSysNone:
        class Flags:
            """Mock flags."""

        flags = Flags()

    with patch("taipanstack.core.compat.sys", MockSysNone()):
        assert _check_nogil_flag() is None


def test_core_compat_additional_core_compat_check_free_threading_available_true_standard_expected():
    from taipanstack.core.compat import _check_free_threading_available

    with patch("taipanstack.core.compat.PY313", True):
        with patch("taipanstack.core.compat._check_nogil_flag", return_value=True):
            assert _check_free_threading_available() is True


def test_core_compat_additional_core_compat_check_free_threading_available_false_when_nogil_false_standard_expected():
    from taipanstack.core.compat import _check_free_threading_available

    with patch("taipanstack.core.compat.PY313", True):
        with patch("taipanstack.core.compat._check_nogil_flag", return_value=False):
            # Even if config states gil is disabled, if flag exists and is False, it should return False
            with patch(
                "taipanstack.core.compat._check_disable_gil_config", return_value=True
            ):
                assert _check_free_threading_available() is False


def test_core_compat_additional_core_compat_check_mimalloc_available_error_standard_expected():
    from taipanstack.core.compat import _check_mimalloc_available

    with patch(
        "taipanstack.core.compat.sysconfig.get_config_var",
        side_effect=TypeError("mock"),
    ):
        assert _check_mimalloc_available() is False
