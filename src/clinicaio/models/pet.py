from enum import Enum

__all__ = [
    "Tracer",
    "SUVRReferenceRegions",
]


class Tracer(str, Enum):
    """BIDS label for PET tracers.

    Follows the convention proposed in the PET section of the BIDS specification.

    See: https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/09-positron-emission-tomography.html
    """

    PIB = "11CPIB"
    AV1451 = "18FAV1451"
    AV45 = "18FAV45"
    FBB = "18FFBB"
    FDG = "18FFDG"
    FMM = "18FFMM"


class SUVRReferenceRegions(str, Enum):
    """Possible SUVR reference region for pet images in clinicaIO."""

    PONS = "pons"
    CEREBELLUMPONS = "cerebellumPons"
    PONS2 = "pons2"
    CEREBELLUMPONS2 = "cerebellumPons2"
