import importlib
import inspect
import datajoint as dj

import coordinate_framework

schema = dj.schema()


def activate(electrode_localization_schema_name, coordinate_framework_schema_name=None, *, create_schema=True,
             create_tables=True, linking_module=None):
    """
    activate(electrode_localization_schema_name, coordinate_framework_schema_name=None, *, create_schema=True, create_tables=True, linking_module=None)
        :param electrode_localization_schema_name: schema name on the database server to activate the `electrode_localization` element
        :param coordinate_framework_schema_name: schema name on the database server to activate the `coordinate_framework` element
         - may be omitted if the `probe` element is already activated
        :param create_schema: when True (default), create schema in the database if it does not yet exist.
        :param create_tables: when True (default), create tables in the database if they do not yet exist.
        :param linking_module: a module name or a module containing the
         required dependencies to activate the `electrode_localization` element:
            Upstream tables:
                + ProbeInsertion: table referenced by ElectrodePosition, typically identifying a Probe Insertion instance
                + Electrode: table referenced by ElectrodePosition, specifying an ephys electrode
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module),\
        "The argument 'dependency' must be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    # activate
    coordinate_framework.activate(coordinate_framework_schema_name, create_schema=create_schema,
                                  create_tables=create_tables)
    schema.activate(electrode_localization_schema_name, create_schema=create_schema,
                    create_tables=create_tables, add_objects=_linking_module.__dict__)


@schema
class ElectrodePosition(dj.Manual):
    definition = """
    -> ProbeInsertion
    """

    class ElectrodePosition(dj.Part):
        definition = """
        -> master
        -> Electrode
        ---
        -> coordinate_framework.CCF.Voxel
        """
