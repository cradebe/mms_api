import unittest
import io
from unittest import mock

import pytest as pytest
from freezegun import freeze_time
from werkzeug.datastructures import FileStorage

from app import upload


@pytest.fixture()
def image_upload_data():
    """Fixture that returns a static image data."""
    with io.open('resources/testdata/test_pond.jpg', 'rb') as file:
        image = FileStorage(filename='test', content_type='image/jpg', stream=io.BytesIO(file.read()))
        image.filename = 'test'
        image.save('resources/testdata/output_test_pond.jpg')
    return image


class TestAPI:
    @freeze_time('2022-10-01')
    @mock.patch('app.request')
    def test_upload_success(self, request_mock, image_upload_data):
        request_mock.files.return_value = image_upload_data
        response = {'imageId': 1, 'imageUrl': 'test/url/', 'imageName': ''}
        assert upload() == response

    def test_upload_no_image(self):
        pass

    def test_image_upload_fail(self):
        pass


if __name__ == '__main__':
    unittest.main()
