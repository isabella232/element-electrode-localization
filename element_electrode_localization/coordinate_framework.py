import logging
import pathlib
import re

import datajoint as dj
import nrrd
import numpy as np
import pandas as pd
from tqdm import tqdm

log = logging.getLogger(__name__)
schema = dj.schema()


def activate(schema_name, *, create_schema=True, create_tables=True):
    """Activates the schema.

    Args:
        schema_name (str): A string containing the name of the probe schema.
        create_schema (bool): If True, schema will be created in the database.
        create_tables (bool): If True, tables related to the schema will be created in the database.
    """
    schema.activate(
        schema_name, create_schema=create_schema, create_tables=create_tables
    )

    # ----------------------------- Table declarations ----------------------


@schema
class CCF(dj.Lookup):
    """Common coordinate framework information.

    Attributes:
        ccf_id (foreign key, int): CCF ID/atlas ID.
        ccf_version (varchar(64) ): Allen CCF version.
        ccf_resolution (float): Voxel resolution in microns.
        ccf_description (varchar(255) ): CCF label descriptions.
    """

    definition = """  # Common Coordinate Framework
    ccf_id            : int             # CCF ID, a.k.a atlas ID
    ---
    ccf_version       : varchar(64)     # Allen CCF Version - e.g. CCFv3
    ccf_resolution    : float           # voxel resolution in micron
    ccf_description='': varchar(255)    # CCFLabel Description
    """

    class Voxel(dj.Part):
        """CCF voxel coordinates.

        Attributes:
            CCF (foreign key): CCF primary key.
            x (foreign key, int): Anterior-to-posterior axis (AP axis) in micrometers.
            y (foreign key, int): Superior-to_inferior axis (DV axis) in micrometers.
            z (foreign key, int): Left-to-right (ML axis) in micrometers.
        """

        definition = """  # CCF voxel coordinates
        -> master
        x   :  int   # (um)  Anterior-to-Posterior (AP axis)
        y   :  int   # (um)  Superior-to-Inferior (DV axis)
        z   :  int   # (um)  Left-to-Right (ML axis)
        index(y, z)
        """


@schema
class BrainRegionAnnotation(dj.Lookup):
    """Brain region annotation.

    Attributes:
        CCF (foreign key): CCF primary key.
    """

    definition = """
    -> CCF
    """

    class BrainRegion(dj.Part):
        """Brain region information.

        Attributes:
            BrainRegionAnnotation (foreign key): BrainRegionAnnotation primary key.
            acronym (foreign key, varchar(32) ): Brain region acronym.
            region_name (varchar(128) ): Brain region full name.
            region_id (int): Brain region ID.
            color_code (varchar(6) ): Hex code of the color code for this region.
        """

        definition = """
        -> master
        acronym: varchar(32)  # CHARACTER SET utf8 COLLATE utf8_bin
        ---
        region_name: varchar(128)
        region_id=null: int
        color_code=null: varchar(6)  # Hex code of the color code of this region
        """

    class Voxel(dj.Part):
        """Voxel information from CCF.

        Attributes:
            BrainRegion (foreign key): BrainRegionAnnotation.BrainRegion primary key.
            CCF.Voxel (foreign key): CCF.Voxel primary key.
        """

        definition = """
        -> master.BrainRegion
        -> CCF.Voxel
        """

    @classmethod
    def retrieve_acronym(self, acronym):
        """Retrieve the DataJoint translation of the CCF acronym"""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", acronym).lower()

    @classmethod
    def voxel_query(self, x=None, y=None, z=None):
        """Given one or more coordinates, return unique brain regions

        Args:
            x (float): x coordinate.
            y (float): y coordinate.
            z (float): z coordinate.

        Raises:
            ValueError: Must specificy at least one dimension.
            NotImplementedError: Coming soon.
        """
        if not any(x, y, z):
            raise ValueError("Must specify at least one dimension")
        # query = self.Voxel  #  TODO: add utility function name lookup
        raise NotImplementedError("Coming soon")


