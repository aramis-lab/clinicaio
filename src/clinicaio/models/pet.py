from enum import Enum


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


class SUVRReferenceRegion(str, Enum):
    """Possible SUVR Reference Regions for PET pipelines."""

    PONS = "pons"
    CEREBELLUM_PONS = "cerebellumPons"
    PONS2 = "pons2"
    CEREBELLUM_PONS2 = "cerebellumPons2"
