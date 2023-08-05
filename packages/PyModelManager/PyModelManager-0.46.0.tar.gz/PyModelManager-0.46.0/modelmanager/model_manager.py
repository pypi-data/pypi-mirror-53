from .requester import Requester
from .project import Project
from .feature import FeatureRegistry


class ModelManager(object):
    def __init__(self, base_url=None, login=None, password=None) -> None:
        super().__init__()

        self._requester = Requester(base_url, login, password)

    def get_projects(self):
        # status, data = self.__requester.request_json_and_check(
        #     'GET',
        #     '/projects'
        # )

        return [
            Project(self._requester, {})
        ]

    def get_feature_registry(self):
        return FeatureRegistry(self._requester)
