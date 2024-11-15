import shutil
from pathlib import Path
from clinicaio.utils.caps_generator.t1_linear import build_t1_linear


def test_build_t1_linear():
    test_dir = Path(__file__).parents[2] / "tmp"
    pipeline_dir = test_dir / "subjects" / "sub-002" / "ses-M003" / "t1_linear"

    if pipeline_dir.exists():
        shutil.rmtree(pipeline_dir)

    build_t1_linear(root=test_dir, subject=2, session=3, crop=True)
    assert (
        pipeline_dir
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_T1w.nii.gz"
    ).exists()
    assert (
        pipeline_dir / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        pipeline_dir / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_T1w.nii.gz"
    ).exists()

    shutil.rmtree(pipeline_dir)

    build_t1_linear(root=test_dir, subject=2, session=3, crop=False)
    assert not (
        pipeline_dir
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_T1w.nii.gz"
    ).exists()
    assert (
        pipeline_dir / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        pipeline_dir / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_T1w.nii.gz"
    ).exists()

    shutil.rmtree(pipeline_dir)
