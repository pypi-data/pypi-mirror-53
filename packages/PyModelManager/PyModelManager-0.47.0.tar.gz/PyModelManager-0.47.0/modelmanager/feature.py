from .model_manager_object import ModelManagerObject


class FeatureRegistry(ModelManagerObject):

    def _use_attributes(self, attributes):
        pass

    def all(self):
        status, data = self._requester.request_json_and_check(
            'GET',
            '/features'
        )

        return [
            Feature(self._requester, item)
            for item in data
        ]

    def get(self, id):
        status, data = self._requester.request_json_and_check(
            'GET',
            '/features/%s' % id
        )

        return Feature(self._requester, data)

    def create(self, name, description):
        payload = {
            'name': name,
            'description': description
        }

        status, data = self._requester.request_json_and_check(
            'POST',
            '/features',
            input=payload
        )

        return Feature(self._requester, data)

    def delete(self, feature):
        status, data = self._requester.request_json_and_check(
            'DELETE',
            '/features/%s' % feature.id()
        )

        return self


class Feature(ModelManagerObject):

    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def tags(self):
        return self._tags

    def _use_attributes(self, attributes):
        self._id = attributes['id']
        self._name = attributes['name']
        self._description = attributes['description']
        self._tags = []

    def update(self):
        payload = {
            'name': self.name,
            'description': self.description,
            'tags': []
        }

        status, data = self._requester.request_json_and_check(
            'PATCH',
            '/features/%s' % self.id(),
            input=payload
        )

        self._use_attributes(data)

        return self
