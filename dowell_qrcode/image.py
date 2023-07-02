"""
Contains custom image object that allows for face detection and other modifications using OpenCV
"""

from typing import List, Tuple
import cv2
import os
import numpy as np


ALLOWED_IMAGE_FORMATS = ('.png', '.jpeg', '.jpg', '.bmp', '.tiff', '.tif', '.gif', '.pbm', '.pgm', '.ppm', '.webp')


def check_image_ok(path: str):
    """
    Verifies that the path provided point to a valid image file

    :param path (str): path to image file

    :raises ValueError: if path provided is invalid
    :return: absolute path to image file
    """
    if not isinstance(path, str):
        raise TypeError("Invalid type for path. Path must be a string")

    _, extension = os.path.splitext(path)
    if not extension:
        raise ValueError("Invalid path provided. No extension found")
    if extension.lower() not in ALLOWED_IMAGE_FORMATS:
        raise ValueError(f"Invalid image format. Allowed formats are {ALLOWED_IMAGE_FORMATS}")

    if not os.path.exists(path):
        raise ValueError('Invalid path provided. Path does not exist')
    return os.path.abspath(path)
        
        
class Image:
    """Custom image object that allows for face detection and other modifications using OpenCV"""

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def __init__(self, path: str):
        """
        Initialize Image object

        :param path (str): path to image file
        """
        self._path = check_image_ok(path)
        self._data = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)

    def __str__(self) -> str:
        return f"Image(path={self.path})"

    def __repr__(self):
        return self.data

    @property
    def path(self):
        """Image file path"""
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = check_image_ok(value)

    @property
    def name(self):
        """Image file name"""
        return self.path.replace('\\', '/').split('/')[-1]

    @property
    def format(self):
        """Image file format"""
        return os.path.splitext(self.path)[1].removeprefix('.').lower()

    @property
    def data(self):
        """Image data in numpy array"""
        return self._data

    @data.setter
    def data(self, value: cv2.Mat | np.ndarray):
        if not isinstance(value, (cv2.Mat, np.ndarray)):
            raise TypeError("Invalid type for data")
        self._data = value

    @property
    def bytes(self) -> bytes:
        """Image data as bytes"""
        success, buffer = cv2.imencode(f'.{self.format}', self.data)
        if success is True:
            return buffer.tobytes()
        else:
            raise Exception('Image could not be encoded')
        
    @property
    def gray(self):
        """
        Image data in grayscale. If image is already grayscale, image data is returned as is.
        If the image is in color, it is converted to grayscale but if it is in binary, binary is still returned.
        Binary cannot be converted to grayscale.
        """
        if self.channels < 3:
            return self.data

        elif self.channels == 3:
            return cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        
        elif self.channels > 3:
            return cv2.cvtColor(self.data, cv2.COLOR_BGRA2GRAY)

        else:
            raise Exception(f'Invalid number of channels -> {self.channels}. Cannot convert to grayscale')

    @property
    def eqgray(self):
        "Equalized image data in grayscale"
        return cv2.equalizeHist(self.gray)

    @property
    def binary(self):
        """Image data in binary"""
        return cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY)[1]

    @property
    def binary_inv(self):
        """Image data in binary inverted"""
        return cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

    @property
    def shape(self):
        """Shape of image. A tuple of (height, width, channels)."""
        return self.data.shape

    @property
    def height(self):
        """Height of image"""
        return int(self.data.shape[0])
    
    @property
    def width(self):
        """Width of image"""
        return int(self.data.shape[1])

    @property
    def area(self):
        """Area of image"""
        return self.width * self.height
    
    @property
    def aspect_ratio(self):
        """Aspect ratio of image"""
        return self.width // self.height

    @property
    def size(self):
        """Size of image as tuple (width, height)"""
        return self.width, self.height

    @property
    def channels(self):
        """
        Number of channels in image
        
        For color images, channels are typically Red, Green, and Blue (RGB) or Blue, Green, Red, and Alpha (BGRA).
        color images have 3 or 4 channels. Grayscale images have 1 channel. Binary images have 1.1 channels(just to distinguish from grayscale), although
        binary images are technically grayscale images with only two colors (black and white) and have 1 channel.
        """
        try:
            return self.data.shape[2]
        except IndexError:
            # if data.shape is just (height, width) then image data has less than two channels
            unique_colors = np.unique(self.data)
            if len(unique_colors) == 2 and [0, 255] in unique_colors: # that is only black and white
                return 1.1 # Although binary images have 1 channel, we return 1.1 to differentiate from grayscale
            return 1

    @property
    def is_grayscale(self):
        """Check if image is grayscale"""
        return self.channels == 1

    @property
    def is_color(self):
        """Check if image is color"""
        return self.channels >= 3

    @property
    def is_binary(self):
        """Check if image is binary"""
        return self.channels == 1.1

    @property
    def is_empty(self):
        """Check if image is empty"""
        return self.data.size == 0

    @property
    def is_valid(self):
        """Check if image is valid"""
        return not self.is_empty

    @property
    def is_valid_grayscale(self):
        """Check if image is valid grayscale"""
        return self.is_valid and self.is_grayscale
    
    @property
    def is_valid_color(self):
        """Check if image is valid color"""
        return self.is_valid and self.is_color

    @property
    def is_valid_binary(self):
        """Check if image is valid binary"""
        return self.is_valid and self.is_binary


    def resize(self, width: int = None, height: int = None, interpolation: int = cv2.INTER_AREA):
        """
        Resize image. Aspect ratio is maintained if only one of width or height is provided.
        
        :param width (int): width of resized image
        :param height (int): height of resized image
        :param interpolation (int): interpolation method to use

        >>> img = Image('path/to/image.jpg')
        >>> img.resize(width=500)
        >>> assert img.width == 500
        """
        if width is None and height is None:
            raise ValueError("Either width or height must be provided")

        if width is None:
            width = int(height / self.aspect_ratio)
        elif height is None:
            height = int(width / self.aspect_ratio)
        self.data = cv2.resize(self.data, dsize=(width, height), interpolation=interpolation)
        return None


    def rotate(self, angle: int, center: tuple = None, scale: float = 1.0):
        """
        Rotate image
        
        :param angle (int): angle of rotation. Positive values mean clockwise rotation and negative values mean counter clockwise rotation.
        :param center (tuple): center of rotation. `center` will serve as the pivot point for the rotation. Default is center of image.
        :param scale (float): Optional parameter to adjust the scale of the image during rotation. Default is 1.0.

        >>> img = Image('path/to/image.jpg')
        >>> img.rotate(90) # rotate image 90 degrees clockwise
        >>> img.rotate(-90) # rotate image 90 degrees counter clockwise
        """
        if center is None:
            center = (self.width / 2, self.height / 2)
        matrix = cv2.getRotationMatrix2D(center, angle, scale)
        self.data = cv2.warpAffine(self.data, matrix, dsize=(self.width, self.height))
        return None


    def flip(self, direction: int):
        """
        Flip image
        
        :param direction (int): direction of flip
         
        * For normal vertical flipping (flipping upside-down) use integer 0.
        * For horizontal flipping (flipping side-ways) use integers greater than 0.
        * For simultaneous vertical and horizontal flipping use integers less than 0.

        >>> img = Image('path/to/image.jpg')
        >>> img.flip(0) # flip image upside-down
        >>> img.flip(1) # flip image side-ways
        >>> img.flip(-1) # flip image upside-down and side-ways
        """
        self.data = cv2.flip(self.data, direction)
        return None


    def crop(self, x_top_left: int, y_top_left: int, width: int, height: int, resize: bool = True):
        """
        Crop image
        
        :param x_top_left (int): x coordinate of top left corner of crop of the region of interest
        :param y_top_left (int): y coordinate of top left corner of crop of the region of interest
        :param width (int): width of crop
        :param height (int): height of crop
        :param resize (bool): whether to resize the cropped image to original image size. Default is True.

        >>> img = Image('path/to/image.jpg')
        >>> x_top_left, y_top_left = 100, 500
        >>> img.crop(x_top_left, y_top_left, width=200, height=100) # crop image from top left corner with width 200 and height 100
        """
        cropped_data = self.data[y_top_left:y_top_left + height, x_top_left:x_top_left + width].copy()
        if resize is True:
            self.data = cv2.resize(cropped_data, dsize=(self.width, self.height), interpolation=cv2.INTER_AREA)
        else:
            self.data = cropped_data
        return None


    def grayscale(self, equalize: bool = False):
        """
        Convert color image to grayscale
        
        :param equalize (bool): whether to equalize the histogram of the grayscale image.
        """
        if equalize is True:
            self.data = self.eqgray
        else:
            self.data = self.gray
        return None


    def makebinary(self, invert: bool = False):
        """
        Convert image to binary (black and white)
        
        :param invert (bool): whether to invert binary code
        """
        if invert is True:
            self.data = self.binary_inv
        else:
            self.data = self.binary
        return None


    def show(self):
        """Display image in a window"""
        cv2.imshow(self.path, self.data)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def draw_rectangle(self, x_top_left: int, y_top_left: int, width: int, height: int, rgb: tuple = (255, 0, 0), thickness: int = 2):
        """
        Draw rectangle on image
        
        :param x_top_left (int): x coordinate of top left corner of rectangle on image
        :param y_top_left (int): y coordinate of top left corner of rectangle on image
        :param width (int): width of rectangle
        :param height (int): height of rectangle
        :param rgb (tuple): color of rectangle
        :param thickness (int): thickness of rectangle
        """
        cv2.rectangle(self.data, pt1=(x_top_left, y_top_left), pt2=(x_top_left + width, y_top_left + height), color=rgb, thickness=thickness)


    def find_faces(self, scale_factor: float = 1.1, min_neighbors: int = 5, min_size: tuple = (30, 30)) -> np.ndarray:
        """
        Looks for human faces in image and returns coordinates of faces found

        :param scale_factor (float): adjusts the image scale factor. A smaller scale factor, such as 1.1, will result in more image pyramid levels and more precise face detection, 
        but it may also increase the processing time. A larger scale factor, such as 1.5, will have fewer pyramid levels and may lead to faster but potentially less accurate detection.
        :param min_neighbors (int): specifies the minimum number of neighbors required for a region to be considered a face
        :param min_size (tuple): specifies the minimum number of neighbors required for a region to be considered a face     
        :return: list of tuples containing coordinates of faces found if any
        """
        face_coordinates = self.face_cascade.detectMultiScale(
                                                                self.gray, scaleFactor=scale_factor, 
                                                                minNeighbors=min_neighbors, minSize=min_size
                                                                )
        return face_coordinates


    @property
    def has_faces(self):
        """Returns True if image has human faces"""
        return self.face_count > 0
    
    @property
    def face_count(self):
        """Number of human faces in image"""
        return len(self.find_faces())


    def markout_faces(self, face_coordinates: List[Tuple[int, int, int, int]], color: tuple = (0, 255, 0)):
        """
        Mark out human faces found in image

        :param face_coordinates (list): list of tuples containing coordinates of faces found
        :param color (tuple): tuple of rgb color code in format (R, G, B) to be used to mark-out faces in image.
        """
        for (x, y, w, h) in face_coordinates:
            self.draw_rectangle(x, y, w, h, rgb=color)
        return None


    @property
    def compression_algo(self):
        """Algorithm to be used in image compression"""
        match self.format:
            case 'jpeg':
                return cv2.IMWRITE_JPEG_QUALITY
            case 'jpg':
                return cv2.IMWRITE_JPEG_QUALITY
            case 'png':
                return cv2.IMWRITE_PNG_COMPRESSION
            case 'tiff':
                return cv2.IMWRITE_TIFF_COMPRESSION
            case 'tif':
                return cv2.IMWRITE_TIFF_COMPRESSION
            case 'webp':
                return cv2.IMWRITE_WEBP_QUALITY
        return None


    def save(self, path: str = None, quality: int = 100):
        """
        Save image to path in disk
        
        :param path (str): path to save image to (defaults to path image was read from)
        :param quality (int): quality of image to save (defaults to 100)
        """
        if not isinstance(quality, int):
            raise TypeError('quality should be an integer')
        if quality < 10 or quality > 100:
            raise ValueError('quality should be an integer between 10 and 100')
        
        if quality < 100:
            if self.format in ['jpeg', 'jpg', 'webp']:
                return cv2.imwrite(path or self.path, self.data, [self.compression_algo, quality])

            elif self.format == 'png':
                return cv2.imwrite(path or self.path, self.data, [self.compression_algo, quality // 10])

            elif self.format in ['tiff', 'tif']:
                return cv2.imwrite(path or self.path, self.data, [self.compression_algo, round(quality / 100)])
            
        return cv2.imwrite(path or self.path, self.data)

