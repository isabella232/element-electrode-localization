import logging
import pathlib

import datajoint as dj
import pandas as pd
import numpy as np
import nrrd


log = logging.getLogger(__name__)
schema = dj.schema()


def activate(schema_name, *, create_schema=True, create_tables=True):
    """
    activate(schema_name, create_schema=True, create_tables=True)
        :param schema_name: schema name on the database server to activate the `coordinate_framework` element
        :param create_schema: when True (default), create schema in the database if it does not yet exist.
        :param create_tables: when True (default), create tables in the database if they do not yet exist.
    """
    schema.activate(schema_name, create_schema=create_schema, create_tables=create_tables)


@schema
class CCF(dj.Lookup):
    definition = """  # Common Coordinate Framework
    ccf_id:             int             # CCF ID
    ---
    ccf_version:        int             # Allen CCF Version - e.g. CCFv3
    ccf_description='': varchar(255)    # CCFLabel Description
    """

    class Voxel(dj.Part):
        definition = """  # CCF voxel coordinates
        -> master
        x   :  int   # (um)  Anterior-to-Posterior (AP axis)
        y   :  int   # (um)  Superior-to-Inferior (DV axis)
        z   :  int   # (um)  Left-to-Right (ML axis)
        index(y, z)
        """


@schema
class BrainRegionAnnotation(dj.Lookup):
    definition = """
    -> CCF
    """

    class BrainRegion(dj.Part):
        definition = """
        -> master
        acronym: varchar(32)
        ---
        region_name: varchar(128)
        region_id=null: int
        color_code=null: varchar(6)  # hexcode of the color code of this region
        """

    class Voxel(dj.Part):
        definition = """
        -> master.BrainRegion
        -> CCF.Voxel
        """


@schema
class ParentBrainRegion(dj.Lookup):
    definition = """ # Hierarchical structure between the brain regions
    -> BrainRegionAnnotation.BrainRegion
    ---
    -> BrainRegionAnnotation.BrainRegion.proj(parent='acronym')
    """


# ---- HELPERS ----


def load_ccf_annotation(ccf_id, version_name, voxel_resolution,
                        nrrd_filepath, ontology_csv_filepath, colorcode_csv_filepath):
    """
    :param ccf_id: unique id to identify a new CCF dataset to be inserted
    :param version_name: CCF version
    :param voxel_resolution: voxel resolution in micron
    :param nrrd_filepath: path to the .nrrd file for the volume data
    :param ontology_csv_filepath: path to the .csv file for the brain region ontology
    :param colorcode_csv_filepath: path to the .csv file for the brain region color code

    For an example Allen brain atlas for mouse, see:
    http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017
    """
    nrrd_filepath = pathlib.Path(nrrd_filepath)
    ontology_csv_filepath = pathlib.Path(ontology_csv_filepath)
    colorcode_csv_filepath = pathlib.Path(colorcode_csv_filepath)

    regions = get_ontology_regions(ontology_csv_filepath, colorcode_csv_filepath)
    stack, hdr = nrrd.read(nrrd_filepath.as_posix())  # AP (x), DV (y), ML (z)

    log.info('.. loaded atlas brain volume of shape {} from {}'
             .format(stack.shape, nrrd_filepath))

    ccf_key = {'ccf_id': ccf_id}
    ccf_entry = {**ccf_key,
                 'ccf_version': version_name,
                 'ccf_description': f'Version: {version_name}'
                                    f' - Voxel resolution (uM): {voxel_resolution}'
                                    f' - Volume file: {nrrd_filepath.name}'
                                    f' - Region ontology file: {ontology_csv_filepath.name},'
                                    f' {colorcode_csv_filepath.name}'}

    with dj.conn().transaction:
        CCF.insert1(ccf_entry)
        BrainRegionAnnotation.insert1(ccf_key)
        BrainRegionAnnotation.BrainRegion.insert([
            dict(ccf_entry,
                 acronym=r.region_name,
                 region_id=region_id,
                 region_name=r.region_name,
                 color_code=r.hexcode) for region_id, r in regions.iterrows()])

        # Process voxels per brain region
        for idx, (region_id, r) in enumerate(regions.iterrows()):
            region_id = int(region_id)

            log.info('.. loading region {} ({}/{}) ({})'
                     .format(region_id, idx, len(regions), r.region_name))

            # extracting filled volumes from stack in scaled [[x,y,z]] shape,
            vol = (np.array(np.where(stack == region_id)).T * voxel_resolution)
            vol = pd.DataFrame(vol, columns=['x', 'y', 'z'])

            if not vol.shape[0]:
                log.info('.. region {} volume: shape {} - skipping'
                         .format(region_id, vol.shape))
                continue
            else:
                log.info('.. region {} volume: shape {}'.format(
                    region_id, vol.shape))

            vol['ccf_id'] = [ccf_key['ccf_id']] * len(vol)
            CCF.Voxel.insert(vol)

            vol['acronym'] = [r.region_name] * len(vol)
            BrainRegionAnnotation.Voxel.insert(vol)

    log.info('.. done.')


def get_ontology_regions(ontology_csv_filepath, colorcode_csv_filepath):
    regions = pd.read_csv(ontology_csv_filepath, header=None, index_col=0)
    regions.columns = ['region_name']
    hexcode = pd.read_csv(colorcode_csv_filepath, header=None, index_col=0)
    hexcode.columns = ['hexcode']

    return pd.concat([regions, hexcode], axis=1)
