import os
import pathlib
import datajoint as dj
from element_lab import lab
from element_animal import subject
from element_session import session_with_datetime as session
from element_session.session_with_datetime import Session
from element_electrode_localization import electrode_localization, coordinate_framework
from element_lab.lab import Device as Equipment

from element_array_ephys import probe, ephys_no_curation as ephys
from element_animal.subject import Subject
from element_lab.lab import Lab, Project, Protocol, Source, User


if "custom" not in dj.config:
    dj.config["custom"] = {}

# overwrite dj.config['custom'] values with environment variables if available

dj.config["custom"]["database.prefix"] = os.getenv(
    "DATABASE_PREFIX", dj.config["custom"].get("database.prefix", "")
)

dj.config["custom"]["electrode_localization_root_data_dir"] = os.getenv(
    "ELECTRODE_LOCALIZATION_ROOT_DATA_DIR",
    dj.config["custom"].get("electrode_localization_root_data_dir", ""),
)

if "custom" not in dj.config:
    dj.config["custom"] = {}

db_prefix = dj.config["custom"].get("database.prefix", "")


# # Import the configured "ephys mode"
# ephys_mode = os.getenv("EPHYS_MODE", dj.config["custom"].get("ephys_mode", "acute"))
# if ephys_mode == "acute":
#     from element_array_ephys import ephys_acute as ephys
# elif ephys_mode == "chronic":
#     from element_array_ephys import ephys_chronic as ephys
# elif ephys_mode == "no-curation":
#     from element_animal.export.nwb import subject_to_nwb
#     from element_array_ephys import ephys_no_curation as ephys
#     from element_array_ephys.export.nwb import ecephys_session_to_nwb, write_nwb
#     from element_lab.export.nwb import element_lab_to_nwb_dict
#     from element_session.export.nwb import session_to_nwb
# elif ephys_mode == "precluster":
#     from element_array_ephys import ephys_precluster as ephys
# else:
#     raise ValueError(f"Unknown ephys mode: {ephys_mode}")


# Declare functions for retrieving data
def get_electrode_localization_dir():
    """Retrieve electrode_localization root data directory."""
    eloc_root_dirs = dj.config.get("custom", {}).get(
        "get_electrode_localization_dir", None
    )
    if not eloc_root_dirs:
        return None
    elif isinstance(eloc_root_dirs, (str, pathlib.Path)):
        return [eloc_root_dirs]
    elif isinstance(eloc_root_dirs, list):
        return eloc_root_dirs
    else:
        raise TypeError(
            "`get_electrode_localization_dir` must be a string, pathlib, or list"
        )


@lab.schema
class SkullReference(dj.Lookup):
    definition = """
    skull_reference   : varchar(60)
    """
    contents = zip(["Bregma", "Lambda"])


# Activate schemas -------------
lab.activate(db_prefix + "lab")
subject.activate(db_prefix + "subject", linking_module=__name__)
session.activate(db_prefix + "session", linking_module=__name__)
Session = session.Session
Experimenter = lab.User

# def get_session_directory(session_key):
#     session_directory = (session.SessionDirectory & session_key).fetch1("session_dir")
#     return pathlib.Path(session_directory)

# Activate ephys and electrode-localization schema -----------------------------------
ephys.activate(db_prefix + "ephys", db_prefix + "probe", linking_module=__name__)
ProbeInsertion = ephys.ProbeInsertion
electrode_localization.activate(
    db_prefix + "electrode_localization",
    db_prefix + "coordinate_framework",
    linking_module=__name__,
)
