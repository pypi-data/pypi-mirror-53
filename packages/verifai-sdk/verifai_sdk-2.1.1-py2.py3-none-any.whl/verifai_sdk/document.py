import io
from PIL import Image, ImageColor, ImageDraw


ID_FRONT = 'F'
ID_BACK = 'B'


class VerifaiDocument:
    """
    Once a classification has taken place the VerifaiService will
    return a instance of this class.

    It represents the data we collected for you, and provides several
    operations like getting additional information and getting a cropped
    image of the document.

    Some operations require communication to external services.
    Everything is lazy, and will be collected upon request. When that
    has happened it will be cached in memory as long as the object
    lives.

    """
    service = None
    id_uuid = None
    id_side = None
    coordinates = None

    image = None
    cropped_image = None

    def __init__(self, response, b_jpeg_image, service):
        self.service = service
        if response:
            self.set_model_data(
                response['uuid'], response['side']
            )
            self.set_coordinates(
                response['coords']['xmin'],
                response['coords']['ymin'],
                response['coords']['xmax'],
                response['coords']['ymax']
            )

        self.load_image(b_jpeg_image)
        self.__model_data = None
        self.__zones = None
        self.__mrz = None
        self.__security_features_data = None
        self.__security_features = None

    def set_model_data(self, id_uuid, id_side):
        """
        To set the model data manually. For example when using a manual
        flow fallback. This way you are still able to use the other
        functions of Verifai.
        :param id_uuid: The UUID of the model
        :type id_uuid: str
        :param id_side: The side of the model F or B
        :type id_side: str
        """
        self.id_uuid = id_uuid
        self.id_side = id_side

    def set_coordinates(self, xmin, ymin, xmax, ymax):
        """
        To set the coordinates of the document location in the image
        manually. For example, you could make a interface that lets
        the user draw the bounding box around the document in an image.
        :param xmin: xmin
        :type xmin: float
        :param ymin: ymin
        :type ymin: float
        :param xmax: xmax
        :type xmax: float
        :param ymax: ymax
        :type ymax: float
        """
        self.coordinates = {
            'xmin': float(xmin),
            'ymin': float(ymin),
            'xmax': float(xmax),
            'ymax': float(ymax)
        }

    @property
    def model(self):
        """
        :return: Returns the model name.
        :rtype: str
        """
        return self.get_model_data()['model']

    @property
    def country(self):
        """
        :return: Returns the Alpha-2 county code. For example "NL"
        :rtype: str
        """
        return self.get_model_data()['country']

    @property
    def position_in_image(self):
        """
        :return: Return the coordinates where te document is located.
        :rtype: dict
        """
        return self.coordinates

    def load_image(self, b_jpeg_image):
        """
        Load filecontents into the object, and use that as image.

        :param b_jpeg_image: image data bytes
        """
        f = io.BytesIO(b_jpeg_image)
        self.image = Image.open(f)

    def get_cropped_image(self):
        """
        Cuts out the document form the entire image and returns the
        cropped image.
        :return: cropped image
        :rtype: Image
        """
        if self.cropped_image is not None:
            return self.cropped_image
        px_coords = self.get_bounding_box_pixelcoords(self.coordinates)
        px_coords = self.__coordinates_list(px_coords)
        self.cropped_image = self.image.crop(px_coords)
        return self.cropped_image

    def get_part_of_card_image(self, coordinates, tolerance=0):
        """
        Every document consists of a lot of parts. You can get some
        parts of the document by giving the coordinates.
        It returns a new Image object.

        :param coordinates: xmin, ymin, xmax, ymax coordinates
        :type coordinates: dict
        :param tolerance: The extra spacing around the image. .03 being 3%
        :type tolerance: float
        :return: part of the image
        :rtype: Image
        """
        i = self.get_cropped_image()
        if tolerance > 0:
            coordinates = self.inflate_coordinates(coordinates, tolerance)
        px_coords = self.get_bounding_box_pixelcoords(coordinates, i.width, i.height)
        px_coords = self.__coordinates_list(px_coords)
        return i.crop(px_coords)

    def inflate_coordinates(self, coordinates, factor):
        """
        Inflates the coordinates with the factor. It makes sure you
        can't inflate it more than the document is in size.

        :param coordinates: xmin, ymin, xmax, ymax coordinates
        :type coordinates: dict
        :param factor: the extra spacing around the image. .03 being 3%
        :type factor: float
        :return: xmin, ymin, xmax, ymax coordinates
        :rtype: dict
        """

        new_coords = {
            'xmin': coordinates['xmin'] - factor,
            'ymin': coordinates['ymin'] - factor,
            'xmax': coordinates['xmax'] + factor,
            'ymax': coordinates['ymax'] + factor,
        }
        for key, value in new_coords.items():
            if value < 0:
                new_coords[key] = 0
            if value > 1:
                new_coords[key] = 1
        return new_coords

    def get_bounding_box_pixelcoords(
            self, float_coords, im_width=None, im_height=None
    ):
        """
        Get the pixel coords based on the image and the inference
        result.

        :return: dict with the bounding box in pixels
        :rtype: dict
        """
        if im_width is None and im_height is None:
            im_width = self.image.width
            im_height = self.image.height

        response = {
            'xmin': int(im_width * float_coords['xmin']),
            'ymin': int(im_height * float_coords['ymin']),
            'xmax': int(im_width * float_coords['xmax']),
            'ymax': int(im_height * float_coords['ymax'])
        }
        return response

    @property
    def zones(self):
        """
        :return: Returns a list of VerifaiDocumentZone objects.
        :rtype: [VerifaiDocumentZone]
        """
        if self.__zones is None:
            data = self.get_model_data()
            self.__zones = []
            if data:  # If there is no data available
                for zone_data in data['zones']:
                    self.__zones.append(
                        VerifaiDocumentZone(self, zone_data)
                    )
        return self.__zones

    def get_actual_size_mm(self):
        """
        :return: Returns the width and height in mm of the document.
        :rtype tuple (width_mm, height_mm)
        """
        data = self.get_model_data()
        return float(data['width_mm']), float(data['height_mm'])

    def get_model_data(self):
        """
        :return: Returns the raw model data via the VerifaiService
        :rtype: dict
        """
        if not self.__model_data:
            self.__model_data = self.service.get_model_data(
                self.id_uuid
            )
        return self.__model_data

    def mask_zones(self, zones, image=None, filter_sides=True):
        """
        Function to mask zones and return the masked image.

        It takes a list of VerifaiDocumentZone objects, and draws black
        squares on the coordinates of the zone.

        By default it filters out the zones that are for the other side.

        :param zones: list of VerifaiDocumentZone objects
        :type zones: list
        :param image: Optional image to apply the masking to
        :type image: Image
        :param filter_sides: Weather or not to apply side-filters
        :type filter_sides: bool
        :return: Resulting masked image
        :rtype: Image
        """
        if image is None:
            image = self.get_cropped_image()
        c = ImageColor.getrgb('#000000')
        drawer = ImageDraw.Draw(image)
        for zone in zones:
            if filter_sides and zone.side != self.id_side:
                continue
            px_coords = self.get_bounding_box_pixelcoords(
                zone.coordinates, image.width, image.height
            )
            px_coords = self.__coordinates_list(px_coords)
            drawer.rectangle(px_coords, c)

        return image

    @property
    def mrz_zone(self):
        """
        Returns the zone that holds the MRZ.

        :return: Zone or None
        :rtype: VerifaiDocumentZone, None
        """
        for zone in self.zones:
            if zone.is_mrz:
                return zone
        return None

    @property
    def mrz(self):
        """
        Returns the VerifaiDocumentMrz object of the mrz_zone.

        :return: a VerifaiDocumentMrz object
        :rtype: VerifaiDocumentMrz, None
        """
        if not self.mrz_zone:
            return None
        if not self.__mrz:
            self.__mrz = VerifaiDocumentMrz(self.mrz_zone)
        return self.__mrz

    @property
    def security_features(self):
        """
        Returns a list of VerifaiDocumentSecurityFeatureZone
        objects.

        :return: list of VerifaiDocumentSecurityFeatureZone objects
        :rtype: [VerifaiDocumentSecurityFeatureZone]
        """
        if self.__security_features is None:
            data_list = self.get_security_features_data()
            self.__security_features = []
            if data_list:  # If there is no data available
                for zone_data in data_list:
                    self.__security_features.append(
                        VerifaiDocumentSecurityFeatureZone(
                            self, zone_data
                        )
                    )
        return self.__security_features

    def get_security_features_data(self):
        """
        Fetches the raw security features data from the API
        and stores them in memory.

        :return: Raw dict from the API
        :rtype: dict
        """
        if not self.__security_features_data:
            self.__security_features_data = \
                self.service.get_security_features(self.id_uuid)
        return self.__security_features_data

    def __coordinates_list(self, coordinates):
        """
        Helper to make a PIL coordnates list

        :param coordinates: xmin-max ymin-max coords
        :type coordinates: dict
        :return: tuple of coords
        :rtype: tuple (xmin, ymin, xmax, ymax)
        """
        return (coordinates['xmin'], coordinates['ymin'],
                coordinates['xmax'], coordinates['ymax'])


