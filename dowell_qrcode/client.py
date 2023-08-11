"""
Contains base class for the Dowell QR Code Generator API Client
"""

import requests
import random
from bs4_web_scraper.utils import generate_random_user_agents
from bs4_web_scraper import scraper
from typing import Dict, Any, List


from .exceptions import (   ClientError, QRCodeGenerationError, QRCodeUpdateError, 
                            QRCodeNotFoundError, QRCodeRetrievalError, NotSupportedError,
                         )


api_base_url = 'https://100099.pythonanywhere.com/api/v2'
api_status_url = f"{api_base_url}/server-status/"
api_get_url = f"{api_base_url}/qr-code/"
api_put_url = f"{api_base_url}/update-qr-code/"
actual_image_url_base = "http://67.217.61.253/uploadfiles/qrcode-download"

ALLOWED_CREATE_FIELDS = {
    "logo": str,
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
    "logo": str,
    "company_id": str,
    "created_by": str,
    "link": str,
    "qrcode_color": str,
    "logo_size": int,
    "product_name": str,
    "description": str,
    "is_active": bool,
}

AVAILABLE_QRCODE_TYPES = ('Link',)


def get_new_user_agent() -> str:
    """Get a new user agent and save it to config.json"""
    user_agent = random.choice(generate_random_user_agents())
    return user_agent