@schema
class ParentBrainRegion(dj.Lookup):
    """Hierarchical structure between the brain regions.

    Attributes:
        BrainRegionAnnotation.BrainRegion (foreign key): BrainRegionAnnotation.BrainRegion primary key.
        Parent (query): parent brain region acronym from BrainRegion table
    """

    definition = """ # Hierarchical structure between the brain regions
    -> BrainRegionAnnotation.BrainRegion
    ---
    -> BrainRegionAnnotation.BrainRegion.proj(parent='acronym')
    """


# ---- HELPERS ----


def load_ccf_annotation(
    ccf_id, version_name, voxel_resolution, nrrd_filepath, ontology_csv_filepath
):
    """Load CCF annotation.

    For an example Allen brain atlas for mouse, see:
    http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017
    For the structure/ontology tree, see:
    https://community.brain-map.org/t/allen-mouse-ccf-accessing-and-using-related-data-and-tools/359
    (particularly the ontology file downloadable as CSV)

    Args:
        ccf_id (int): unique id to identify a new CCF dataset to be inserted.
        version_name (str): CCF version.
        voxel_resolution (float): voxel resolution in microns.
        nrrd_filepath (str): path to the .nrrd file for the volume data.
        ontology_csv_filepath (str): path to the .csv file for the brain region ontology.
    """
    ccf_key = {"ccf_id": ccf_id}
    if CCF & ccf_key:
        print(f"CCF ID {ccf_id} already exists!")
        return

    nrrd_filepath = pathlib.Path(nrrd_filepath)
    ontology_csv_filepath = pathlib.Path(ontology_csv_filepath)

    def to_snake_case(s):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()

    ontology = pd.read_csv(ontology_csv_filepath)

    stack, hdr = nrrd.read(nrrd_filepath.as_posix())  # AP (x), DV (y), ML (z)

    log.info(
        ".. loaded atlas brain volume of shape " + f"{stack.shape} from {nrrd_filepath}"
    )

    ccf_key = {"ccf_id": ccf_id}
    ccf_entry = {
        **ccf_key,
        "ccf_version": version_name,
        "ccf_resolution": voxel_resolution,
        "ccf_description": (
            f"Version: {version_name}"
            + f" - Voxel resolution (uM): {voxel_resolution}"
            + f" - Volume file: {nrrd_filepath.name}"
            + " - Region ontology file: "
            + ontology_csv_filepath.name
        ),
    }

    with dj.conn().transaction:
        CCF.insert1(ccf_entry)
        BrainRegionAnnotation.insert1(ccf_key)
        BrainRegionAnnotation.BrainRegion.insert(
            [
                dict(
                    ccf_id=ccf_id,
                    acronym=to_snake_case(r.acronym),
                    region_id=r.id,
                    region_name=r.safe_name,
                    color_code=r.color_hex_triplet,
                )
                for _, r in ontology.iterrows()
            ]
        )

        # Process voxels per brain region
        for idx, (region_id, r) in enumerate(tqdm(ontology.iterrows())):
            dj.conn().ping()
            region_id = int(region_id)

            log.info(
                ".. loading region {} ({}/{}) ({})".format(
                    region_id, idx, len(ontology), r.safe_name
                )
            )

            # extracting filled volumes from stack in scaled [[x,y,z]] shape,
            vol = np.array(np.where(stack == region_id)).T * voxel_resolution
            vol = pd.DataFrame(vol, columns=["x", "y", "z"])

            if not vol.shape[0]:
                log.info(
                    ".. region {} volume: shape {} - skipping".format(
                        region_id, vol.shape
                    )
                )
                continue
            else:
                log.info(".. region {} volume: shape {}".format(region_id, vol.shape))

            vol["ccf_id"] = [ccf_key["ccf_id"]] * len(vol)
            CCF.Voxel.insert(vol)

            vol["acronym"] = [to_snake_case(r.acronym)] * len(vol)
            BrainRegionAnnotation.Voxel.insert(vol)

    log.info(".. done.")


def load_parent_regions(ccf_id):
    raise NotImplementedError("Coming soon")
