.. dowell_qrcode documentation master file, created by
   sphinx-quickstart on Mon Jul  3 14:25:22 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

📑 Dowell QR Code Generator Client Documentation
=================================================
.. toctree::
   :maxdepth: 2
   :caption: Contents:


This is a python client for the Dowell QR Code Generator API. Uses API version 2.

About the API
-------------

This API provides endpoints that allows for the creation, retrieval and update of two-dimensional barcodes - QR codes, that can store data such as URLs and other types of information. Read the `API documentation <https://documenter.getpostman.com/view/14306028/2s93mBwyrj>`_ for more information.

Installation
------------

To install a distribution of this package, do the following:

.. code-block:: bash

   git clone https://github.com/DoWellLabs/100099-Dowell-QR-code-Package.git

   cd 100099-Dowell-QR-code-Package

   git checkout DowellQRCodeClient-DanielAfolayan

   pip install dist/dowell_qrcode-0.1.0-py3-none-any.whl

Quickstart
----------

Here is a quickstart guide to get you started.

Generating QR Codes for Links
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To import the api client used to create QR codes for links, use the following code:

.. code-block:: python

   import dowell_qrcode

   # Create a client
   client = dowell_qrcode.Client(username='Username', user_id="UserID")

   # Generate QR Code for a link
   result = client.generate_qrcode(obj='https://www.google.com', product_name='Google Link', qrcode_type='Link')
   # You can read the method docstring for more information on other keyword arguments you can pass

   qrcode_image_url, qrcode_id = result
   print(qrcode_image_url, qrcode_id, sep='\n')

``client.generate_qrcode`` usually returns a tuple containing the qrcode image url and the qrcode id. You can read the method docstring for more information on the return type.

To get a more detailed result set the ``verbose`` argument to True.

.. code-block:: python


   result = client.generate_qrcode(obj='https://www.google.com', product_name='Google Link', qrcode_type='Link', verbose=True)
   print(result)
   client.activate_qrcode(qrcode_id=result['qrcode_id'])

The result returned here is basically the response object from the API. You can read the `API documentation <https://documenter.getpostman.com/view/14306028/2s93mBwyrj>`_ for more information on the response object.

Generating QR Codes for Images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generating QR codes for links is done using a different client from the one used to generate QR codes for images. To import the api client used to create QR codes for images, use the following code:

.. code-block:: python

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

..

   Note that ImageClient can only generate QR codes for images that have at least one human face in it. If you try to generate a QR code for an image that does not have a human face, a ``NoFaceDetected`` error will be raised.


Getting QR Code Details
^^^^^^^^^^^^^^^^^^^^^^^

To get the details of an already existing QR code, use the following code:

.. code-block:: python

   import dowell_qrcode

   client = dowell_qrcode.Client(username='Username', user_id="UserID")
   qrcode_image_url = client.get_qrcode(qrcode_id='QrCodeID')
   print(qrcode_image_url)

   # For a more detailed result, set the verbose argument to True
   result = client.get_qrcode(qrcode_id='QrCodeID', verbose=True)
   print(result)

Getting all QR Codes
^^^^^^^^^^^^^^^^^^^^

To get a qr code list associated to a user, use the following code:

.. code-block:: python


   qr_code_list = client.get_qrcodes()
   print(qr_code_list)

Updating QR Code Details
^^^^^^^^^^^^^^^^^^^^^^^^

To update the details of an already existing QR code, use the following code:

.. code-block:: python


   update_payload = {
       "qrcode_color": '#ff0000', 
       "description": 'This is a new description'
   }
   updated_qrcode = client.update_qrcode(qrcode_id='QrCodeID', data=update_payload, verbose=True)
   print(updated_qrcode)

..

   Note! You cannot update the qrcode ``company_id`` and ``logo``\ (for images only) field. If you try to update, it will be ignored.


For more info on fields you can update:

.. code-block:: python

   from dowell_qrcode import client

   print(client.ALLOWED_UPDATE_FIELDS)

