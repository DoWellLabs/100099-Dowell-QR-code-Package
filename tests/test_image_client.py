import unittest
import shutil

from dowell_qrcode.image_client import ImageClient
from dowell_qrcode.image import Image
from tests.test_client import TestClient
from dowell_qrcode.exceptions import *


class TestImageClient(TestClient, unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = ImageClient(username=cls.client_name, user_id=cls.client_id)
        assert cls.client.username == cls.client_name
        assert cls.client.user_id == cls.client_id


    def test_generate_qrcode(self):
        try:
            face_image = Image('./tests/fixtures/face.jpg')
            noface_image = Image('./tests/fixtures/no-face.jpg')

            with self.assertRaises(NotSupportedError):
                # try generating unsupported QR code type
                resp = self.client.generate_qrcode(image=face_image, qrcode_type='test')
            
            with self.assertRaises(NoFaceDetected):
                # try generating QR code for image with no face in it
                resp = self.client.generate_qrcode(image=noface_image)

            resp = self.client.generate_qrcode(image='./tests/fixtures/face.jpg', verbose=False)

            resp = self.client.generate_qrcode(image=face_image, verbose=False)
            self.assertIsInstance(resp, tuple)

            kwargs = {
                'description': 'Image QR code',
                'qrcode_color': '#00ff23',
                'logo_size': 30,
                'quality': 2,
            }
            resp = self.client.generate_qrcode(image=face_image, verbose=True, **kwargs)
            self.assertIsInstance(resp, list)
            for i in resp:
                self.assertIsInstance(i, dict)
                self.assertTrue(i['description'] == "Image QR code")
                self.assertTrue(i['qrcode_color'] == "#00ff23")
                self.assertTrue(i['logo_size'] == 30)

        except QRCodeGenerationError as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()

# RUN WITH 'python -m unittest discover tests "test_*.py"' from project directory 