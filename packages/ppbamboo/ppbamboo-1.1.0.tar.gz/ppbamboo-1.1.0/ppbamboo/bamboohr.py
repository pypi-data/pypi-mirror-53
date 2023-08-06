# -*- coding: utf-8 -*-
"""This module implements communication with BambooHR.

Author: Peter Pakos <peter.pakos@wandisco.com>

Copyright (C) 2018 WANdisco
"""

from __future__ import print_function
import base64
import xml.etree.ElementTree
import logging

try:
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request

log = logging.getLogger(__name__)


class BambooHR(object):
    def __init__(self, url, api_key):
        log.debug('Initialising BambooHR API (%s)' % url)
        self._directory = {}
        self._url = url
        self._api_key = api_key

    def get_directory(self):
        if not self._directory:
            self._fetch_directory()
        return self._directory

    def _fetch(self, url):
        log.debug('Request %s' % self._url + url)
        request = urllib_request.Request(self._url + url)
        base64string = base64.b64encode(('%s:x' % self._api_key).encode('utf8')).decode('utf8')
        request.add_header('Authorization', 'Basic %s' % base64string)
        result = None
        try:
            result = urllib_request.urlopen(request)
        except urllib_request.HTTPError as err:
            log.error('Failed to fetch Bamboo data (HTTP Error Code %s)' % err.code)
        except urllib_request.URLError as err:
            log.error('Failed to fetch Bamboo data (URL Error %s)' % err.reason)
        except ValueError:
            log.error('Failed to fetch Bamboo data (Incorrect API URL)')
        return xml.etree.ElementTree.fromstring(result.read())

    def _fetch_directory(self):
        log.debug('Fetching employee directory')
        directory = self._fetch("/directory/")
        for employee in directory.iter('employee'):
            fields = {}
            for field in employee.iter('field'):
                fields[field.attrib['id']] = field.text.strip() if field.text else ''
            self._directory.update({employee.attrib['id']: fields})
        n = len(self._directory)
        if n == 0:
            log.debug('Bamboo data set is empty')
        else:
            log.debug('Fetched %s records' % n)

    def fetch_field(self, bamboo_id, bamboo_fields):
        if type(bamboo_fields) is not list:
            bamboo_fields = [bamboo_fields]
        log.debug('Fetching record id %s, fields: %s' % (bamboo_id, ', '.join(bamboo_fields)))
        result = {}
        fields = self._fetch("/%s?fields=%s" % (bamboo_id, ','.join(bamboo_fields)))
        for f in fields.iter('field'):
            field_id = f.attrib['id']
            field_text = f.text.strip() if f.text else ''
            result[field_id] = field_text
        if len(bamboo_fields) == 1 and len(result) == 1:
            return result[bamboo_fields[0]]
        else:
            return result

    def find_accounts_by_email(self, email):
        log.debug('Looking for accounts with email address: %s' % email)
        ids = []
        for bamboo_id, bamboo_fields in self.get_directory().items():
            if bamboo_fields.get('workEmail') == email:
                ids.append(bamboo_id)
        n = len(ids)
        log.debug('Found %s account%s with email address %s: %s' % (n, '' if n == 1 else 's', email, ', '.join(ids)))
        return ids