Downloading QR Code Image
^^^^^^^^^^^^^^^^^^^^^^^^^

To download the QR code image, use the following code:

.. code-block:: python

   import dowell_qrcode

   client = dowell_qrcode.Client(username='Username', user_id="UserID")
   qrcode_image_url = client.get_qrcode(qrcode_id='QrCodeID')

   # returns a FileHandler object
   file_handler = client.download_qrcode(qrcode_url=qrcode_image_url, save_to='path/to/dir')

   print(file_handler.file_path)
   file_handler.close_file() # Always close the file handler after use

Deactivating a QR Code
^^^^^^^^^^^^^^^^^^^^^^

QR codes cannot be deleted. They can only be deactivated. To deactivate a QR code, use the following code:

.. code-block:: python


   client = dowell_qrcode.Client(username='Username', user_id="UserID")
   client.deactivate_qrcode(qrcode_id='QrCodeID')

   assert client.get_qrcode(qrcode_id='QrCodeID', verbose=True)['is_active'] == False

Activating a QR Code
^^^^^^^^^^^^^^^^^^^^

To activate a QR code, use the following code:

.. code-block:: python


   client = dowell_qrcode.Client(username='Username', user_id="UserID")
   client.activate_qrcode(qrcode_id='QrCodeID')

   assert client.get_qrcode(qrcode_id='QrCodeID', verbose=True)['is_active'] == True

End User Session with the API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To end a user session with the API, use the following code:

.. code-block:: python


   client.endsession()

Classes
-------

The ``Client`` Class
^^^^^^^^^^^^^^^^^^^^^^^^

The ``Client`` class is used to create a client object that can be used to interact with the API. Listed below are most of the objects attributes and methods:

Instantiating the ``Client`` Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creating an instance requires the ``username`` and ``user_id`` of the user.

.. code-block:: python

   import dowell_qrcode

   # Create a client
   client = dowell_qrcode.Client(username='Username', user_id="UserID")

Attributes
~~~~~~~~~~

The ``Client`` object has the following attributes:


* ``username``\ : The username of the user
* ``user_id``\ : The user id of the user
* ``session_``\ : The session object used to make requests to the API at the moment
* ``user_agent``\ : The user agent used in ``client.session_`` headers

Methods
~~~~~~~

The ``Client`` object has the following methods:


* 
  ``get_qrcode(qrcode_id, verbose=False)``\ : Get the details of a QR code


  * ``qrcode_id``\ : The id of the QR code
  * 
    ``verbose``\ : If True, returns a more detailed result

    .. code-block:: python

       # Example
       result = client.get_qrcode(qrcode_id='QrCodeID', verbose=True)
       print(result)

       # set verbose to False to get a simpler result
       result = client.get_qrcode(qrcode_id='QrCodeID', verbose=False)
       print(result)

* 
  ``get_qrcodes()``\ : Get a list of all QR codes associated to the user

  .. code-block:: python

       # Example
       qr_code_list = client.get_qrcodes()
       print(qr_code_list)

* 
  ``generate_qrcode(self, obj: str | Any, product_name: str = None, qrcode_type: str = "Link", verbose: bool = False, **kwargs)``\ : Generate a QR code for a link


  * ``obj``\ : The object to generate a QR code for. It can be a link or an image object
  * ``product_name``\ : The name of the product
  * ``qrcode_type``\ : The type of QR code to generate. Leave as ``Link`` for now
  * ``verbose``\ : If True, returns a more detailed result
  * 
    ``**kwargs``\ : Other keyword arguments to pass to the API

    .. code-block:: python

       # Example
       result = client.generate_qrcode(obj='https://www.google.com', product_name='Google', qrcode_type='Link', verbose=True)
       print(result)

       # providing other keyword arguments
       kwargs = {
           "qrcode_color": '#ff0000', 
           "description": 'This is a new description'
           "quantity": 10, # The number of QR codes to generate. Multiple results will be returned
       }
       result = client.generate_qrcode(obj='https://www.google.com', product_name='Google', qrcode_type='Link', verbose=True, **kwargs)
       print(result)

