"""Chaos tests for Web Bridge edge cases."""

from taipanstack.bridges.web_bridge import SecurityHeadersConfig, result_to_response
from taipanstack.core.result import Err, Ok


def test_chaos_web_bridge_result_to_response_extreme_status_expected_standard_expected() -> (
    None
):
    """Test result_to_response with extreme HTTP status codes."""
    res1 = result_to_response(Ok("data"), status_ok=999)
    assert res1["status"] == 999

    res2 = result_to_response(Err(ValueError("bad")), status_err=-1)
    assert res2["status"] == -1


def test_chaos_web_bridge_security_headers_extreme_config_expected_standard_expected() -> (
    None
):
    """Test SecurityHeadersConfig with extreme length values."""
    massive_string = "A" * 10000
    config = SecurityHeadersConfig(x_frame_options=massive_string)
    headers = dict(config.to_headers())
    assert headers[b"x-frame-options"] == massive_string.encode()
