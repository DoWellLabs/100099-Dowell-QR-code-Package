# Dowell QR Code Generator Client

This is a python client for the Dowell QR Code Generator API. Uses API version 2.

**[Documentation](https://dowell-qr-code-package.readthedocs.io/en/latest/)**

## Setting up in local environment

* Clone the repository to your local machine
* Import the `dowell_qrcode` module from the local repository

## Usage

### Generating QR Codes for Links

To import the api client used to create QR codes for links, use the following code:

```python
import dowell_qrcode

# Create a client
client = dowell_qrcode.Client(username='Username', user_id="UserID")

# Generate QR Code for a link
result = client.generate_qrcode(obj='https://www.google.com', product_name='Google Link', qrcode_type='Link')
# You can read the method docstring for more information on other keyword arguments you can pass

qrcode_image_url, qrcode_id = result
print(qrcode_image_url, qrcode_id, sep='\n')

```

`client.generate_qrcode` usually returns a tuple containing the qrcode image url and the qrcode id. You can read the method docstring for more information on the return type.

To get a more detailed result set the `verbose` argument to True.

```python

result = client.generate_qrcode(obj='https://www.google.com', product_name='Google Link', qrcode_type='Link', verbose=True)
print(result)
client.activate_qrcode(qrcode_id=result['qrcode_id'])

```

The result returned here is basically the response object from the API. You can read the [API documentation](https://documenter.getpostman.com/view/14306028/2s93mBwyrj) for more information on the response object.


### Generating QR Codes for Images

Generating QR codes for links is done using a different client from the one used to generate QR codes for images. To import the api client used to create QR codes for images, use the following code:

```python
import dowell_qrcode

# Create a client
image_client = dowell_qrcode.ImageClient(username='Username', user_id="UserID")

# Generate QR Code for an image

# Create a custom image object using the Image class
image = dowell_qrcode.Image('path/to/image.png')
result = image_client.generate_qrcode(image=image, image_name='My image')

# Alternatively, you can pass the path to the image file directly
result = image_client.generate_qrcode(image='path/to/image.png', image_name='My image')
# You can read the method docstring for more information on other keyword arguments you can pass

qrcode_image_url, qrcode_id = result
print(qrcode_image_url, qrcode_id, sep='\n')

```

> Note that ImageClient can only generate QR codes for images that have at least one human face in it. If you try to generate a QR code for an image that does not have a human face, a `NoFaceDetected` error will be raised.

### Getting QR Code Details

To get the details of an already existing QR code, use the following code:

```python
import dowell_qrcode

client = dowell_qrcode.Client(username='Username', user_id="UserID")
qrcode_image_url = client.get_qrcode(qrcode_id='QrCodeID')
print(qrcode_image_url)

# For a more detailed result, set the verbose argument to True
result = client.get_qrcode(qrcode_id='QrCodeID', verbose=True)
print(result)

```

### Getting all QR Codes

To get a qr code list associated to a user, use the following code:

```python

qr_code_list = client.get_qrcodes()
print(qr_code_list)

```

### Updating QR Code Details

To update the details of an already existing QR code, use the following code:

```python

update_payload = {
    "qrcode_color": '#ff0000', 
    "description": 'This is a new description'
}
updated_qrcode = client.update_qrcode(qrcode_id='QrCodeID', data=update_payload, verbose=True)
print(updated_qrcode)

```

> Note! You cannot update the qrcode `company_id` and `logo`(for images only) field. If you try to update, it will be ignored.

For more info on fields you can update:

```python
from dowell_qrcode import client

print(client.ALLOWED_UPDATE_FIELDS)

```

### Downloading QR Code Image

To download the QR code image, use the following code:

```python
import dowell_qrcode

client = dowell_qrcode.Client(username='Username', user_id="UserID")
qrcode_image_url = client.get_qrcode(qrcode_id='QrCodeID')

# returns a FileHandler object
file_handler = client.download_qrcode(qrcode_url=qrcode_image_url, save_to='path/to/dir')

print(file_handler.file_path)
file_handler.close_file() # Always close the file handler after use

```

### Deactivating a QR Code

QR codes cannot be deleted. They can only be deactivated. To deactivate a QR code, use the following code:

```python

client = dowell_qrcode.Client(username='Username', user_id="UserID")
client.deactivate_qrcode(qrcode_id='QrCodeID')

assert client.get_qrcode(qrcode_id='QrCodeID', verbose=True)['is_active'] == False

```

### Activating a QR Code

To activate a QR code, use the following code:

```python

client = dowell_qrcode.Client(username='Username', user_id="UserID")
client.activate_qrcode(qrcode_id='QrCodeID')

assert client.get_qrcode(qrcode_id='QrCodeID', verbose=True)['is_active'] == True

```

### End User Session with the API

To end a user session with the API, use the following code:

```python

client.endsession()
    
```

### Get API version and status

To get the API version and status, use the following code:

```python
import dowell_qrcode

# Get API version
print(dowell_qrcode.api_version)

# Get API status
status = dowell_qrcode.get_api_status()
print(status)

```

### Dependencies

* [opencv-python](https://pypi.org/project/opencv-python/)
* [requests](https://pypi.org/project/requests/)
* [bs4_web_scraper](https://pypi.org/project/bs4-web-scraper/)
