from typing import Optional
from pathlib import Path
from .bids_entities import (
    SubjectEntity,
    SessionEntity,
    TracerEntity,
    SpaceEntity,
    DescriptionEntity,
    ResolutionEntity,
    SUVREntity,
)
from .bids import Suffix, Extension
from .caps import Description


def get_caps_filename(
    subject: int,
    session: int,
    suffix: str,
    extension: str,
    tracer: Optional[str] = None,
    space: Optional[str] = None,
    crop: bool = False,
    resolution: Optional[str] = None,
    suvr_ref_region: Optional[str] = None,
) -> Path:
    entities_list = []
    for entity in [  # order matters
        SubjectEntity(subject),
        SessionEntity(session),
        TracerEntity(tracer) if tracer else None,
        SpaceEntity(space) if space else None,
        DescriptionEntity(Description.CROP) if crop else None,
        ResolutionEntity(resolution) if resolution else None,
        SUVREntity(suvr_ref_region) if suvr_ref_region else None,
        Suffix(suffix).value,
    ]:
        if entity is not None:
            entities_list.append(entity)

    return Path("_".join(entities_list)).with_suffix(Extension(extension).value)
