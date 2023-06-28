from typing import Dict, Any

from .exceptions import QRCodeGenerationError, NoFaceDetected
from .client import Client, api_get_url
from .image import Image



class ImageClient(Client):
    """Handles QR Code generation, update and retrieval for images using Dowell QR Code API"""


    def generate_qrcode(self, image: Image | str, image_name: str = None, qrcode_type: str = "Link", verbose: bool = False, **kwargs):
        """
        Generate QR Code for image in path provided
        
        :param image (Image | str): Image object for image file or path to image file to be converted to QR Code
        :param image_name (str): name of image file to be converted to QR Code. Defaults to the name of the image file in the path provided.
        You can pass in a custom name for the image file to be converted to QR Code.
        :param qrcode_type (str): type of QR Code to be generated (Leave as default for now)
        :param verbose (bool): if True, return the response object for th created QR code from the API
        :param kwargs: additional data to be sent to the API
            :kwarg quantity (int): number of QR Codes to be generated

            :kwarg logo_size (int): size of logo to be added to QR Code

            :kwarg qrcode_color (str): color of QR Code to be generated. Must be a valid hex color code. Use colors that have good contrast with white.

            :kwarg description (str): description of QR Code to be generated

        :return: a tuple of the QR Code image url and the QR Code id or a list of such tuples if quantity is greater than 1
        """
        if qrcode_type not in self.available_qrcode_types:
            raise ValueError(f"Invalid QR Code type. Available types are {self.available_qrcode_types}")

        if isinstance(image, str):
            image_path = image.strip().replace('\\', '/')
            image = Image(path=image_path)
        if not image.has_faces:
            raise NoFaceDetected("Error Generating QR Code: No face could be detected in the image")
            
        image_name = image.name if image_name is None else image_name
        data = {
            "product_name": image_name.split('.')[0],
            "qrcode_type": qrcode_type,
        }
        kwargs.update(data)

        # with open(image_path, 'rb') as f:
        files = [
            ('logo', (image_name, image.bytes, 'application/octet-stream'))
        ]
        payload = self._prepare_payload(kwargs)
        response = self.session_.post(api_get_url, data=payload, files=files)
        if response.ok:
            response_data = response.json()['qrcodes']
            response_data = self._correct_response_data(response_data)
            if verbose:
                return response_data

            if len(response_data) > 1:
                return [ self._handle_qrcode_generation_response_data(data) for data in response_data ]
            else:
                return self._handle_qrcode_generation_response_data(response_data[0])             
        else:
            raise QRCodeGenerationError(f"Error generating QR Code: {response.text}")


    def _handle_qrcode_generation_response_data(self, response_data: Dict[str, Any]):
        """
        Handle response data returned by the API after generating QR Code

        :param response_data (Dict[str, Any]): data returned by the API after generating QR Code
        :return: a tuple of the QR Code image url and the QR Code id
        """
        # Since the API does not support creating QR codes for images yet, we have to add the image as a logo to the QR code
        # and then update the QR code `link` field with the `logo_url` returned in the response from the API
        logo_url = response_data['logo_url']
        qrcode_id = response_data['qrcode_id']
        qrcode_image_url = self.update_qrcode(qrcode_id, qrcode_link=logo_url, data={})
        return qrcode_image_url, qrcode_id

