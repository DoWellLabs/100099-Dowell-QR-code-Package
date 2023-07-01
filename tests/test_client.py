import unittest
import shutil

from dowell_qrcode.client import Client
from dowell_qrcode.exceptions import *


class TestClient(unittest.TestCase):

    client_name = 'TestUser'
    client_id = 'TestUserID'

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client(username=cls.client_name, user_id=cls.client_id)
        assert cls.client.username == cls.client_name
        assert cls.client.user_id == cls.client_id


    @classmethod
    def tearDownClass(cls) -> None:
        # delete all files saved/resulting from testing
        try:
            shutil.rmtree('./tests/results/')
        except:
            pass
        cls.client.endsession()
        del cls.client


    def test_get_status(self):
        status = self.client.get_status()
        assert status['status_code'] == 200


    def test_get_qrcodes(self):
        try:
            qrcodes = self.client.get_qrcodes()
            self.assertIsInstance(qrcodes, list)
            self.assertIsInstance(qrcodes[0], dict)
        except QRCodeRetrievalError as e:
            self.fail(e)


    def test_get_qrcode(self):
        try:
            with self.assertRaises(QRCodeNotFoundError):
                qrcode = self.client.get_qrcode('5578252259716846')
        
            qrcode = self.client.get_qrcode('13755485505829016046', verbose=True)
            self.assertIsInstance(qrcode, dict)

            qrcode = self.client.get_qrcode('13755485505829016046', verbose=False)
            self.assertIsInstance(qrcode, str)
        except QRCodeRetrievalError as e:
            self.fail(e)


    def test_update_qrcode(self):
        with self.assertRaises(QRCodeUpdateError):
            # try updating QR code that doesn't exist
            resp = self.client.update_qrcode('13755485505829', data={'qrcode_color': "#00ff23"}, verbose=True)

        try:
            resp = self.client.update_qrcode('13755485505829016046', data={'qrcode_color': "#00ff23"}, verbose=True)
            self.assertIsInstance(resp, dict)

            resp = self.client.update_qrcode('13755485505829016046', data={'qrcode_color': "#00ff23"}, verbose=False)
            self.assertIsInstance(resp, str)
        except QRCodeUpdateError as e:
            self.fail(e)
        

    def test_generate_qrcode(self):
        try:
            with self.assertRaises(NotSupportedError):
                # try generating unsupported QR code type
                resp = self.client.generate_qrcode('https://www.google.com', qrcode_type='test')

            resp = self.client.generate_qrcode('https://www.google.com', product_name='Google Link', verbose=False)
            self.assertIsInstance(resp, tuple)
            
            kwargs = {
                'logo': './tests/fixtures/test-logo.jpg',
                'description': 'Google Link',
                'qrcode_color': '#00ff23',
                'logo_size': 30,
                'quality': 2,
            }
            resp = self.client.generate_qrcode('https://www.google.com', verbose=True, **kwargs)
            self.assertIsInstance(resp, list)
            for i in resp:
                self.assertIsInstance(i, dict)
                self.assertTrue(i['link'] == 'https://www.google.com')
                self.assertTrue(i['description'] == 'Google Link')
                self.assertTrue(i['qrcode_color'] == '#00ff23')
                self.assertTrue(i['logo_size'] == 30)

        except QRCodeGenerationError as e:
            self.fail(e)


    def test_deactivate_qrcode(self):
        try:
            self.client.deactivate_qrcode('13755485505829016046')
        except ClientError as e:
            self.fail(e)


    def test_activate_qrcode(self):
        try:
            self.client.activate_qrcode('13755485505829016046')
        except ClientError as e:
            self.fail(e)


    def test_download_qrcode_image(self):
        try:
            url = self.client.get_qrcode('13755485505829016046')
            file_hdl = self.client.download_qrcode_image(url, save_to='./tests/results/')
            file_hdl.close_file()
        except ClientError as e:
            self.fail(e)



if __name__ == "__main__":
    unittest.main()

# RUN WITH 'python -m unittest discover tests "test_*.py"' from project directory
