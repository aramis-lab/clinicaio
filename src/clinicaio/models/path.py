from enum import Enum
from pathlib import Path
from typing import Optional, Union

from clinicaio.models.bids.entity import Entity, SessionEntity, SubjectEntity, Suffix

__all__ = [
    "Extension",
    "BIDSPath",
    "AnatMRISuffix",
]


class Extension(str, Enum):
    NIFTI = ".nii"
    NIFTI_GZ = ".nii.gz"
    DICOM = ".dcm"
    PT = ".pt"


class AnatMRISuffix(str, Enum):
    FLAIR = "FLAIR"
    T1W = "T1w"
    T2W = "T2w"


class BIDSPath:
    def __init__(
        self,
        subject: Union[str, SubjectEntity],
        session: Union[str, SessionEntity],
        modality: str,
        suffix: Union[str, Suffix],
        extension: Union[str, Extension],
        entities: Optional[list[Entity]] = None,
    ):
        self.subject = SubjectEntity(subject)
        self.session = SessionEntity(session)
        self.modality = modality  # Modality
        self.suffix = Suffix(suffix)
        self.extension = Extension(extension)
        self.entities = entities or []

    @property
    def filename(self) -> str:
        filename = str(self.subject) + "_" + str(self.session)
        for entity in self.entities:
            filename += "_" + str(entity)
        filename += f"_{self.suffix}{self.extension.value}"
        return filename

    @property
    def path(self) -> Path:
        return (
            Path(str(self.subject))
            / str(self.session)
            / str(self.modality)
            / self.filename
        )
