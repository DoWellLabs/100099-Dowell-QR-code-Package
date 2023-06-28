import requests
import random
from bs4_web_scraper.utils import generate_random_user_agents
from bs4_web_scraper import scraper
from typing import Dict, Any, List


from .exceptions import ( 
                            QRCodeGenerationError, QRCodeUpdateError, 
                            QRCodeNotFoundError, QRCodeRetrievalError, NotSupportedError,
                         )


api_base_url = 'https://100099.pythonanywhere.com/api/v2'
api_get_url = f"{api_base_url}/qr-code/"
api_put_url = f"{api_base_url}/update-qr-code/"
actual_image_url_base = "http://67.217.61.253/uploadfiles/qrcode-download"

ALLOWED_CREATE_FIELDS = {
    "quantity": int,
    "created_by": str,
    "company_id": str,
    "qrcode_type": str,
    "link": str,
    "product_name": str,
    "qrcode_color": str,
    "logo_size": int,
    "description": str,
    "is_active": bool,
}


ALLOWED_UPDATE_FIELDS = {
    "created_by": str,
    "company_id": str,
    "link": str,
    "qrcode_color": str,
    "logo_size": int,
    "product_name": str,
    "description": str,
    "is_active": bool,
}


def get_new_user_agent() -> str:
    """Get a new user agent and save it to config.json"""
    user_agent = random.choice(generate_random_user_agents())
    return user_agent



