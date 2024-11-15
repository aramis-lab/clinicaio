import shutil
from pathlib import Path

from clinicaio.utils.caps_generator.flair_linear import build_flair_linear


def test_build_flair_linear():
    test_dir = Path(__file__).parents[3] / "tmp"
    pipeline_dir = test_dir / "subjects" / "sub-002" / "ses-M003" / "flair_linear"

    if test_dir.exists():
        shutil.rmtree(test_dir)

    build_flair_linear(root=test_dir, subject=2, session=3)
    assert (
        pipeline_dir
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_FLAIR.nii.gz"
    ).exists()
    assert (
        pipeline_dir / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        pipeline_dir
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_FLAIR.nii.gz"
    ).exists()

    shutil.rmtree(test_dir)

    build_flair_linear(root=test_dir, subject=2, session=3, crop=False)
    assert not (
        pipeline_dir
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_FLAIR.nii.gz"
    ).exists()
    assert (
        pipeline_dir / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        pipeline_dir
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_FLAIR.nii.gz"
    ).exists()

    shutil.rmtree(test_dir)
