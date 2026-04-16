from src.taipanstack.utils.logging import mask_sensitive_data_processor


def test_v034_logging_coverage_coverage_expected():
    from src.taipanstack.utils import logging as my_logging

    old_regex = my_logging._SENSITIVE_KEY_REGEX
    my_logging._SENSITIVE_KEY_REGEX = None
    try:
        res = mask_sensitive_data_processor(None, None, {"test": "val"})
        assert res == {"test": "val"}
        assert my_logging._is_sensitive("any", None) is False
    finally:
        my_logging._SENSITIVE_KEY_REGEX = old_regex


if __name__ == "__main__":
    test_v034_logging_coverage_coverage_expected()