class Client:
    """Handles QR Code generation, update and retrieval using Dowell QR Code Generator API"""

    session_ = requests.Session()

    def __init__(self, username: str, user_id: str):
        """
        Initialize class

        :param username (str): username of the user. Should be unique
        :param user_id (str): user id of the user. Should be unique
        """
        self.username = username
        self.user_id = user_id
        user_agent = get_new_user_agent()
        self.session_.headers.update({'User-Agent': user_agent})


    @property
    def available_qrcode_types(self):
        """Return a tuple of available qrcode types"""
        return ('Link',)

    
    @staticmethod
    def _validate_payload(payload: Dict[str, Any], validate_with: Dict[str, Any] = ALLOWED_CREATE_FIELDS):
        """
        Validates data to be sent to the API
        
        :param payload (dict): data to be validated before being sent to the API
        :param validate_with (dict): dictionary of allowed fields and their types that will be used to validate the payload
        :return (bool): True if payload is valid, else False
        """
        for key, value in payload.items():
            if key not in validate_with.keys():
                raise KeyError(f"Invalid field {key}. Allowed fields are {validate_with.keys()}")
            if not isinstance(value, validate_with[key]):
                raise TypeError(f"Invalid type for field `{key}`. Expected {validate_with[key]} but got {type(value)}")
        return True


    def _prepare_payload(self, data: Dict[str, Any]):
        """
        Prepare data to be sent to the API
        
        :param data (dict): data to be sent to the API
        :return (dict): prepared and validated data to be sent to the API
        """

        payload = {
            "quantity": data.get('quantity', 1),
            "created_by": self.username,
            "company_id": self.user_id,
            "qrcode_type": data.get('qrcode_type', 'Link'),
            "link": data.get('link', 'https://google.com/'),
            "product_name": data.get('product_name', 'QR Code'),
            "qrcode_color": data.get('qrcode_color', '#000000'),
            "logo_size": data.get('logo_size', 20),
            "description": data.get('description', ''),
            "is_active": data.get('is_active', False),
        }
        try:
            self._validate_payload(payload, validate_with=ALLOWED_CREATE_FIELDS)
        except Exception as e:
            raise e                   
        return payload


    def generate_qrcode(self, obj: str | Any, product_name: str = None, qrcode_type: str = "Link", verbose: bool = False, **kwargs):
        """
        Generate QR Code for object of `qrcode_type`
        
        :param obj (str | Any): object for which QR Code is to be generated. If `qrcode_type` is `Link`, then `obj` should be a valid url.
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
        if qrcode_type != "Link":
            raise NotSupportedError(f"QR Code type {qrcode_type} is not supported yet")

        data = {
            "link": obj, 
            "product_name": product_name or '',
            "qrcode_type": qrcode_type,
        }
            
        files = []
        kwargs.update(data)
        logo_path: str = kwargs.pop('logo', None)
        if logo_path:
            logo_path = logo_path.strip().replace('\\', '/')
            logo_name = logo_path.split('/')[-1]
            f = open(logo_path, 'rb')
            files = [
                ('logo', (logo_name, f, 'application/octet-stream'))
            ]
        
        payload = self._prepare_payload(kwargs)
        response = self.session_.post(api_get_url, data=payload, files=files)
        if logo_path:
            f.close()

        if response.ok:
            response_data = response.json()['qrcodes']
            response_data = self._correct_response_data(response_data)
            if verbose is True:
                return response_data

            if len(response_data) > 1:
                return [ (data["qrcode_image_url"], data["qrcode_id"]) for data in response_data ]
            else:
                return (response_data["qrcode_image_url"], response_data["qrcode_id"])
        else:
            raise QRCodeGenerationError(f"Error generating QR Code: {response.text}")


    @staticmethod
    def _get_actual_image_url(image_url: str):
        """Return the actual image url from the image url returned by the API"""
        image_id = image_url.split('/')[-1]
        return f"{actual_image_url_base}/{image_id}"


    def _correct_response_data(self, response_data: List[Dict[str, Any]] | Dict[str, Any]):
        """
        Corrects image urls provided in the response data. The Dowell API returns the wrong image url of the QR Code.
        This method corrects that.

        :param response_data (List[Dict[str, Any]] | Dict[str, Any]): response data to be corrected
        :return (List[Dict[str, Any]] | Dict[str, Any]): corrected response data
        """
        if isinstance(response_data, dict):
            for item, value in response_data.items():
                if item.endswith('url') and value:
                    response_data[item] = self._get_actual_image_url(value)

        elif isinstance(response_data, list):
            for index, data in enumerate(response_data):
                response_data[index] = self._correct_response_data(data)
        return response_data


    def update_qrcode(self, qrcode_id: str, qrcode_link: str, data: Dict[str, Any], verbose: bool = False):
        """
        Updates QR Code with data provided

        :param qrcode_id (str): `qrcode_id` of QR Code to be updated
        :param qrcode_link (str): `link` of the QR Code to be updated
        :param data (Dict[str, Any]): data to be updated
        :param verbose (bool): if True, return the response object instead of the image url

        :return: link to new QR Code image by default.
        """
        data.update({"link": qrcode_link, "created_by": self.username, "company_id": self.user_id})
        self._validate_payload(data, validate_with=ALLOWED_UPDATE_FIELDS)
        response = self.session_.put(f"{api_put_url}/{qrcode_id}/", data=data)

        if not response.ok:
            raise QRCodeUpdateError(f"Error updating QR Code: {response.text}")
        response_data =  response.json()['response']
        response_data = self._correct_response_data(response_data)
        if verbose is True:
            return response_data
        return response_data['qrcode_image_url']


    def get_qrcode(self, qrcode_id: str, verbose: bool = False):
        """
        Get QR code image for qrcode_id

        :param qrcode_id (str): id of QR Code to be retrieved
        :param verbose (bool): if True, return the response object instead of the image url
        """
        response = self.session_.get(f"{api_put_url}/{qrcode_id}/")
        if not response.ok:
            if response.status_code == 404:
                raise QRCodeNotFoundError(f"QR Code with id {qrcode_id} not found")
            raise QRCodeRetrievalError(f"Error getting QR Code: {response.text}")
        response_data = response.json()['response'][0]
        response_data = self._correct_response_data(response_data)
        if verbose is True:
            return response_data
        return response_data['qrcode_image_url']


    def get_qrcodes(self):
        """Get all QR codes associated with user"""
        response = self.session_.get(api_get_url, params={'company_id': self.user_id})
        if not response.ok:
            raise QRCodeRetrievalError(f"Error getting QR Codes: {response.text}")
        response_data = response.json()['response']['data']
        response_data = self._correct_response_data(response_data)
        return response_data


    @staticmethod
    def download_qrcode_image(qrcode_url: str, save_to: str):
        """
        Download QR Code image from url

        :params qrcode_url (str): url to QR Code image
        :params save_to (str): path to save downloaded image to
        :return: bs4_web_scraper.FileHandler object of downloaded image

        To get the image file itself, use the `file` attribute of the returned object
        and for the file path use the `file_path` attribute
        """
        downloader = scraper.BS4WebScraper()
        downloaded_file_hdl = downloader.download_url(qrcode_url, save_to=save_to)
        return downloaded_file_hdl