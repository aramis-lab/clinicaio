from pathlib import Path
from typing import Union

import nibabel as nib
import numpy as np
from scipy.io import savemat

from clinicaio.models.bids_entities import SessionEntity, SubjectEntity
from clinicaio.models.caps import Extension, Resolution, Space, Suffix

from .filename import _get_caps_filename


def _build_t1_linear(
    root: Union[str, Path], subject: int, session: int, crop: bool = True
):
    """
    Simulates t1-linear by creating fake output files in `root`.
    """
    dummy_nifti_img = nib.Nifti1Image(np.ones((1, 1, 1)).astype(np.int8), np.eye(4))
    dummy_mat = {
        "AffineTransform_double_3_3": np.ones((1, 1)).astype(np.int8),
        "fixed": np.ones((1, 1)).astype(np.int8),
    }

    space = Space.MNI
    resolution = Resolution.ONE
    directory = (
        Path(root)
        / "subjects"
        / SubjectEntity(subject)
        / SessionEntity(session)
        / "t1_linear"
    )
    directory.mkdir(parents=True, exist_ok=True)

    uncropped_file = directory / _get_caps_filename(
        subject,
        session,
        space=space,
        resolution=resolution,
        suffix=Suffix.T1W,
        extension=Extension.NIIGZ,
    )
    nib.save(dummy_nifti_img, uncropped_file)

    mat_file = directory / _get_caps_filename(
        subject,
        session,
        space=space,
        resolution=resolution,
        suffix=Suffix.AFFINE,
        extension=Extension.MAT,
    )
    savemat(mat_file, dummy_mat)

    if crop:
        cropped_file = directory / _get_caps_filename(
            subject,
            session,
            space=space,
            crop=True,
            resolution=resolution,
            suffix=Suffix.T1W,
            extension=Extension.NIIGZ,
        )
        nib.save(dummy_nifti_img, cropped_file)
