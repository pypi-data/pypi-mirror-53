import subprocess
import tempfile
import os.path
from os import listdir
import re
import shutil


class VerifaiPdfProcessor:
    """
    A wrapper around the Verifai features so you can use it with multi-
    page PDF documents.

    It uses a service and the ImageMagick commandline tool.
    """
    service = None
    image_magick_convert_binary = 'magick'
    density = 300
    __jpegs = []
    __tmp = None

    def __init__(self, path_to_file=None, service=None):
        self.__jpegs = []
        __tmp = None

        if path_to_file:
            self.__convert_to_jpegs(path_to_file)

        if service:
            self.service = service

    def __get_tmp(self):
        if not self.__tmp:
            self.__tmp = tempfile.gettempdir()
        return self.__tmp

    def __convert_to_jpegs(self, path_to_file):
        options = {
            'command': self.image_magick_convert_binary,
            'density': self.density,
            'pdf': path_to_file,
            'output': os.path.join(self.__get_tmp(), 'output-%d.jpeg')
        }
        command = "{command} {pdf} -trim -density {density} {output}"
        subprocess.run(command.format(**options), shell=True)

        listing = listdir(self.__get_tmp())
        pattern = re.compile("^output-[0-9]+.jpeg$")
        for item in listing:
            if pattern.match(item):
                self.__jpegs.append(item)
        self.__jpegs.sort()

    def get_nuber_of_pages(self):
        """
        :return: Number of pages that the PDF document has
        :rtype: int
        """
        return len(self.__jpegs)

    def get_result_for_page(self, page):
        """
        This is a wrapper around `service.classify_image_path()` with
        the exported JPEG image from a page.
        :param page: the page you want to analyze
        :type page: int
        :return: VerifaiDocument, confidence
        :rtype: tuple (VerifaiDocument, float)
        """
        jpeg_path = os.path.join(self.__get_tmp(), self.__jpegs[page])
        document, confidence = self.service.classify_image_path(jpeg_path)
        return document, confidence

    def get_results_for_all_pages(self):
        """
        This is a wrapper around `get_result_for_page()` that returns the
        results as a list of tuples
        :return: list of tuple resuts from `get_result_for_page()`
        :rtype: list
        """
        results = []
        for page in range(self.get_nuber_of_pages()):
            results.append(self.get_result_for_page(page))
        return results

    def cleanup(self):
        """
        Should not be forgotten to call, otherwise it leaves stuff in
        a temp folder.
        :return: nothing
        """
        if self.__tmp and os.path.exists(self.__tmp):
            shutil.rmtree(self.__tmp)

    def __del__(self):
        self.cleanup()
