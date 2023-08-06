from pathlib import Path
from typing import Dict, Any, List


class SFModel:
    """
    3D Model
    https://docs.sketchfab.com/data-api/v3/index.html#/models
    """

    def __init__(self, j: Dict[str, Any] = None, clt: 'SketchFabClient' = None):
        """
        Constructor
        :param j: json data
        :param clt: Client
        """
        self.json = j if j else {}
        self.clt = clt

    @property
    def name(self) -> str:
        return self.json.get('name')

    @property
    def uid(self) -> str:
        return self.json.get('uid')

    @property
    def viewer_url(self) -> str:
        return self.json.get('viewerUrl')

    def comment(self, msg: str):
        from sketchfab.api import SketchFabModelApi
        return SketchFabModelApi.comment(self.clt, self, msg)

    def download(self) -> str:
        from sketchfab.api import SketchFabModelApi
        return SketchFabModelApi.download(self.clt, self)

    def download_to_dir(self) -> str:
        from sketchfab.api import SketchFabModelApi
        return SketchFabModelApi.download_to_dir(self.clt, self)

    def __str__(self) -> str:
        return f'Model{{{self.name}}}'


class SFCollection:
    """
    Collection of models
    https://docs.sketchfab.com/data-api/v3/index.html#/collections
    """

    def __init__(self, j: Dict[str, Any] = None, clt: 'SketchFabClient' = None):
        self.json = j if j else {}
        self.clt = clt

    @property
    def name(self) -> str:
        return self.json.get('name')

    @property
    def uid(self) -> str:
        return self.json.get('uid')

    def models(self) -> List[SFModel]:
        """
        Fetch the models of the collection
        :return:
        """
        from sketchfab.api import SketchFabCollectionApi
        return SketchFabCollectionApi.list_models(self.clt, self)

    def add_model(self, model: SFModel) -> bool:
        """
        Add a model to a collection
        :param model: Model to add
        :return: If the model could be added
        """
        from sketchfab.api import SketchFabCollectionApi
        return SketchFabCollectionApi.add_model(self.clt, self, model)

    def remove_model(self, model: SFModel) -> bool:
        from sketchfab.api import SketchFabCollectionApi
        return SketchFabCollectionApi.remove_model(self.clt, self, model)

    def __str__(self) -> str:
        return f'Collection{{{self.name}}}'
