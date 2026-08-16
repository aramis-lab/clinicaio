import re
from typing import Optional, Union

from clinicaio.models.pet import SUVRReferenceRegions, Tracer

from ._base import Index, Label

__all__ = [
    "Entity",
    "SubjectEntity",
    "SessionEntity",
    "AcquisitionEntity",
    "SpaceEntity",
    "TracerEntity",
    "DescriptionEntity",
    "ResolutionEntity",
    "RunEntity",
    "SUVREntity",
    "parse_entity",
]


class Entity:
    """Base class for entities as defined in the BIDS specifications."""

    key: Label
    value: Union[Label, Index]

    def __str__(self) -> str:
        return f"{self.key}-{self.value}"


class SubjectEntity(Entity):
    """A person or animal participating in the study."""

    key = Label("sub")

    def __init__(self, value: str):
        if value.startswith(str(self.key)):
            value = value.removeprefix(f"{self.key}-")
        self.value = Label(value)


class SessionEntity(Entity):
    """A logical grouping of neuro-imaging and behavioral data consistent across subjects.

    Session can (but doesn't have to) be synonymous to a visit in a longitudinal study.
    In general, subjects will stay in the scanner during one session.
    However, for example, if a subject has to leave the scanner room and then be re-positioned
    on the scanner bed, the set of MRI acquisitions will still be considered as a session
    and match sessions acquired in other subjects. Similarly, in situations where different
    data types are obtained over several visits (for example fMRI on one day followed by DWI
    the day after) those can be grouped in one session.

    Defining multiple sessions is appropriate when several identical or similar data
    acquisitions are planned and performed on all -or most- subjects, often in the
    case of some intervention between sessions (for example, training).
    """

    key = Label("ses")

    def __init__(self, value: str):
        if value.startswith(str(self.key)):
            value = value.removeprefix(f"{self.key}-")
        self.value = Label(value)


class AcquisitionEntity(Entity):
    """The acq-<label> entity corresponds to a custom label the user MAY use to distinguish a different
    set of parameters used for acquiring the same modality.

    For example, this should be used when a study includes two T1w images - one full brain low
    resolution and one restricted field of view but high resolution. In such case two files
    could have the following names: sub-01_acq-highres_T1w.nii.gz and sub-01_acq-lowres_T1w.nii.gz;
    however, the user is free to choose any other label than highres and lowres as long as they are
    consistent across subjects and sessions.

    In case different sequences are used to record the same modality (for example, RARE and FLASH for T1w)
    this field can also be used to make that distinction. The level of detail at which the distinction
    is made (for example, just between RARE and FLASH, or between RARE, FLASH, and FLASHsubsampled) remains
    at the discretion of the researcher.
    """

    key = Label("acq")

    def __init__(self, value: str):
        self.value = Label(value)


class SpaceEntity(Entity):
    """
    The space-<label> entity can be used to indicate the way in which electrode positions are interpreted
    (for EEG/MEG/iEEG data) or the spatial reference to which a file has been aligned (for MRI data).
    The <label> MUST be taken from one of the modality specific lists in the Coordinate Systems Appendix.
    For example, for iEEG data, the restricted keywords listed under iEEG Specific Coordinate Systems are
    acceptable for <label>.

    For EEG/MEG/iEEG data, this entity can be applied to raw data, but for other data types, it is restricted to derivative data.
    """

    key = Label("space")

    def __init__(self, value: str):
        self.value = Label(value)


class TracerEntity(Entity):
    """
    This entity represents the "TracerName" metadata field.
    Therefore, if the trc-<label> entity is present in a filename,
    "TracerName" MUST be defined in the associated metadata.
    Please note that the <label> does not need to match the actual value of the field.
    """

    key = Label("trc")

    def __init__(self, value: Union[str, Tracer]):
        self.value = Label(Tracer(value))


class DescriptionEntity(Entity):
    """
    When necessary to distinguish two files that do not otherwise have a distinguishing entity,
    the desc-<label> entity SHOULD be used.

    This entity is only applicable to derivative data.
    """

    key = Label("desc")

    def __init__(self, value: str):
        self.value = Label(value)


class ResolutionEntity(Entity):
    """Resolution of regularly sampled N-dimensional data.

    This entity represents the "Resolution" metadata field. Therefore, if the res-<label>
    entity is present in a filename, "Resolution" MUST also be added in the JSON file,
    to provide interpretation.

    This entity is only applicable to derivative data.

    """

    key = Label("res")

    def __init__(self, value: Union[int, str, tuple[int, int, int]]):
        if isinstance(value, int):
            value = f"{value}x{value}x{value}"
        elif isinstance(value, tuple):
            value = f"{value[0]}x{value[1]}x{value[2]}"
        if re.fullmatch(r"\dx\dx\d", value):
            self.value = Label(value)
        else:
            raise ValueError(
                f"Resolution as a string should look like '1x1x1', {value} received."
            )


class RunEntity(Entity):
    """
    The run-<index> entity is used to distinguish separate data acquisitions with the same
    acquisition parameters and (other) entities.

    If several data acquisitions (for example, MRI scans or EEG recordings) with the same acquisition
    parameters are acquired in the same session, they MUST be indexed with the run-<index> entity:
    _run-1, _run-2, _run-3, and so on (only nonnegative integers are allowed as run indices).

    If different entities apply, such as a different session indicated by ses-<label>,
    or different acquisition parameters indicated by acq-<label>, then run is not needed to distinguish
    the scans and MAY be omitted.
    """

    key = Label("run")

    def __init__(self, value: int, length_as_string: Optional[int] = None):
        self.value = Index(value, length_as_string=length_as_string)


class SUVREntity(Entity):
    key = Label("suvr")

    def __init__(self, value: Union[str, SUVRReferenceRegions]):
        self.value = Label(SUVRReferenceRegions(value))


key_to_entity = {
    "sub": SubjectEntity,
    "ses": SessionEntity,
    "acq": AcquisitionEntity,
    "space": SpaceEntity,
    "trc": TracerEntity,
    "desc": DescriptionEntity,
    "res": ResolutionEntity,
    "run": RunEntity,
    "suvr": SUVREntity,
}


def parse_entity(entity: str) -> Entity:
    key, value = entity.split("-")
    return key_to_entity[key](value)