* 
  ``update_qrcode(qrcode_id, data, verbose=False)``\ : Update the details of a QR code


  * ``qrcode_id``\ : The id of the QR code
  * ``data``\ : The data to update the QR code with
  * 
    ``verbose``\ : If True, returns a more detailed result

    .. code-block:: python

       # Example
       data = {
           "product_name": "New Product Name",
           "description": "New Description",
           "qrcode_color": "#ff0000",
           "logo": "path/to/logo.png"
       }
       result = client.update_qrcode(qrcode_id='QrCodeID', data=data, verbose=True)
       print(result)

* 
  ``download_qrcode(qrcode_url, save_to)``\ : Download a QR code image


  * ``qrcode_url``\ : The url of the QR code image
  * 
    ``save_to``\ : The path to save the QR code image to

    .. code-block:: python

       # Example
       qrcode_image_url = client.get_qrcode(qrcode_id='QrCodeID')
       file_handler = client.download_qrcode(qrcode_url=qrcode_image_url, save_to='path/to/dir')

       print(file_handler.file_path)
       file_handler.close_file() # Always close the file handler after use

* 
  ``deactivate_qrcode(qrcode_id)``\ : Deactivate a QR code


  * 
    ``qrcode_id``\ : The id of the QR code

    .. code-block:: python

       # Example
       client.deactivate_qrcode(qrcode_id='QrCodeID')

* 
  ``activate_qrcode(qrcode_id)``\ : Activate a QR code

  .. code-block:: python

       # Example
       client.activate_qrcode(qrcode_id='QrCodeID')

* 
  ``endsession()``\ : End the user session with the API

  .. code-block:: python

       # Example
       client.endsession()

* 
  ``get_status()``\ : Get the status of the API

  .. code-block:: python

       # Example
       status = client.get_status()
       print(status)

Constants
~~~~~~~~~

The ``dowell_qrcode`` module has the following constants:


* ``ALLOWED_UPDATE_FIELDS``\ : The fields that can be updated for a QR code
* ``ALLOWED_CREATE_FIELDS``\ : The fields that can be passed to the API to create a QR code

To access the constants, use the following code:

.. code-block:: python

   from dowell_qrcode import client

   print(client.ALLOWED_UPDATE_FIELDS)
   print(client.ALLOWED_CREATE_FIELDS)

The ``ImageClient`` Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``ImageClient`` class is used to generate QR codes for images. It is a subclass of the ``Client`` class. Hence, it inherits all methods and attributes of the ``Client`` class except for two specific methods, ``generate_qrcode`` and ``update_qrcode``\ , modified to allow for QR code generation for images.

For more information on the ``Client`` class, see the `Client Class <#the-client-class>`_ section.

Instatiating the ``ImageClient`` Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instatiation works the same as the ``Client`` class.

.. code-block:: python

   import dowell_qrcode

   # Instatiate the ImageClient
   image_client = dowell_qrcode.ImageClient(username='Username', user_id='UserID')

Modified Methods
~~~~~~~~~~~~~~~~

The following methods have been modified to allow for QR code generation for images:


* 
  ``generate_qrcode(self, image: Image | str, image_name: str = None, qrcode_type: str = "Link", verbose: bool = False, **kwargs)``\ : Generate a QR code for an image. Uses `Image <#the-image-class>`_ objects.


  * ``image``\ : The image object or path to the image
  * ``image_name``\ : The name of the image
  * ``qrcode_type``\ : The type of QR code to generate. Leave as is.
  * ``verbose``\ : If True, returns a more detailed result
  * 
    ``**kwargs``\ : Other keyword arguments to pass to the API

    .. code-block:: python

       # Example using an `Image` object
       img = dowell_qrcode.Image(path='path/to/image.png')
       result = image_client.generate_qrcode(image=img, image_name='Image', qrcode_type='Image', verbose=True)
       # Alternatively, you can pass the path to the image
       result = image_client.generate_qrcode(image='path/to/image.png', image_name='Image', qrcode_type='Image', verbose=True)
       print(result)

       # providing other keyword arguments
       # Note `logo` is not allowed for image QR codes
       kwargs = {
           "qrcode_color": '#ff0000', 
           "description": 'This is a new description'
           "quantity": 5, # The number of QR codes to generate. Multiple results will be returned
       }
       result = image_client.generate_qrcode(image='path/to/image.png', image_name='Image', verbose=True, **kwargs)
       print(result)

