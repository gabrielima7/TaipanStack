from src.taipanstack.utils.logging import mask_sensitive_data_processor


def test_coverage():
    from src.taipanstack.utils import logging as my_logging

    # Temporarily set regex to None to hit the branch
    old_regex = my_logging._SENSITIVE_KEY_REGEX
    my_logging._SENSITIVE_KEY_REGEX = None

    try:
        res = mask_sensitive_data_processor(None, None, {"test": "val"})
        assert res == {"test": "val"}

        # Hitting _is_sensitive(key, None)
        assert my_logging._is_sensitive("any", None) is False
    finally:
        my_logging._SENSITIVE_KEY_REGEX = old_regex


if __name__ == "__main__":
    test_coverage()
