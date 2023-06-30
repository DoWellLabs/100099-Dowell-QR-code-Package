"""Module exceptions."""

class ClientError(Exception):
    """Raised when an error occurs during API request"""

class QRCodeGenerationError(ClientError):
    """Raised when an error occurs during QR Code generation"""


class QRCodeUpdateError(ClientError):
    """Raised when an error occurs during QR Code update"""


class QRCodeNotFoundError(ClientError):
    """Raised when a QR Code is not found"""


class QRCodeRetrievalError(ClientError):
    """Raised when an error occurs during QR Code retrieval"""


class NotSupportedError(Exception):
    """Raised when a feature is not supported"""


class NoFaceDetected(Exception):
    """Raised when a face cannot be found in an Image object"""

