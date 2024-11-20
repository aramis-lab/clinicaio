

from collections import UserString
from typing import Union, Optional
from pathlib import Path 
from .enum import SUVRReferenceRegions, Tracer, 
from enum import Enum
# questions: dependance à Pydantic ??


class Label(UserString):
    def __init__(self, value: str):
        super().__init__(self.validate(value))

    @classmethod
    def validate(cls, value: Union[str, Enum]) -> str:
        if isinstance(value, Enum):
            return value.value
        elif isinstance(value, str) and value.isalnum():
            return value
        raise ValueError(
            f"Label '{value}' is not a valid BIDS label: it must be string composed only by letters and/or numbers."
        )
    
class Index(UserString):
    
    def __init__(self, value: int, length_as_string: int = 1):
        super().__init__(self.validate(value, length_as_string))

    @classmethod
    def validate(cls, value: int, length_as_string: int) -> str:
        if not isinstance(value, int):
            try:
                value = int(value)
            except TypeError as exc:
                raise ValueError(
                    f"Index '{value}' is not a valid BIDS index: it must be a non-negative integer."
                ) from exc

        return str(value).zfill(length_as_string)
        


class Entity:
    key: Label
    value : Union[Label, Index]

    def __str__(self) -> str:
        return f"{self.key}-{self.value}"


# BIDS Entities

class SubjectEntity(Entity):
    """
    A person or animal participating in the study.
    """
    key = Label("sub")

    def __init__(self, value: str):
        self.value = Label(value)


class SessionEntity(Entity):
    """
    A logical grouping of neuroimaging and behavioral data consistent across subjects. 
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
        self.value = Label(value)


class AcquisitionEntity(Entity):
    """
    The acq-<label> entity corresponds to a custom label the user MAY use to distinguish a different 
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

    def __init__(self, value: str):
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
    """
    Resolution of regularly sampled N-dimensional data.

    This entity represents the "Resolution" metadata field. Therefore, if the res-<label> 
    entity is present in a filename, "Resolution" MUST also be added in the JSON file, 
    to provide interpretation.

    This entity is only applicable to derivative data.

    """
    key = Label("res")

    def __init__(self, value: str):
        self.value = Label(value) 


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

    def __init__(self, value: int):
        self.value = Index(value) 


class AnatMRISuffix(str, Enum):
    FLAIR = "FLAIR"
    T1W = "T1w"
    T2W = "T2w"
    

class PETSuffix(str, Enum):
    PET = "pet"

class DWISuffix(str, Enum):
    DWI = "dwi"

class FMapSuffix(str, Enum):
    

# CAPS Entities

class SUVREntity(Entity):
    key = Label("suvr")
    def __init__(self, value: str):
        self.value = Label(SUVRReferenceRegions(value))


#
class Modality(str, Enum):
    T1 = "T1W"

class Extension(str, Enum):
    NIFTI = ".nii"
    NIFTI_GZ = ".nii.gz"
    DICOM = ".dcm"
    PT = ".pt"

 
class BIDSPath(Base):
    subject: SubjectEntity
    session: SessionEntity
    modality: Modality
    entities: Optional[list[Entity]]
    extension: Optional[Extension]

    
    def __init__(self, subject, session, modality, entities, extension):
        self.subject = subject
        self.session = session
        self.modality = modality
        self.entities = entities
        self.extension = extension
        
        

    def get_image(self):
        path_ = Path(str(self.subject)) / str(self.session) / str(self.modality)

        filename = path_

        for entity in self.entities:
            filename += "_" + str(entity)
        
        filename += f".{(str(self.extension) if self.extension else '')}"