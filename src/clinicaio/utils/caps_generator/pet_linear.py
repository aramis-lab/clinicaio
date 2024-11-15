from pathlib import Path
from typing import Union

import nibabel as nib
import numpy as np
from scipy.io import savemat

from clinicaio.utils.bids_entities import SessionEntity, SubjectEntity
from clinicaio.utils.caps import Extension, Resolution, Space, Suffix
from clinicaio.utils.pet import SUVRReferenceRegion, Tracer

from .filename import get_caps_filename


def build_pet_linear(
    root: Union[str, Path],
    subject: int,
    session: int,
    tracer: str = Tracer.FDG,
    suvr_ref_region: str = SUVRReferenceRegion.PONS,
    crop: bool = True,
    save_pet_in_t1w_space: bool = False,
):
    """
    Simulates pet-linear by creating fake output files in `root`.
    """
    dummy_nifti_img = nib.Nifti1Image(np.ones((1, 1, 1)).astype(np.int8), np.eye(4))
    dummy_mat = {
        "AffineTransform_double_3_3": np.ones((1, 1)).astype(np.int8),
        "fixed": np.ones((1, 1)).astype(np.int8),
    }

    resolution = Resolution.ONE
    trc = Tracer(tracer)
    suvr = SUVRReferenceRegion(suvr_ref_region)
    directory = (
        Path(root)
        / "subjects"
        / SubjectEntity(subject)
        / SessionEntity(session)
        / "pet_linear"
    )
    directory.mkdir(parents=True, exist_ok=True)

    uncropped_file = directory / get_caps_filename(
        subject,
        session,
        tracer=trc,
        space=Space.MNI,
        crop=False,
        resolution=resolution,
        suvr_ref_region=suvr,
        suffix=Suffix.PET,
        extension=Extension.NIIGZ,
    )
    nib.save(dummy_nifti_img, uncropped_file)

    mat_file = directory / get_caps_filename(
        subject,
        session,
        tracer=trc,
        space=Space.T1W,
        suffix=Suffix.RIGID,
        extension=Extension.MAT,
    )
    savemat(mat_file, dummy_mat)

    if crop:
        cropped_file = directory / get_caps_filename(
            subject,
            session,
            tracer=trc,
            space=Space.MNI,
            crop=True,
            resolution=resolution,
            suvr_ref_region=suvr,
            suffix=Suffix.PET,
            extension=Extension.NIIGZ,
        )
        nib.save(dummy_nifti_img, cropped_file)

    if save_pet_in_t1w_space:
        nifti_file = directory / get_caps_filename(
            subject,
            session,
            tracer=trc,
            space=Space.T1W,
            suffix=Suffix.PET,
            extension=Extension.NIIGZ,
        )
        nib.save(dummy_nifti_img, nifti_file)
