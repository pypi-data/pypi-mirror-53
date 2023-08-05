from dli.models import DictionaryModel
from unittest.mock import MagicMock


def test_dictionary_with_fields():
    client = MagicMock()
    model = DictionaryModel(
            {'attributes':{'fields': []}, 'id': '123'}, client
    )

    assert not client.session.get.called


def test_dictionary_fields():
    client = MagicMock()
    model = DictionaryModel(
        {'attributes':{}, 'id': '123'}, client
    )

    assert client.session.get.called


def test_dictionary_field_pagination():
    client = MagicMock()

    def _response():
        i = 0
        while True:
            yield {
                'meta': {'total_count': 3},
                'data': {
                    'attributes': {
                        'fields': [{
                            'test': i
                        }]
                    }
                }
            }
            i += 1

    client.session.get().json.side_effect = _response()

    model = DictionaryModel(
        {'attributes':{}, 'id': '123'}, client
    )

    assert len(model.fields) == 3
