import pytest

import test.test_sqs_messages
import test.test_s3_files


def test_wipe_all():
    test.test_sqs_messages.test_consume_all_messages()
    test.test_s3_files.test_s3_delete_all_objects()
