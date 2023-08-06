#!/usr/bin/python

# -*- coding: utf-8 -*-

# Started from https://sketchfab.com/developers/data-api/v3/python
# The code was not compatible with the API and wrong by *many* standards.
# Requires python 3.7+

# There are basically 3 classes:
# - The models
# - The API management
# - The client that handle everything
import json
import logging
import os

from typing import List, Optional
import requests.auth

from sketchfab.api import SketchFabModelApi, SketchFabCollectionApi
from sketchfab.model import SFCollection, SFModel


class SFCltAuth(requests.auth.AuthBase):
    """
    Authentication handling
    """

    def __init__(self, token: str):
        self.token = token

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        r.headers['Authorization'] = f'Token {self.token}'
        return r


class SFClient:
    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.getenv('SKETCHFAB_APIKEY')

        if not api_key:
            conf_file = os.path.join(os.getenv('HOME'), '.sketchfabclient')
            if os.path.isfile(conf_file):
                logging.info("Loading api key from %s", conf_file)
                with open(conf_file) as f:
                    j = json.load(f)
                    api_key = j.get('apikey')

        if not api_key:
            raise RuntimeError("You need to pass an API key or define the SKETCHFAB_APIKEY env var.")

        self.auth = SFCltAuth(api_key)

    def models(self, sort_by: str = '-created_at', downloadable: bool = None) -> List[SFModel]:
        return SketchFabModelApi.list(self, sort_by=sort_by, downloadable=downloadable)

    def collections(self) -> List[SFCollection]:
        return SketchFabCollectionApi.list(self)

    def create_collection(self, name: str, models: List[SFModel]) -> SFCollection:
        return SketchFabCollectionApi.create(self, name, models)

    def get_collection(self, name: str) -> Optional[SFCollection]:
        for c in self.collections():
            if c.name == name:
                return c
        return None