class VerifaiDocumentZoneAbstract:
    """
    There are several types of zones, Data zones and Security Feature
    zones. All types of zones inherit from this abstract.
    """
    document = None
    side = None
    coordinates = None

    def __init__(self, document, side, x, y, width, height):
        """
        Initialize zone
        :param document: The parent VerifaiDocument
        :type document: VerifaiDocument
        :param side: Side of the document
        :type side: str
        :param x: xmin of the zone
        :type x: float
        :param y: ymin of the zone
        :type y: flat
        :param width: width of the zone in factor / percentage
        :type width: float
        :param height: height of the zone in factor / percentage
        :type height: float
        """
        self.document = document
        self.set_side(side)
        self.set_coordinates(x, y, width, height)

    def set_side(self, side):
        """
        Change and set the side of the zone.
        :param side: F for front, and B for back
        :type side: str
        :return: None
        """
        self.side = side[:1]

    def set_coordinates(self, xmin, ymin, width, height):
        """
        Since the coordinate system of the zones is different this
        method converts it to the xmin, ymin, xmax, ymax system.
        :param xmin: xmin
        :type xmin: float
        :param ymin: ymin
        :type ymin: float
        :param width: width
        :type width: float
        :param height: height
        :type height: float
        :return: None
        """
        width_mm, height_mm = self.document.get_actual_size_mm()

        mm_xmin = xmin * width_mm
        mm_ymin = ymin * height_mm

        mm_xmax = mm_xmin + (width_mm * width)
        mm_ymax = mm_ymin + (height_mm * height)

        xmax = mm_xmax / width_mm
        ymax = mm_ymax / height_mm

        self.coordinates = {
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax
        }


