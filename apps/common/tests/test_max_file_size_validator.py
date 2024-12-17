from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.common.validators import MaxFileSizeValidator


class TestMaxFileSizeValidator(TestCase):
    def setUp(self):
        super().setUp()
        self.max_size_kb = 100  # 100 KB
        self.validator = MaxFileSizeValidator(max_size_kb=self.max_size_kb)

    def test_file_within_limit(self):
        file = SimpleUploadedFile(
            name="test_file.txt",
            content=b"file_content" * 10,  # 100 bytes
        )
        try:
            self.validator(file)
        except ValidationError:
            self.fail(
                "MaxFileSizeValidator raised ValidationError "
                "unexpectedly for a valid file size."
            )

    def test_file_exceeds_limit(self):
        file = SimpleUploadedFile(
            name="test_file.txt",
            content=b"file_content" * 10240,  # 102400 bytes (100 KB)
        )
        with self.assertRaises(ValidationError):
            self.validator(file)
