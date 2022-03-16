import datajoint as dj


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
    # CCF Dataset Information
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


