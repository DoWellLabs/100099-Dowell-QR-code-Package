"""
Python Client for Dowell QR Code Generation API.

For more information or to report issues, visit the `GitHub page` at https://github.com/DoWellLabs/100099-Dowell-QR-code-Package/
"""


from .exceptions import *
from .client import Client
from .image_client import ImageClient
from .image import Image

api_version = 'v2'
__version__ = "0.2.0"

def get_api_status():
    """Get the status of Dowell QR Code Generator API"""
    return Client.get_status()

__all__ = [
    "__version__",
    "Image",
    "Client",
    "ImageClient",
]