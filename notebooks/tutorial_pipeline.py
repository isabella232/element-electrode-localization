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

if "custom" not in dj.config:
    dj.config["custom"] = {}

db_prefix = dj.config["custom"].get("database.prefix", "")


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


# Activate schemas -------------
lab.activate(db_prefix + "lab")
subject.activate(db_prefix + "subject", linking_module=__name__)
Experimenter = lab.User
Session = session.Session
session.activate(db_prefix + "session", linking_module=__name__)


ephys.activate(db_prefix + "ephys", db_prefix + "probe", linking_module=__name__)
ProbeInsertion = ephys.ProbeInsertion
electrode_localization.activate(
    db_prefix + "electrode_localization",
    db_prefix + "coordinate_framework",
    linking_module=__name__,
)
