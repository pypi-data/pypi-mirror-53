# Verifai SDK for Python

Great that you choose to use Verifai for your business or project. This software development kit (SDK) takes
care of most of the heavy lifting for you. It is aimed to be used for every level of developer. There are some samples provided so you can see it work.

Companies use Verifai to comply with the GDPR legislation that states
you should not store data about your users and customers that you do not
need for your business. By masking unneeded data you can comply to that.

Features of this SDK are:

 * Detect ID documents in JPEG images (in a privacy guaranteed way)
 * Give you information about the detected document
    * Position in the image
    * Type of document
    * The zones on the document
 * Get a cropped out image from the provided image
 * Get crops of all individual zones
 * Apply masks to the ID document image
 * Read the Machine Readable Zones of documents

## Full documentation

The full documentation can be found at https://docs.verifai.com/

This README only contains the basic setup and a simple classify call.

## Quick introduction

![Highlevel setup](docs/Server-SDK-flow-with-ocr-design.png)

The basic idea is that all of your users or client's private data stays within
your own network. Data we do not have, we can not loose.

Therefore the heavy lifting takes place in the
"Verifai Server-side Classifier" and the SDK. The SDK sends a JPEG image
to it via a HTTP POST request, and it responds with a JSON result. The SDK
processes that response for you. You only have to tell it where the
"Server-side Classifier" is within your network.

When you need more information, like the kind of document you are dealing with, the name, or what
data is where on the document, it fetches that from the Verifai servers.

No personal information is sent to us, never.

## Install

Setup the SDK for use first. You can install it via [PIP](https://pypi.org/project/verifai-sdk/).

    pip install verifai-sdk

Check if it is installed:

    Python 3.6.1 (v3.6.1:69c0db5050, Mar 21 2017, 01:21:04)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin

    >>> import verifai_sdk
    >>> verifai_sdk.VERSION
    '1.0.0'

    >>>

## Initialize SDK

If the setup is tested we can continue with the initialization of the
SDK. From now on we will assume that you initialized the SDK before use.

    from verifai_sdk import VerifaiService

    # Setup the service with your API token
    # the token is used for `SDK` <-> `Verifai API` communication.
    service = VerifaiService(token='<API TOKEN IN HERE>')

    # Tell the service where on your network the "Verifai Server-side
    # Classifier" can be found.
    # See the Verifai Server-side Classifier docs for info about how to
    # set it up.
    service.add_classifier_url('http://localhost:5000/api/classify/')

    # service is now initialized and ready to use.

## Classify a JPEG image

There are Dutch ID document sample images in the `docs/sample_images/`
directory. We will use `dutch-id-front-sample.jpg` underneath.

    import os

    # Assuming you initialized from here on

    sample_dir = 'docs/sample_images/'
    image_path = os.path.join(sample_dir, 'dutch-id-front-sample.jpg')

    document = service.classify_image_path(image_path)
    print(document)  # <verifai_sdk.VerifaiDocument object at 0x10e44e710>

    print(document.model)  # "Dutch ID 011"
    print(document.country)  # "NL"

You now know that there is a "Dutch ID 011" in this image. Lets get it's
position now.

    print(document.position_in_image)
    # {
    #   'xmax': 0.6118464469909668,
    #   'xmin': 0.21217313408851624,
    #   'ymax': 0.8527788519859314,
    #   'ymin': 0.45336633920669556
    # }

The position is relative, e.g. 0.5 means half way the image. It
the top-left and bottom-right are given. You can use this for further
processing if you like.

Read the full docs at: https://docs.verifai.com/

## Contributions

 * Photo of Groningen (sample\_images/not\_id.jpg) by Sjaak Kempe CC - from [Flickr](https://flic.kr/p/YEXuY1)
