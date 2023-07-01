import unittest
import cv2
import shutil
import numpy as np

from dowell_qrcode.image import Image


class TestImage(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.face_image = Image('./tests/fixtures/face.jpg')
        cls.noface_image = Image('./tests/fixtures/no-face.jpg')

    @classmethod
    def tearDownClass(cls) -> None:
        # delete all files saved/resulting from testing
        try:
            shutil.rmtree('./tests/results/')
        except:
            pass
        del cls.face_image
        del cls.noface_image

    def test_attributes(self):
        # ensure that all attributes are of the correct type
        self.assertIsInstance(self.face_image.path, str)
        self.assertIsInstance(self.face_image.data, (cv2.Mat, np.ndarray))
        self.assertIsInstance(self.face_image.bytes, bytes)
        self.assertIsInstance(self.face_image.name, str)
        self.assertIsInstance(self.face_image.size, tuple)
        self.assertIsInstance(self.face_image.shape, tuple)
        self.assertIsInstance(self.face_image.width, int)
        self.assertIsInstance(self.face_image.height, int)
        self.assertIsInstance(self.face_image.channels, int)
        self.assertIsInstance(self.face_image.format, str)
        self.assertIsInstance(self.face_image.gray, (cv2.Mat, np.ndarray))
        self.assertIsInstance(self.face_image.eqgray, (cv2.Mat, np.ndarray))
        self.assertIsInstance(self.face_image.binary, (cv2.Mat, np.ndarray))
        self.assertIsInstance(self.face_image.binary_inv, (cv2.Mat, np.ndarray))
        self.assertIsInstance(self.face_image.is_grayscale, bool)
        self.assertIsInstance(self.face_image.is_binary, bool)
        self.assertIsInstance(self.face_image.is_color, bool)
        self.assertIsInstance(self.face_image.is_valid, bool)
        self.assertIsInstance(self.face_image.is_empty, bool)
        self.assertIsInstance(self.face_image.is_valid_binary, bool)
        self.assertIsInstance(self.face_image.is_valid_grayscale, bool)
        self.assertIsInstance(self.face_image.is_valid_color, bool)
        self.assertIsInstance(self.face_image.has_faces, bool)
        self.assertIsInstance(self.face_image.face_count, int)

        # test setting data and path attributes
        # self.face_image.data = cv2.imread('./tests/fixtures/face.jpg')
        self.face_image.path = './tests/fixtures/face.jpg'
        # self.assertIsInstance(self.face_image.data, (cv2.Mat, np.ndarray))
        self.assertIsInstance(self.face_image.path, str)
        with self.assertRaises(TypeError):
            # try passing invalid types for data and path
            self.face_image.data = './tests/fixtures/face.jpg'
            self.face_image.path = cv2.imread('./tests/fixtures/face.jpg')
        with self.assertRaises(ValueError):
            self.face_image.path = './tests/fixtures/face'
            self.face_image.path = './tests/fixtures/face.svg'

        # test that face detection works
        self.assertTrue(self.face_image.has_faces)
        self.assertTrue(self.face_image.face_count > 0)
        self.assertFalse(self.noface_image.has_faces)
        self.assertEqual(self.noface_image.face_count, 0)

        # Check that image format is correct
        self.assertTrue(self.face_image.format == 'jpg')
        self.assertTrue(self.noface_image.format == 'jpg')


    def test_rotate(self):
        try:
            self.face_image.rotate(90)
            self.face_image.rotate(180)
            self.face_image.rotate(270)
            self.face_image.rotate(360)
            self.face_image.rotate(450)
            self.face_image.rotate(540)
        except Exception as e:
            self.fail(e)

    
    def test_resize(self):
        try:
            self.noface_image.resize(width=800, height=600)
            self.assertTrue(self.noface_image.width == 800 and self.noface_image.height == 600)
            self.noface_image.resize(width=600)
            self.assertTrue(self.noface_image.width == 600)
            self.noface_image.resize(height=400)
            self.assertTrue(self.noface_image.height == 400)
        except Exception as e:
            self.fail(e)

    
    def test_crop(self):
        try:
            self.noface_image.crop(x_top_left=0, y_top_left=0, width=800, height=400)
            pass
        except Exception as e:
            self.fail(e)

    
    def test_flip(self):
        try:
            self.noface_image.flip(0)
            self.noface_image.flip(1)
            self.noface_image.flip(-1)
        except Exception as e:
            self.fail(e)


    # def test_grayscale(self):
    #     try:
    #         self.noface_image.grayscale()
    #         self.assertTrue(self.noface_image.is_grayscale)
    #     except Exception as e:
    #         self.fail(e)

    
    def test_makebinary(self):
        try:
            self.noface_image.makebinary()
            self.assertTrue(self.noface_image.makebinary(invert=True))
            self.assertTrue(self.noface_image.is_binary)
        except Exception as e:
            self.fail(e)

    
    def test_find_faces(self):
        try:
            coordinates = self.face_image.find_faces()
            self.assertIsInstance(coordinates, np.ndarray)
            self.assertTrue(len(coordinates) > 0)
        except Exception as e:
            self.fail(e)

    
    def test_markout_faces(self):
        try:
            face_coordinates = self.face_image.find_faces()
            self.face_image.markout_faces(face_coordinates=face_coordinates)
        except Exception as e:
            self.fail(e)


    def test_save(self):
        try:
            # test saving with quality reduction
            self.face_image.save('./tests/results/face.jpg', quality=80)
            # test saving without quality reduction
            self.noface_image.save('./tests/results/no-face.jpg')
        except Exception as e:
            self.fail(e)
        


if __name__ == "__main__":
    unittest.main()

# RUN WITH 'python -m unittest discover tests "test_*.py"' from project directory

