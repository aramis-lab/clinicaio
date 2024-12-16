from pathlib import Path

import pytest

from clinicaio.generators.caps.filename import _get_caps_filename


@pytest.mark.parametrize(
    "args,expected_output",
    [
        (
            {"subject": 1, "session": 0, "suffix": "T1w", "extension": ".nii.gz"},
            "sub-001_ses-M000_T1w.nii.gz",
        ),
        (
            {
                "subject": 1,
                "session": 0,
                "suffix": "affine",
                "crop": True,
                "space": "MNI152NLin2009cSym",
                "resolution": "1x1x1",
                "extension": ".mat",
            },
            "sub-001_ses-M000_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_affine.mat",
        ),
        (
            {
                "subject": 111,
                "session": 222,
                "suffix": "pet",
                "tracer": "18FFDG",
                "suvr_ref_region": "pons",
                "extension": ".nii.gz",
            },
            "sub-111_ses-M222_trc-18FFDG_suvr-pons_pet.nii.gz",
        ),
    ],
)
def test_get_caps_filename(args, expected_output):
    filename = _get_caps_filename(**args)
    assert isinstance(filename, Path)
    assert str(filename) == expected_output
