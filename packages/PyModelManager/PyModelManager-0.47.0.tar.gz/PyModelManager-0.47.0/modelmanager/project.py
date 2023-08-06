from .model_manager_object import ModelManagerObject
from .model import Model


class Project(ModelManagerObject):

    def get_models(self):
        status, data = self._requester.request_json_and_check(
            'GET',
            '/models'
        )

        return [
            Model(self._requester, item)
            for item in data
        ]

    def get_model(self, id):
        status, data = self._requester.request_json_and_check(
            'GET',
            '/models/%s' % id
        )

        return Model(self._requester, data)

    def create_model(self, author, name, title,
                     description, algorithm, label,
                     features=None, characteristics=None, model_file=None):
        payload = {
            'author': author,
            'name': name,
            'title': title,
            'description': description,
            'algorithm': algorithm,
            'label': label,
            'features': features or [],
            'characteristics': characteristics or {}
        }

        status, data = self._requester.request_json_and_check(
            'POST',
            '/models',
            input = payload
        )

        model = Model(self._requester, data)
        if model_file:
            status, data = self._requester.request_files_and_check(
                'POST',
                '/models/%s/upload' % model.id,
                ('file', model_file)
            )

            print('status: {}, data: {}'.format(status, data))

        return model

    def _use_attributes(self, attributes):
        pass

    def __str__(self) -> str:
        return 'Project()'



