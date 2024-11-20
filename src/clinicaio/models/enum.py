

from enum import Enum

class SUVRReferenceRegions(str, Enum):
    """Possible SUVR reference region for pet images in clinicaDL."""

    PONS = "pons"
    CEREBELLUMPONS = "cerebellumPons"
    PONS2 = "pons2"
    CEREBELLUMPONS2 = "cerebellumPons2"


class Tracer(str, Enum):
    """Possible tracer for pet images in clinicaDL."""

    FFDG = "18FFDG"
    FAV45 = "18FAV45"
    CPIB = "11CPIB"

class AnatMRISuffix(str, Enum):
    FLAIR = "FLAIR"
    T1W = "T1w"
    T2W = "T2w"
    

class PETSuffix(str, Enum):
    PET = "pet"

class DWISuffix(str, Enum):
    DWI = "dwi"

class FMapSuffix(str, Enum):
    pass

class Modality(str, Enum):
    pass


class Extension(str, Enum):
    NIFTI = ".nii"
    NIFTI_GZ = ".nii.gz"
    DICOM = ".dcm"
    PT = ".pt"
