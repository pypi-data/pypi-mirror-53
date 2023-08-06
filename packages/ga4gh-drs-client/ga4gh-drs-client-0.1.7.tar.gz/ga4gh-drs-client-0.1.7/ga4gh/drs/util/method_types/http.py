# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.method_types.http.py
Contains the HTTP class, a child of MethodType. HTTP contains submethods to 
download DRS object bytes according to the http url scheme.
"""

from ga4gh.drs.exceptions.drs_exceptions import DownloadSubmethodException
from ga4gh.drs.util.method_types.method_type import DownloadSubmethod
from ga4gh.drs.util.method_types.method_type import MethodType

class HTTP(MethodType):
    """Download DRS object bytes according to http url scheme

    Attributes:
        download_submethods (list): multiple methods to attempt byte download
    """

    def __init__(self, json, drs_obj):
        """Instantiates an HTTP object

        Arguments:
            json (dict): parsed AccessMethod JSON, used to set other attributes
            drs_obj (DRSObject): reference to parent DRSObject object
        """

        super(HTTP, self).__init__(json, drs_obj)
        self.download_submethods = [
            self.__download_by_http
        ]

    @DownloadSubmethod()
    def __download_by_http(self, write_config):
        """Download submethod, get object bytes by http

        Arguments:
            write_config (dict): config to write downloaded file
        """

        url = self.access_url.get_url()
        self._MethodType__download_by_requests_package(url, write_config)
