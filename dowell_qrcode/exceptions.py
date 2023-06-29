
class QRCodeGenerationError(Exception):
    """Raised when an error occurs during QR Code generation"""


class QRCodeUpdateError(Exception):
    """Raised when an error occurs during QR Code update"""


class QRCodeNotFoundError(Exception):
    """Raised when a QR Code is not found"""


class QRCodeRetrievalError(Exception):
    """Raised when an error occurs during QR Code retrieval"""


class NotSupportedError(Exception):
    """Raised when a feature is not supported"""


class NoFaceDetected(Exception):
    """Raised when a face cannot be found in an Image object"""

