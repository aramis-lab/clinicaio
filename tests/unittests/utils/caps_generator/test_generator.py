import shutil
from pathlib import Path

from clinicaio.utils.caps_generator.generator import CAPSGenerator


def test_caps_generator():
    test_dir = Path(__file__).parents[3] / "tmp"
    generator = CAPSGenerator(test_dir)

    generator.build_pipeline("t1-linear", subjects=[1, 2], sessions=[3, 4], crop=False)
    generator.build_pipeline("flair-linear", subjects=[2], sessions=[4], crop=False)
    generator.build_pipeline(
        "pet-linear",
        subjects=[1, 2],
        sessions=[3],
        crop=False,
        save_pet_in_t1w_space=False,
        tracer="18FFMM",
        suvr_ref_region="pons2",
    )
    generator.remove_pipeline("pet-linear", subject=2, session=3)
    generator.remove_pipeline("flair-linear", subject=1, session=4)  # does not exist

    # t1-linear
    assert not (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M003"
        / "t1_linear"
        / "sub-001_ses-M003_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_T1w.nii.gz"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M003"
        / "t1_linear"
        / "sub-001_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M003"
        / "t1_linear"
        / "sub-001_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_T1w.nii.gz"
    ).exists()

    assert not (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M004"
        / "t1_linear"
        / "sub-001_ses-M004_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_T1w.nii.gz"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M004"
        / "t1_linear"
        / "sub-001_ses-M004_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M004"
        / "t1_linear"
        / "sub-001_ses-M004_space-MNI152NLin2009cSym_res-1x1x1_T1w.nii.gz"
    ).exists()

    assert not (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M003"
        / "t1_linear"
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_T1w.nii.gz"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M003"
        / "t1_linear"
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M003"
        / "t1_linear"
        / "sub-002_ses-M003_space-MNI152NLin2009cSym_res-1x1x1_T1w.nii.gz"
    ).exists()

    assert not (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M004"
        / "t1_linear"
        / "sub-002_ses-M004_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_T1w.nii.gz"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M004"
        / "t1_linear"
        / "sub-002_ses-M004_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M004"
        / "t1_linear"
        / "sub-002_ses-M004_space-MNI152NLin2009cSym_res-1x1x1_T1w.nii.gz"
    ).exists()

    # flair-linear
    assert not (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M004"
        / "t1_linear"
        / "sub-002_ses-M004_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_FLAIR.nii.gz"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M004"
        / "flair_linear"
        / "sub-002_ses-M004_space-MNI152NLin2009cSym_res-1x1x1_affine.mat"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-002"
        / "ses-M004"
        / "flair_linear"
        / "sub-002_ses-M004_space-MNI152NLin2009cSym_res-1x1x1_FLAIR.nii.gz"
    ).exists()

    # pet-linear
    assert (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M003"
        / "pet_linear"
        / "sub-001_ses-M003_trc-18FFMM_space-T1w_rigid.mat"
    ).exists()
    assert not (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M003"
        / "pet_linear"
        / "sub-001_ses-M003_trc-18FFMM_space-T1w_pet.nii.gz"
    ).exists()
    assert (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M003"
        / "pet_linear"
        / "sub-001_ses-M003_trc-18FFMM_space-MNI152NLin2009cSym_res-1x1x1_suvr-pons2_pet.nii.gz"
    ).exists()
    assert not (
        test_dir
        / "subjects"
        / "sub-001"
        / "ses-M003"
        / "pet_linear"
        / "sub-001_ses-M003_trc-18FFMM_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_suvr-pons2_pet.nii.gz"
    ).exists()

    assert not (test_dir / "subjects" / "sub-002" / "ses-M003" / "pet_linear").exists()

    shutil.rmtree(test_dir)
