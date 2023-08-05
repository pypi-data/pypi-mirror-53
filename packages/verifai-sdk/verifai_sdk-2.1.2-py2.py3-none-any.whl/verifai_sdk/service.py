import io
import requests

from PIL import Image

from verifai_sdk.document import VerifaiDocument
from verifai_sdk.id_model import IdModel


class VerifaiService:
    """
    The VerifaiService is your main component to use. It communicates
    with various backend systems and handles all the privacy sensitive
    data internally.

    To use the service you need to initialize it first with a API token
    and the URL to the classifier service, and optional to the OCR
    service.

    See https://docs.verifai.com/server_docs/python-sdk-latest.html
    """
    api_token = None
    server_urls = {'classifier': [], 'ocr': []}
    base_api_url = 'https://dashboard.verifai.com/api/'
    ssl_verify = True

    def __init__(self, token=None):
        """
        Initialize the VerifaiService with a token. A token is mandatory
        to communicate with the Verifai backend services.

        :param token: API token, can be found in the Verifai Dashboard.
        :type token: str
        """
        self.__url_roundrobin = {'classifier': 0, 'ocr': 0}
        self.api_token = token

    def add_classifier_url(self, url, skip_unreachable=False):
        """
        To add the URL to your local running Verifai Classifier service.
        Please not that you need to provide the full path to the api
        endpoint.

        For example: http://localhost:5000/api/classify/

        You can add multiple servers to scale up operations.

        :param url: The full path to the classifier API
        :type url: str
        :param skip_unreachable: Ignore errors in connecting to it.
        :type skip_unreachable: bool
        :return: True if add is successful, False if it doesn't.
        :rtype: bool
        """
        return self.__add_server_url(url, skip_unreachable, 'classifier')

    def add_ocr_url(self, url, skip_unreachable=False):
        """
        To add the URL to your local running Verifai OCR service.
        Please not that you need to provide the full path to the api
        endpoint.

        For example: http://localhost:5001/api/ocr/

        You can add multiple servers to scale up operations.
        :param url: The full path to the classifier API
        :type url: str
        :param skip_unreachable: Ignore errors in connecting to it.
        :type skip_unreachable: bool
        :return: True if add is successful, False if it doesn't.
        :rtype: bool
        """
        return self.__add_server_url(url, skip_unreachable, 'ocr')

    def get_model_data(self, id_uuid):
        """
        Fetch the raw data from the API for further processing.

        Note: Since it is not a public API it is subject to changes.

        :param id_uuid: The UUID you got form the classifier
        :type id_uuid: str
        :return: dict with the results found in the Verifai Backend
        :rtype: dict or None
        """
        data = self.__get_from_api('id-models', params={'uuid': id_uuid})
        if data:
            return data[0]  # Get first result because a unique key is queried
        return None

    def get_ocr_data(self, mrz_image):
        """
        Sends the mrz_image (Image) to the Verifai OCR service, and
        returns the raw response.

        :param mrz_image: MRZ cutout of the document
        :type mrz_image: Image
        :return: dict with raw response or None of not response
        :rtype: dict or None
        """
        bytes_io = io.BytesIO()
        mrz_image.save(bytes_io, 'JPEG')
        r = requests.post(
            self.__get_url('ocr'),
            files={'file': bytes_io.getvalue()},
            verify=self.ssl_verify
        )
        response = r.json()
        return response

    def classify_image(self, image):
        """
        Send a image to the Verifai Classifier and get a VerifaiDocument
        in return. If it fails to classify it will return None.

        :param image: file contents of a JPEG image
        :type image: str
        :return: Initialized VerifaiDocument
        :rtype: tuple (VerifaiDocument, confidence), tuple (None, None)
        """
        r = requests.post(
            self.__get_url('classifier'),
            files={'file': image},
            verify=self.ssl_verify
        )
        response = r.json()
        if response['status'] == 'SUCCESS':
            return VerifaiDocument(response, image, self), float(response['confidence'])

        return None, 0.0

    def classify_image_path(self, image_path):
        """
        Send a image to the Verifai Classifier and get a VerifaiDocument
        in return. If it fails to classify it will return None.

        :param image_path: Path to the image
        :type image_path: str
        :return: Initialized VerifaiDocument
        :rtype: tuple (VerifaiDocument, confidence), None
        """
        f = open(image_path, 'rb')
        i = f.read()
        return self.classify_image(i)

    def classify_pil_image(self, image):
        """
        Wraper around `classify_image` that converts the image to a jpeg
        before sending it to the classifier.

        :param image: A PIL Image
        :type image: Image
        :return: Initialized VerifaiDocument
        :rtype: tuple (VerifaiDocument, confidence), tuple (None, None)
        """
        jpeg_image = io.BytesIO()
        image.save(jpeg_image, 'jpeg')
        return self.classify_image(jpeg_image.getvalue())


    def get_supported_countries(self):
        """
        Fetches the list of supported countries. It is based on all the
        document types registerd in the backend of Verifai.

        Example:
        [{'code': 'AD', 'flag': '🇦🇩', 'name': 'Andorra'}, ... ]

        :return: list of dicts
        :rtype: list
        """
        results = self.__get_from_api('id-model-countries', None)
        return results

    def get_id_models_for_country(self, country):
        """
        Gets a list of IdModel objects for that specific country. It
        can be used to make nice listings of documents for manual
        processing of data.

        :param country: ALPHA-2 country name, for example: NL or US
        :type country: str
        :return: list of IdModel objects
        :rtype: list
        """
        results = self.__get_from_api('id-models', {'country': country})
        idmodels = []
        for result in results:
            idmodels.append(IdModel(result))
        return idmodels

    def get_id_models(self, country=None, mrz_start=None):
        """
        Gets a list of IdModel objects, which can be further filtered by country or first 5 MRZ characters

        :param country: ALPHA-2 country name, for example: NL or US
        :type country: str
        :param mrz_start: first 5 characters of the MRZ
        :type mrz_start: str
        :return: list of IdModel objects
        :rtype: list
        """

        query = {}
        if country:
            query['country'] = country

        if mrz_start:
            query['mrz_start'] = mrz_start

        results = self.__get_from_api('id-models', query)
        idmodels = []
        for result in results:
            idmodels.append(IdModel(result))
        return idmodels

    def get_id_model(self, uuid):
        """
        Get the details of one specific document. This is useful when
        you want to lookup just one IdModel from the backend and you
        already know the UUID of that IdModel.

        :param uuid: UUID of the IdModel
        :type uuid: str
        :return: The found IdModel
        :rtype: IdModel
        """
        results = self.__get_from_api('id-models', {'uuid': uuid})
        if results:
            return IdModel(results[0])
        return None

    def get_security_features(self, uuid):
        """
        Get a list of security features from the backend.

        :param uuid: UUID of the IdModel
        :type uuid: str
        :return: list of Security Features
        :rtype: list of dicts
        """
        results = self.__get_from_api('id-model-security-features', {
            'id_model': uuid
        })
        return results

    def __add_server_url(self, url, skip_unreachable, type):
        try:
            self.__check_server_url(url)

            if type == 'classifier':
                self.server_urls[type].append(url)
            else:
                self.server_urls[type].append(url)
            return True
        except AssertionError:
            if not skip_unreachable:
                raise ValueError('No server available at that URL ({0})'.format(url))
            return False

    def __get_url(self, type):
        index = self.__url_roundrobin[type]
        if self.server_urls[type][index]:
            if index + 1 >= len(self.server_urls[type]):
                self.__url_roundrobin[type] = 0
            else:
                self.__url_roundrobin[type] = index + 1
            return self.server_urls[type][index]
        raise ValueError("No clasifier URLs. Set one first with add_classifier_url(url)")

    def __get_from_api(self, path, params):
        headers = {
            'Authorization': 'Token ' + self.api_token
        }
        r = requests.get(self.base_api_url + path, headers=headers, params=params, verify=self.ssl_verify)
        if r.status_code == 200:
            return r.json()
        r.raise_for_status()

    def __check_server_url(self, url):
        try:
            r = requests.options(url, verify=self.ssl_verify)
        except requests.exceptions.ConnectionError:
            raise AssertionError('No connection possible for ' + url)
        if not r.status_code == 200:
            raise AssertionError('Got a {0} for {1}'.format(r.status_code, url))
        methods = r.headers['allow'].replace(' ', '').split(',')
        assert 'OPTIONS' in methods
        assert 'POST' in methods
        return True
