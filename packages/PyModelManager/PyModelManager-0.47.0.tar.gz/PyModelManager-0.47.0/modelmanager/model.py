from .model_manager_object import ModelManagerObject


def feature(name, description=None):
    return {
        'name': name,
        'description': description or ''
    }


class ModelMetric(ModelManagerObject):

    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    def _use_attributes(self, attributes):
        self._id = attributes['id']
        self._model_id = attributes['model_id']
        self._name = attributes['name']
        self._value = attributes['value']
        self._description = attributes['description']

    def delete(self):
        pass

    def update(self):
        pass


class ModelCharacteristics(ModelManagerObject):

    @property
    def metrics(self):
        return self._metrics

    def _use_attributes(self, attributes):
        self._model_id = attributes['model_id']
        self._metrics = attributes['metrics']

    def update(self):
        pass


class Model(ModelManagerObject):

    @property
    def id(self):
        return self._id

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value

    @property
    def characteristics(self):
        return self._characteristics

    @characteristics.setter
    def characteristics(self, value):
        self._characteristics = value

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        self._features = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    def _use_attributes(self, attributes):
        self._id = attributes['id']
        self._project_id = None
        self._author = attributes['author']
        self._name = attributes['name']
        self._title = attributes['title']
        self._description = attributes['description']
        self._algorithm = attributes['algorithm']
        self._characteristics = attributes['characteristics']
        self._features = attributes['features']
        self._label = attributes['label']

    def upload(self, file):
        status, data = self._requester.request_files_and_check(
            'POST',
            '/models/%s/upload' % self.id,
            ('file', file)
        )

        return self

    def download(self):
        status, data = self._requester.request_blob(
            'GET',
            '/models/%s/download' % self.id
        )

        return data

    def update(self):
        payload = {}

        status, data = self._requester.request_json_and_check(
            'UPDATE',
            '/models/%s' % self.id,
            payload
        )

        return data

    def delete(self):
        status, data = self._requester.request_json_and_check(
            'DELETE',
            '/models/%s' % self.id
        )

        return data

    def __str__(self):
        return 'Model[id=%s]' % self.id