* 
  ``update_qrcode(self, qrcode_id, data, verbose=False)``\ : Update the details of a QR code


  * ``qrcode_id``\ : The id of the QR code
  * ``data``\ : The data to update the QR code with
  * 
    ``verbose``\ : If True, returns a more detailed result

    .. code-block:: python

       # Example
       # Note `logo` is not allowed for image QR codes
       data = {
           "product_name": "New Product Name",
           "description": "New Description",
           "qrcode_color": "#ff0000",
       }
       result = image_client.update_qrcode(qrcode_id='QrCodeID', data=data, verbose=True)
       print(result)

The ``Image`` Class
^^^^^^^^^^^^^^^^^^^^^^^

The ``Image`` class is used to create a custom image object that can be passed to the ImageClient to generate QR codes for images. It also allows for face detection in the image. Listed below are most of the objects attributes and methods:

Instatiating the ``Image`` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To instatiate the ``Image`` class, use the following code:

.. code-block:: python

   import dowell_qrcode

   # Instatiate the Image class
   image = dowell_qrcode.Image(path='path/to/image.png')

Attributes
~~~~~~~~~~

The ``Image`` class has the following attributes:


* ``data``\ : The image data as a numpy array
* ``name``\ : The name of the image
* ``path``\ : The path to the image
* ``format``\ : The image extension format
* ``size``\ : The image size in bytes
* ``width``\ : The image width
* ``height``\ : The image height
* ``aspect_ratio``\ : The image aspect ratio
* ``area``\ : The image area
* ``bytes``\ : The image data in bytes
* ``has_face``\ : True if the image has a human face, False otherwise
* ``face_count``\ : The number of faces in the image
* ``gray``\ : The image data in grayscale
* ``eqgray``\ : The image data in equalized grayscale
* ``binary``\ : The image data in binary
* ``binary_inv``\ : The image data in inverted binary
* ``is_empty``\ : True if the image data is empty, that is ``image.size`` is (0, 0), False otherwise
* ``is_valid``\ : Returns True if image data is not empty, False otherwise
* ``is_color``\ : Returns True if the image is in color, False otherwise
* ``is_grayscale``\ : Returns True if the image is in grayscale, False otherwise
* ``is_binary``\ : Returns True if the image is in binary, False otherwise
* ``is_valid_color``\ : Returns True if the image is valid and in color, False otherwise
* ``is_valid_grayscale``\ : Returns True if the image is valid and in grayscale, False otherwise
* ``is_valid_binary``\ : Returns True if the image is valid and in binary, False otherwise

Methods
~~~~~~~

The ``Image`` class has the following methods:


* 
  ``find_faces()``\ : Find faces in the image

  .. code-block:: python

       # Example
       face_coordinates = image.find_faces()
       print(face_coordinates)

* 
  ``markout_faces(self, face_coordinates: List[Tuple[int, int, int, int]], color: tuple = (0, 255, 0))``\ : Mark out faces in the image

  .. code-block:: python

       # Example
       face_coordinates = image.find_faces()
       image.markout_faces(face_coordinates=face_coordinates, color=(0, 0, 255)) # draw red rectangles around the faces

* 
  ``save(path: str = None, quality: int = 100)``\ : Save the image to a file


  * ``path``\ : The path to save the image to. If None, the image is saved in the origin path
  * 
    ``quality``\ : The quality of the image to save. Only applies to JPEG, JPG, WEBP, PNG, and TIFF images

    .. code-block:: python

       # Example
       # save image in origin path
       image.save()
       # save image in a new path
       image.save(path='path/to/new/image.png')

       # save image with quality compression
       image.save(quality=50)

