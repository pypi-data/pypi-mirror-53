import logging
import os
import tempfile
import zipfile
from pathlib import Path
from typing import List

import requests

from sketchfab.model import SFModel, SFCollection

API_URL = 'https://api.sketchfab.com/v3'


class SketchFabModelApi:
    @staticmethod
    def comment(clt: 'SketchFabClient', model: SFModel, msg: str) -> bool:
        r = requests.post(
            f'{API_URL}/comments',
            json={'model': model.uid, 'body': msg},
            auth=clt.auth,
        )
        ok = r.status_code == requests.codes.created

        if not ok:
            logging.warning("Could not add comment to model %s: %s", model.uid, r.content)

        return ok

    @staticmethod
    def list(
            clt: 'SketchFabClient',
            sort_by: str = None,
            downloadable: bool = None,
            collection: SFCollection = None
    ) -> List[SFModel]:

        # Using a prepared request is the simplest way to build an URL
        req = requests.PreparedRequest()
        params = {
            'type': 'models',
        }
        if sort_by:
            params['sort_by'] = sort_by
        if downloadable is not None:
            params['downloadable'] = downloadable
        if collection:
            params['collection'] = collection.uid
        req.prepare_url(f'{API_URL}/me/search', params)
        data = requests.get(req.url, auth=clt.auth).json()
        return [SFModel(m, clt) for m in data['results']]

    @staticmethod
    def download(clt: 'SketchFabClient', model: SFModel) -> str:
        data = requests.get(f'{API_URL}/models/{model.uid}/download', auth=clt.auth).json()
        url_download = data['gltf']['url']
        with requests.get(url_download, stream=True) as r:
            r.raise_for_status()
            suffix = f'_{model.uid}'
            if r.headers.get('content-type') == 'application/zip':
                suffix += '.zip'
            _, path = tempfile.mkstemp(prefix='sketchfab_', suffix=suffix)
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            return path

    @staticmethod
    def download_to_dir(clt: 'SketchFabClient', model: SFModel) -> str:
        zf = SketchFabModelApi.download(clt, model)
        with zipfile.ZipFile(zf, 'r') as zip_ref:
            path = tempfile.mkdtemp(prefix='sketchfab_', suffix=f'_{model.uid}')
            zip_ref.extractall(path)
        os.remove(zf)
        return path


class SketchFabCollectionApi:
    @staticmethod
    def list(clt: 'SketchFabClient'):
        data = requests.get(f'{API_URL}/me/collections', auth=clt.auth).json()
        return [SFCollection(m, clt) for m in data['results']]

    @staticmethod
    def create(clt, name: str, models: List[SFModel]) -> 'SFCollection':
        r = requests.post(
            f'{API_URL}/collections',
            json={
                'name': name,
                'models': [m.uid for m in models]
            },
            auth=clt.auth,
        )
        r = requests.get(r.headers['Location'])
        return SFCollection(r.json())

    @staticmethod
    def add_model(clt, collection: SFCollection, model: SFModel) -> bool:
        r = requests.post(
            f'{API_URL}/collections/{collection.uid}/models',
            json={'models': [model.uid]},
            auth=clt.auth,
        )
        ok = r.status_code == requests.codes.created

        if not ok:
            logging.warning("Could not add model %s to collection %s: %s", model.uid, collection.uid, r.content)

        return ok

    @staticmethod
    def remove_model(clt, collection: SFCollection, model: SFModel) -> bool:
        r = requests.delete(
            f'{API_URL}/collections/{collection.uid}/models',
            json={'models': [model.uid]},
            auth=clt.auth,
        )
        ok = r.status_code == 204

        if not ok:
            logging.warning("Could not remove model %s from collection %s: %s", model.uid, collection.uid, r.content)

        return ok

    @staticmethod
    def list_models(clt: 'SketchFabClient', collection: SFCollection):
        return SketchFabModelApi.list(clt, collection=collection)

    @staticmethod
    def list_models_broken(clt: 'SketchFabClient', collection: SFCollection) -> List[SFModel]:
        """
        *Should* list all models of the collection but instead always returns an empty list
        :param clt: Client
        :param collection: Collection
        :return: List of models
        """
        data = requests.get(
            f'{API_URL}/collections/{collection.uid}/models',
            auth=clt.auth,
        ).json()
        return [SFModel(m, clt) for m in data['results']]
