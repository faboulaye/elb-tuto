import pytest
from unit.models.sample_model import SampleModel


@pytest.fixture
def sample_data():
    return SampleModel(id="foobar", value="foobar", ts_created=111, ts_changed=111)


def test_ts_created_and_changed(sample_data):
    res = sample_data.ts_created_and_changed()
    assert res == {"ts_created": 111, "ts_changed": 111}


def test_key(sample_data):
    res = sample_data.key()
    assert res == {"pk": "SAMPLE_MODEL#foobar", "sk": "SAMPLE_MODEL#foobar"}


def test_to_item(sample_data):
    res = sample_data.to_item()
    assert res == {
        "pk": "SAMPLE_MODEL#foobar",
        "sk": "SAMPLE_MODEL#foobar",
        "id": "foobar",
        "value": "foobar",
        "ts_created": 111,
        "ts_changed": 111,
    }