* 
  ``show()``\ : Show the image in a desktop window

  .. code-block:: python

       # Example
       image.show()

* 
  ``resize(self, width: int = None, height: int = None, interpolation: int = cv2.INTER_AREA)``\ : Resize the image


  * ``width``\ : The width to resize the image to
  * ``height``\ : The height to resize the image to
  * 
    ``interpolation``\ : The interpolation method to use

    .. code-block:: python

       # Example
       # resize image to 500x500
       image.resize(width=500, height=500)

* 
  ``crop(self, x_top_left: int, y_top_left: int, width: int, height: int, resize: bool = True)``\ : Crop the image


  * ``x_top_left``\ : The x coordinate of the top left corner of the crop
  * ``y_top_left``\ : The y coordinate of the top left corner of the crop
  * ``width``\ : The width of the crop
  * ``height``\ : The height of the crop
  * 
    ``resize``\ : If True, resize the image to the original image size

    .. code-block:: python

       # Example
       # crop image to 500x500
       image.crop(x_top_left=0, y_top_left=0, width=500, height=500)

* 
  ``rotate(self, angle: int, center: tuple = None, scale: float = 1.0)``\ : Rotate the image


  * ``angle``\ : The angle to rotate the image by
  * ``center``\ : The center of the rotation
  * 
    ``scale``\ : Optional parameter to adjust the scale of the image during rotation

    .. code-block:: python

       # Example
       # rotate image by 90 degrees
       image.rotate(angle=90)

* 
  ``flip(self, direction: int)``\ : Flip the image


  * 
    ``direction``\ : The direction to flip the image. 0 for vertical flip, 1 for horizontal flip, and -1 for both vertical and horizontal flip

    .. code-block:: python

       # Example
       # flip image vertically
       image.flip(direction=0)

* 
  ``draw_rectangle(self, x_top_left: int, y_top_left: int, width: int, height: int, rgb: tuple = (255, 0, 0), thickness: int = 2)``\ : Draw a rectangle on the image


  * ``x_top_left``\ : The x coordinate of the top left corner of the rectangle
  * ``y_top_left``\ : The y coordinate of the top left corner of the rectangle
  * ``width``\ : The width of the rectangle
  * ``height``\ : The height of the rectangle
  * ``rgb``\ : The color of the rectangle border in RGB format
  * 
    ``thickness``\ : The thickness of the rectangle's border

    .. code-block:: python

       # Example
       # draw a red rectangle on the image
       image.draw_rectangle(x_top_left=0, y_top_left=0, width=500, height=500, rgb=(255, 0, 0))

* 
  ``grayscale(self, equalize: bool = False)``\ : Convert ``image.data`` to grayscale. This replaces the original image data


  * 
    ``equalize``\ : If True, equalize the grayscale image

    .. code-block:: python

       # Example
       # convert image to grayscale
       image.grayscale()
       # convert image to equalized grayscale
       image.grayscale(equalize=True)

* 
  ``makebinary(self, invert: bool = False)``\ : Convert ``image.data`` to binary. This replaces the original image data


  * 
    ``invert``\ : If True, invert the binary image

    .. code-block:: python

       # Example
       # convert image to binary
       image.makebinary()
       # convert image to inverted binary
       image.makebinary(invert=True)

Get API version and status
^^^^^^^^^^^^^^^^^^^^^^^^^^

To get the API version and status, use the following code:

.. code-block:: python

   import dowell_qrcode

   # Get API version
   print(dowell_qrcode.api_version)

   # Get API status
   status = dowell_qrcode.get_api_status()
   print(status)

Dependencies
^^^^^^^^^^^^


* `opencv-python <https://pypi.org/project/opencv-python/>`_
* `requests <https://pypi.org/project/requests/>`_
* `bs4_web_scraper <https://pypi.org/project/bs4-web-scraper/>`_


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
