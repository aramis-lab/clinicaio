import shutil
from pathlib import Path
from clinicaio.utils.caps_generator.pet_linear import build_pet_linear


def test_build_pet_linear():
    test_dir = Path(__file__).parents[2] / "tmp"
    pipeline_dir = test_dir / "subjects" / "sub-002" / "ses-M003" / "pet_linear"

    if pipeline_dir.exists():
        shutil.rmtree(pipeline_dir)

    build_pet_linear(
        root=test_dir,
        subject=2,
        session=3,
        tracer="18FFDG",
        suvr_ref_region="pons",
        save_pet_in_t1w_space=True,
    )
    assert (pipeline_dir / "sub-002_ses-M003_trc-18FFDG_space-T1w_rigid.mat").exists()
    assert (pipeline_dir / "sub-002_ses-M003_trc-18FFDG_space-T1w_pet.nii.gz").exists()
    assert (
        pipeline_dir
        / "sub-002_ses-M003_trc-18FFDG_space-MNI152NLin2009cSym_res-1x1x1_suvr-pons_pet.nii.gz"
    ).exists()
    assert (
        pipeline_dir
        / "sub-002_ses-M003_trc-18FFDG_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_suvr-pons_pet.nii.gz"
    ).exists()

    shutil.rmtree(pipeline_dir)

    build_pet_linear(
        root=test_dir,
        subject=2,
        session=3,
        tracer="18FFDG",
        suvr_ref_region="pons",
        crop=False,
        save_pet_in_t1w_space=False,
    )
    assert (pipeline_dir / "sub-002_ses-M003_trc-18FFDG_space-T1w_rigid.mat").exists()
    assert not (
        pipeline_dir / "sub-002_ses-M003_trc-18FFDG_space-T1w_pet.nii.gz"
    ).exists()
    assert (
        pipeline_dir
        / "sub-002_ses-M003_trc-18FFDG_space-MNI152NLin2009cSym_res-1x1x1_suvr-pons_pet.nii.gz"
    ).exists()
    assert not (
        pipeline_dir
        / "sub-002_ses-M003_trc-18FFDG_space-MNI152NLin2009cSym_desc-Crop_res-1x1x1_suvr-pons_pet.nii.gz"
    ).exists()

    shutil.rmtree(pipeline_dir)
