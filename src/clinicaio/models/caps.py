from enum import Enum


class Pipeline(str, Enum):
    """Preprocessing pipelines that can be found in CAPS."""

    T1_LINEAR = "t1-linear"
    FLAIR_LINEAR = "flair-linear"
    PET_LINEAR = "pet-linear"


class Extension(str, Enum):
    """Possible extensions in BIDS file names."""

    NIIGZ = ".nii.gz"
    NII = ".nii"
    JSON = ".json"
    TSV = ".tsv"
    MAT = ".mat"
    BVAL = ".bval"
    BVEC = ".bvec"


class Suffix(str, Enum):
    """Possible suffixes in CAPS file names."""

    DWI = "dwi"
    PET = "pet"
    T1W = "T1w"
    FLAIR = "FLAIR"
    AFFINE = "affine"
    RIGID = "rigid"


class Space(str, Enum):
    """Possible registration spaces."""

    MNI = "MNI152NLin2009cSym"
    IXI = "Ixi549Space"
    T1W = "T1w"


class Resolution(str, Enum):
    """Resolutions that can be found in CAPS."""

    ONE = "1x1x1"


class Description(str, Enum):
    """BIDS Description values that can be found in CAPS."""

    CROP = "Crop"