class VerifaiDocumentZone(VerifaiDocumentZoneAbstract):
    """
    VerifaiDocument objects contain zones, and the zones are represented
    by this class.

    Every zone has a position in the form of coordinates, a title, and
    some operations.
    """
    title = None

    def __init__(self, document, zone_data):
        """
        Initialize zone
        :param document: The parent VerifaiDocument
        :type document: VerifaiDocument
        :param zone_data: raw data about the zone form the Verifai Backend
        :type zone_data: dict
        """
        super(VerifaiDocumentZone, self).__init__(
            document,
            zone_data['side'],
            zone_data['x'],
            zone_data['y'],
            zone_data['width'],
            zone_data['height']
        )
        self.title = zone_data['title']

    @property
    def is_mrz(self):
        """
        :return: Return if this zone is the Machine Readable Zone.
        :rtype: bool
        """
        if self.title.upper() == 'MRZ':
            return True
        return False

    @property
    def position_in_image(self):
        """
        :return: xmin, ymin, xmax, ymax coordinates dict.
        :rtype: dict
        """
        return self.coordinates


class VerifaiDocumentSecurityFeatureZone(VerifaiDocumentZoneAbstract):
    """
    Most documents have security features. They are available through
    the backend.
    They extend from zones because they always have a location on the
    document. Sometimes they cover the whole document.
    """
    score = 0
    reference_image = None
    type = None
    properties = {}
    check_type = None
    check_question = None

    def __init__(self, document, zone_data):
        super(VerifaiDocumentSecurityFeatureZone, self).__init__(
            document,
            zone_data['side'],
            zone_data['x'],
            zone_data['y'],
            zone_data['width'],
            zone_data['height']
        )
        self.score = zone_data['score']
        self.reference_image = zone_data['security_feature']['reference_image']
        self.type = zone_data['security_feature']['type']
        self.check_type = zone_data['security_feature']['check_type']
        self.check_type = zone_data['security_feature']['check_question']

        for item in zone_data['security_feature']['properties']:
            self.properties[item[0]] = item[1]


class VerifaiDocumentMrz:
    """
    Modern document have a Machine Readable Zone. This class is the
    proxy between your code and the Verifai OCR service. You can get
    an instance of this class from the VerifaiDocument object.

    You can create one by initializing it with a VerifaiDocumentZone
    that contains a MRZ.
    """
    zone = None

    def __init__(self, zone):
        """
        Initialize the object with a zone
        :param zone: the MRZ zone
        :type zone: VerifaiDocumentZone
        """
        self.zone = zone
        self.__mrz_response = None

    @property
    def is_successful (self):
        """
        :return: Returns whether the OCR has been successful.
        :rtype: bool
        """
        return self.read_mrz()['status'] == 'SUCCESS'

    def read_mrz(self):
        """
        :return: Returns the raw OCR response from the OCR service.
        :rtype: dict
        """
        if self.__mrz_response:
            ocr_result = self.__mrz_response
        else:
            mrz = self.zone
            mrz_image = self.__document.get_part_of_card_image(mrz.coordinates, .03)
            ocr_result = self.__service.get_ocr_data(mrz_image)
            self.__mrz_response = ocr_result
        if ocr_result['status'] == 'NOT_FOUND':
            return None
        return ocr_result

    @property
    def fields(self):
        """
        :return: Returns the fields form the MRZ.
        :rtype: dict
        """
        if self.is_successful:
            return self.read_mrz()['result']['fields']
        return None

    @property
    def fields_raw(self):
        """
        :return: Returns the raw fields form the MRZ.
        :rtype: dict
        """
        if self.is_successful:
            return self.read_mrz()['result']['fields_raw']
        return None

    @property
    def checksums(self):
        """
        :return: Returns the checksum results for the MRZ.
        :rtype: dict
        """
        if self.is_successful:
            return self.read_mrz()['result']['checksums']
        return None

    @property
    def rotation(self):
        """
        :return: Returns the rotation that was required to read the MRZ.
        :rtype: float
        """
        if self.is_successful:
            return self.read_mrz()['rotation']
        return None

    @property
    def __document(self):
        return self.zone.document

    @property
    def __service(self):
        return self.zone.document.service


