from enum import Enum


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
    """Possible suffixes in BIDS file names."""

    DWI = "dwi"
    PET = "pet"
    T1W = "t1w"
    T2W = "t2w"
    FLAIR = "flair"
    AFFINE = "affine"
    PROBABILITY = "probability"
    DEFORMATION = "deformation"
    PHASEDIFF = "phasediff"
    MAGNITUDE1 = "magnitude1"
    BRAINMASK = "brainmask"
    STATISTICS = "statistics"
    DIFFMODEL = "diffmodel"
    PARCELLATION = "parcellation"