class Client:
    """Handles QR Code generation, update and retrieval using Dowell QR Code Generator API"""

    session_ = requests.Session()
    user_agent = get_new_user_agent()

    def __init__(self, username: str, user_id: str, api_key: str):
        """
        Initialize class

        :param username (str): username of the user. Should be unique
        :param user_id (str): user id of the user. Should be unique
        :param api_key (str): Dowell API key for the user

        Visit https://ll05-ai-dowell.github.io/100105-DowellApiKeySystem/ to get your API key
        """
        self.username = username
        self.user_id = user_id
        self.api_key = api_key
        self.session_.headers.update({"User-Agent": self.user_agent})


    @classmethod
    def get_status(cls):
        """
        Get the status of Dowell QR Code Generator API

        :return (dict): dictionary containing the status of the API and response code or text if API is unreachable
        """
        resp = cls.session_.get(url=api_status_url)
        if resp.ok:
            status_resp = resp.json()
            status_resp.update({'status_code': resp.status_code})
        else:
            status_resp = {'info': resp.text, 'status_code': resp.status_code}
        return status_resp


    @property
    def available_qrcode_types(self):
        """Return a tuple of available qrcode types"""
        return AVAILABLE_QRCODE_TYPES

    
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
                raise KeyError(f"Invalid field `{key}`. Allowed fields are {list(validate_with.keys())}")
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
            "created_by": data.get("created_by", self.username),
            "company_id": self.user_id,
            "qrcode_type": data.get('qrcode_type', 'Link'),
            "link": data.get('link', 'https://google.com/'),
            "product_name": data.get('product_name', 'QR Code'),
            "qrcode_color": data.get('qrcode_color', '#000000'),
            "logo_size": data.get('logo_size', 20),
            "description": data.get('description', ''),
            "is_active": data.get('is_active', False)
        }
        try:
            self._validate_payload(payload, validate_with=ALLOWED_CREATE_FIELDS)
        except Exception as e:
            raise e                   
        return payload

    
    def endsession(self):
        """End client request session with API"""
        self.session_.cookies.clear()
        return self.session_.close()


    def generate_qrcode(self, obj: str | Any, product_name: str = None, qrcode_type: str = "Link", verbose: bool = False, **kwargs):
        """
        Generate QR Code for object of `qrcode_type`. QR code is deactivated by default.
        
        :param obj (str | Any): object for which QR Code is to be generated. If `qrcode_type` is `Link`, then `obj` should be a valid url.
        :param verbose (bool): if True, return the response object for the created QR code from the API
        :param kwargs: additional data to be sent to the API
            :kwarg quantity (int): number of QR Codes to be generated

            :kwarg logo (str): path to logo to be added to QR Code

            :kwarg logo_size (int): size of logo to be added to QR Code

            :kwarg qrcode_color (str): color of QR Code to be generated. Must be a valid hex color code. Use colors that have good contrast with white.

            :kwarg description (str): description of QR Code to be generated

        :return: a tuple of the QR Code image url and the QR Code id or a list of such tuples if quantity is greater than 1
        :raises NotSupportedError: if `qrcode_type` is not supported.
        :raises QrCodeGenerationError: if QR Code generation fails
        """
        if qrcode_type not in self.available_qrcode_types:
            raise NotSupportedError(f"Invalid QR Code type. Available types are {self.available_qrcode_types}")

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
        response = self.session_.post(
            url=api_get_url, 
            data=payload, 
            files=files, 
            params={"api_key": self.api_key}
        )
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
                return (response_data[0]["qrcode_image_url"], response_data[0]["qrcode_id"])
        else:
            raise QRCodeGenerationError(f"Error generating QR Code: reason: {response.text}")


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


    def update_qrcode(self, qrcode_id: str, data: Dict[str, Any], verbose: bool = False):
        """
        Updates QR Code with data provided. Occasionally, updates may take a while to reflect.

        :param qrcode_id (str): `qrcode_id` of QR Code to be updated
        :param data (Dict[str, Any]): data to be updated
        :param verbose (bool): if True, return the response object instead of the image url

        :return: link to new QR Code image by default.
        :raises: QRCodeUpdateError if the API returns an error
        """
        data.update({"company_id": self.user_id})
        # Handle logo data
        logo_path = data.pop('logo', '')
        files = []
        if logo_path:
            logo_path = logo_path.strip().replace('\\', '/')
            logo_name = logo_path.split('/')[-1]
            f = open(logo_path, mode="rb")
            files = [
                ('logo', (logo_name, f, 'application/octet-stream'))
            ]

        self._validate_payload(data, validate_with=ALLOWED_UPDATE_FIELDS)
        response = self.session_.put(
            url=f"{api_put_url}/{qrcode_id}/", 
            data=data, 
            files=files, 
            params={"api_key": self.api_key}
        )

        if logo_path:
            f.close()

        if not response.ok:
            raise QRCodeUpdateError(f"Error updating QR Code: reason: {response.text}")
        response_data =  response.json()['response']
        response_data = self._correct_response_data(response_data)
        if verbose is True:
            return response_data
        return response_data['qrcode_image_url']


    def get_qrcode(self, qrcode_id: str, verbose: bool = False):
        """
        Get QR code image for `qrcode_id`

        :param qrcode_id (str): id of QR Code to be retrieved
        :param verbose (bool): if True, return the response object instead of the image url

        :return: link to QR Code image by default
        :raises QRCodeNotFoundError: if QR Code with `qrcode_id` is not found
        :raises QRCodeRetrievalError: if there is an error retrieving QR Code
        """
        response = self.session_.get(
            url=f"{api_put_url}/{qrcode_id}/",
            params={"api_key": self.api_key}
        )
        if not response.ok and response.status_code != 404:
            raise QRCodeRetrievalError(f"Error getting QR Code: reason: {response.text}")

        if not response.json()['response'] or response.status_code == 404:
            raise QRCodeNotFoundError(f"QR Code with id {qrcode_id} not found")
        response_data = response.json()['response'][0]
        response_data = self._correct_response_data(response_data)
        if verbose is True:
            return response_data
        return response_data['qrcode_image_url']


    def get_qrcodes(self):
        """
        Get all QR codes associated with `user_id`
        
        :return (List[Dict[str, Any]]): list of QR Codes
        :raises QRCodeRetrievalError: if there is an error retrieving QR Codes
        """
        response = self.session_.get(
            url=api_get_url, 
            params={
                'company_id': self.user_id,
                "api_key": self.api_key,
            }
        )
        if not response.ok:
            raise QRCodeRetrievalError(f"Error getting QR Codes: reason: {response.text}")
        response_data = response.json()['response']['data']
        response_data = self._correct_response_data(response_data)
        return response_data


    def activate_qrcode(self, qrcode_id: str):
        """
        Activate QR Code with `qrcode_id`

        :param qrcode_id (str): id of QR Code to be activated
        :raises ClientError: if QR Code is not activated
        """
        try:
            activated_qrcode = self.update_qrcode(qrcode_id, data={'is_active': True}, verbose=True)
            if activated_qrcode['is_active'] != True:
                raise ClientError(f"Error activating QR Code: reason: `is_active` is still False")
        except ClientError as e:
            raise ClientError(e)
        return None


    def deactivate_qrcode(self, qrcode_id: str):
        """
        Deactivate QR Code with `qrcode_id`
        
        :param qrcode_id (str): id of QR Code to be deactivated
        :raises ClientError: if QR Code is not deactivated
        """
        try:
            deactivated_qrcode = self.update_qrcode(qrcode_id, data={'is_active': False}, verbose=True)
            if deactivated_qrcode['is_active'] != False:
                raise ClientError(f"Error deactivating QR Code: reason: `is_active` is still True")
        except ClientError as e:
            raise ClientError(e)
        return None


    @staticmethod
    def download_qrcode(qrcode_url: str, save_to: str):
        """
        Download QR Code image from url

        :params qrcode_url (str): url to QR Code image
        :params save_to (str): path to directory where the downloaded image will be saved
        :return: bs4_web_scraper.FileHandler object of downloaded image

        To get the image file itself, use the `file` attribute of the returned object
        and for the file path use the `file_path` attribute
        """
        downloader = scraper.BS4WebScraper()
        downloaded_file_hdl = downloader.download_url(qrcode_url, save_to=save_to)
        return downloaded_file_hdl