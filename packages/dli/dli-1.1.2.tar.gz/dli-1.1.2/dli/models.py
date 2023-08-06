import warnings
import contextlib

from collections.abc import Mapping

from dli.client.components.urls import dataset_urls


class AttributesDict(Mapping):

    def __init__(self, *args, **kwargs):
        # recurisvely provide the rather silly attribute
        # access
        data = {}

        for arg in args:
            data.update(arg)

        data.update(**kwargs)

        for key, value in data.items():
            if isinstance(value, Mapping):
                self.__dict__[key] = AttributesDict(value)
            else:
                self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def _asdict(self, *args, **kwargs):
        warnings.warn(
            'This method is deprecated as it returns itself.',
            DeprecationWarning
        )

        return self

    def __repr__(self):
        attributes = ' '.join([
            '{}={}'.format(k, v) for k,v in self.__dict__.items() 
            if not k.startswith('_')
        ])

        return "{}({})".format(self.__class__.__name__, attributes)



class Field(AttributesDict):
    pass


class SampleData:
    def __init__(self, parent):
        self._parent = parent
        self._client = parent._client

    def schema(self):
        """
        Returns the schema data and first rows of sample data.

        :returns: attributes dictionary
        """
        response = self._client.session.get(
            dataset_urls.v2_sample_data_schema.format(id=self._parent.id)
        )

        return AttributesDict(**response.json()['data']['attributes'])

    @contextlib.contextmanager
    def file(self):
        """
        Provides a file like object containing sample data.

        Example usage:

        .. code-block:: python

            dataset = self.client.get_dataset(dataset_id)
            with dataset.sample_data.file() as f:
                dataframe = pandas.read_csv(f)
        """
        response = self._client.session.get(
            dataset_urls.v2_sample_data_file.format(id=self._parent.id),
            stream=True
        )
        # otherwise you get raw secure
        response.raw.decode_content = True
        yield response.raw
        response.close()


class DatasetModel(AttributesDict):

    @property
    def sample_data(self):
        return SampleData(self)

    @property
    def id(self):
        return self.dataset_id

    def __init__(self, json, client=None):
        self._client = client

        location = json['attributes'].pop('location')

        if 's3' in location:
            location = location['s3']
        else:
            location = location['other']

        super().__init__(
            json['attributes'],
            dataset_id=json['id'],
            location=location
        )


class DictionaryModel(AttributesDict):

    @property
    def id(self):
        return self.dictionary_id

    @property
    def schema_id(self):
        warnings.warn(
            'This method is deprecated. Please use DictionaryModel.id',
            DeprecationWarning
        )
        return self.id

    def _get_fields(self):
        fields = []

        def _get_page(page=1):
            return self._client.session.get(
                dataset_urls.dictionary_fields.format(id=self.id),
                params={'page': page}
            ).json()

        fields_json = _get_page()
        fields.extend(fields_json['data']['attributes']['fields'])

        for page in range(2, fields_json['meta']['total_count']+1):
            fields.extend(
                _get_page(page=page)['data']['attributes']['fields']
            )

        return fields

    @property
    def fields(self):
        if 'fields' not in self.__dict__:
            self.__dict__['fields'] = self._get_fields()

        return self.__dict__['fields']

    def __init__(self, json, client=None):
        self._client = client
        super().__init__(
            json['attributes'],
            dictionary_id=json['id'],
        )

        if 'fields' not in json['attributes']:
            # DLIv2 doesn't put the fields on the attributes 
            # when getting
            self.__dict__['fields'] = [
                Field(f) for f in self._get_fields()
            ]
