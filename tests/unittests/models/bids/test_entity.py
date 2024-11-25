import re

import pytest


@pytest.mark.parametrize("value", ["foo", "f", "1", "0"])
def test_label(value: str):
    from clinicaio.models.bids import Label

    label = Label(value)

    assert label == value


def test_label_with_enum():
    from clinicaio.models.bids import Label
    from clinicaio.models.pet import Tracer

    label = Label(Tracer.FDG)

    assert label == "18FFDG"


@pytest.mark.parametrize("value", ["foo-bar", "_f", "1$", "+0", ""])
def test_label_error(value: str):
    from clinicaio.models.bids import Label

    with pytest.raises(
        ValueError,
        match=re.escape(
            f"Label '{value}' is not a valid BIDS label: it must be string composed only by letters and/or numbers."
        ),
    ):
        Label(value)


def test_index():
    from clinicaio.models.bids import Index

    assert Index(1) == "1"
    assert Index(1, 2) == "01"
    assert Index(1, 3) == "001"
    assert Index(10) == "10"
    assert Index(0, 4) == "0000"


def test_index_bad_length_compared_to_value_error():
    from clinicaio.models.bids import Index

    with pytest.raises(
        ValueError,
        match="Cannot set index with value 10 with a length of 1.",
    ):
        Index(10, 1)


def test_index_bad_length_error():
    from clinicaio.models.bids import Index

    with pytest.raises(
        ValueError,
        match="The length of an Index should be at least 1, 0 was provided.",
    ):
        Index(10, 0)


def test_index_negative_error():
    from clinicaio.models.bids import Index

    with pytest.raises(
        ValueError,
        match="Index '-1' is not a valid BIDS index: it must be a non-negative integer.",
    ):
        Index(-1)


def test_resolution_entity():
    from clinicaio.models.bids.entity import ResolutionEntity

    assert str(ResolutionEntity(2)) == "res-2x2x2"
    assert str(ResolutionEntity((2, 1, 3))) == "res-2x1x3"
    assert str(ResolutionEntity("1x4x2")) == "res-1x4x2"


def test_resolution_entity_error():
    from clinicaio.models.bids.entity import ResolutionEntity

    with pytest.raises(
        ValueError,
        match="Resolution as a string should look like '1x1x1', foo received.",
    ):
        ResolutionEntity("foo")
