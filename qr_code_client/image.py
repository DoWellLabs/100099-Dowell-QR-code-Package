from typing import List, Tuple
import cv2
import os


ALLOWED_IMAGE_FORMATS = ('.png', '.jpeg', '.jpg', '.bmp', '.tiff', '.tif', '.gif', '.pbm', '.pgm', '.ppm', '.webp')


def check_image_ok(path: str):
    """
    Verifies that the path provided point to a valid image file

    :param path (str): path to image file

    :raises ValueError: if path provided is invalid
    :return: absolute path to image file
    """
    if not os.path.exists(path):
        raise ValueError('Invalid path provided. Path does not exist')
    _, extension = os.path.splitext(path)

    if not extension:
        raise ValueError("Invalid path provided. No extension found")
    if extension.lower() not in ALLOWED_IMAGE_FORMATS:
        raise ValueError(f"Invalid image format. Allowed formats are {ALLOWED_IMAGE_FORMATS}")
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
        return os.path.splitext(self.path)[1].removeprefix('.')

    @property
    def data(self):
        """Image data in numpy array"""
        return self._data

    @data.setter
    def data(self, value: cv2.Mat):
        if not isinstance(value, cv2.Mat):
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
        """Image data in grayscale"""
        if self.channels == 1:
            return self.data
        if self.channels == 3:
            return cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(self.data, cv2.COLOR_BGRA2GRAY)

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
        return self.data.shape[0]
    
    @property
    def width(self):
        """Width of image"""
        return self.data.shape[1]

    @property
    def size(self):
        """Size of image as tuple (width, height)"""
        return self.width, self.height

    @property
    def channels(self):
        """Number of channels in image"""
        return self.data.shape[2]

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
        return self.channels == 0

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
        Resize image
        
        :param width (int): width of resized image
        :param height (int): height of resized image
        :param interpolation (int): interpolation method to use
        """
        if width is None and height is None:
            raise ValueError("Either width or height must be provided")
        if width is None:
            ratio = height / self.height
            width = int(self.width * ratio)
        elif height is None:
            ratio = width / self.width
            height = int(self.height * ratio)
        self.data = cv2.resize(self.data, (width, height), interpolation=interpolation)

    def rotate(self, angle: int, center: tuple = None, scale: float = 1.0):
        """
        Rotate image
        
        :param angle (int): angle of rotation
        :param center (tuple): center of rotation
        :param scale (float): scale of rotation
        """
        if center is None:
            center = (self.width / 2, self.height / 2)
        matrix = cv2.getRotationMatrix2D(center, angle, scale)
        self.data = cv2.warpAffine(self.data, matrix, (self.width, self.height))

    def flip(self, direction: int):
        """
        Flip image
        
        :param direction (int): direction of flip
         
        * For normal vertical flipping (flipping upside-down) use integer 0.
        * For horizontal flipping (flipping side-ways) use integers greater than 0.
        * For simultaneous vertical and horizontal flipping use integers less than 0.
        """
        self.data = cv2.flip(self.data, direction)

    def crop(self, x_top_left: int, y_top_left: int, width: int, height: int):
        """
        Crop image
        
        :param x_top_left (int): x coordinate of top left corner of crop
        :param y_top_left (int): y coordinate of top left corner of crop
        :param width (int): width of crop
        :param height (int): height of crop
        """
        self.data = self.data[y_top_left:y_top_left + height, x_top_left:x_top_left + width]

    def grayscale(self, equalize: bool = False):
        """
        Convert image to grayscale
        
        :param equalize (bool): whether to equalize the histogram of the grayscale image.
        """
        if equalize is True:
            self.data = self.eqgray
        else:
            self.data = self.gray

    def makebinary(self, invert: bool = False):
        """
        Convert image to binary
        
        :param invert (bool): whether to invert binary code
        """
        if invert is True:
            self.data = self.binary_inv
        else:
            self.data = self.binary

    def show(self):
        """Display image"""
        cv2.imshow(self.path, self.data)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def draw_rectangle(self, x_top_left: int, y_top_left: int, width: int, height: int, rgb: tuple = (255, 0, 0)):
        """
        Draw rectangle on image
        
        :param x_top_left (int): x coordinate of top left corner of rectangle
        :param y_top_left (int): y coordinate of top left corner of rectangle
        :param width (int): width of rectangle
        :param height (int): height of rectangle
        :param rgb (tuple): color of rectangle
        """
        cv2.rectangle(self.data, (x_top_left, y_top_left), (x_top_left + width, y_top_left + height), rgb, 2)

    def find_faces(self, scale_factor: float = 1.1, min_neighbors: int = 5, min_size: tuple = (30, 30)):
        """
        Looks for human faces in image and returns coordinates of faces found

        :param scale_factor (float): adjusts the image scale factor
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

