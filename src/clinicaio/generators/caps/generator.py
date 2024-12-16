import shutil
from pathlib import Path
from typing import List, Union

from clinicaio.models.bids_entities import SessionEntity, SubjectEntity
from clinicaio.models.caps import Pipeline

from .flair_linear import _build_flair_linear
from .pet_linear import _build_pet_linear
from .t1_linear import _build_t1_linear


class CAPSGenerator:
    """
    To build fake CAPS. A CAPSGenerator simulates preprocessing pipelines
    by creating fake output files.

    Parameters
    ----------
    directory : Union[str, Path]
        the directory of the CAPS.
    """

    def __init__(self, directory: Union[str, Path]) -> None:
        self.dir = Path(directory)

    def build_pipeline(
        self,
        pipeline: Union[str, Pipeline],
        subjects: List[int],
        sessions: List[int],
        **kwargs,
    ) -> None:
        """
        Simulates a preprocessing pipeline for every subject in `subjects` and every session
        in `sessions`.

        Parameters
        ----------
        pipeline : Union[str, Pipeline]
            the pipeline to simulate. Supported pipelines are `t1-linear`,
            `flair-linear` and `pet-linear`.
        subjects : List[int]
            the list of subject IDs
        sessions : List[int]
            the list of session IDs.
        **kwargs
            any argument accepted by the pipeline:
            - `t1_linear`: `crop`;
            - `flair_linear`: `crop`;
            - `pet-linear`: `tracer`, `suvr_ref_region`, `crop` and `save_pet_in_t1w_space`.

        Raises
        ------
        ValueError
            if  `pipeline` is not in `t1-linear`, `flair-linear` and `pet-linear`.
        """
        pipeline = Pipeline(pipeline)
        if pipeline == Pipeline.T1_LINEAR:
            builder = _build_t1_linear
        elif pipeline == Pipeline.FLAIR_LINEAR:
            builder = _build_flair_linear
        elif pipeline == Pipeline.PET_LINEAR:
            builder = _build_pet_linear
        else:
            raise ValueError(f"pipeline {pipeline} is not yet implemented.")

        for subject in subjects:
            for session in sessions:
                builder(self.dir, subject, session, **kwargs)

    def remove_pipeline(
        self, pipeline: Union[str, Pipeline], subject: int, session: int
    ) -> None:
        """
        Removes a preprocessing pipeline for a specific (subject, session).

        Parameters
        ----------
        pipeline : Union[str, Pipeline]
            the pipeline to remove. Supported pipelines are `t1-linear`,
            `flair-linear` and `pet-linear`.
        subject : int
            the subject ID.
        session : int
            the session ID.

        Raises
        ------
        ValueError
            if  `pipeline` is not in `t1-linear`, `flair-linear` and `pet-linear`.
        """
        pipeline = Pipeline(pipeline)
        if pipeline == Pipeline.T1_LINEAR:
            directory = "t1_linear"
        elif pipeline == Pipeline.FLAIR_LINEAR:
            directory = "flair_linear"
        elif pipeline == Pipeline.PET_LINEAR:
            directory = "pet_linear"
        else:
            raise ValueError(f"pipeline {pipeline} is not yet implemented.")

        full_dir = (
            self.dir
            / "subjects"
            / SubjectEntity(subject)
            / SessionEntity(session)
            / directory
        )
        try:
            shutil.rmtree(full_dir)
        except FileNotFoundError:  # there is not such subject/session for this pipeline
            pass
