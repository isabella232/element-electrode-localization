import os
import pathlib
import datajoint as dj

from element_animal import subject
from element_session import session_with_datetime as session
from element_electrode_localization import electrode_localization, coordinate_framework

from element_animal.subject import Subject
from element_session.session_with_datetime import Session
from element_array_ephys import probe, ephys_no_curation as ephys


if "custom" not in dj.config:
    dj.config["custom"] = {}

# overwrite dj.config['custom'] values with environment variables if available

dj.config["custom"]["database.prefix"] = os.getenv(
    "DATABASE_PREFIX", dj.config["custom"].get("database.prefix", "")
)

if "custom" not in dj.config:
    dj.config["custom"] = {}

db_prefix = dj.config["custom"].get("database.prefix", "")


# Activate schemas -------------
subject.activate(db_prefix + "subject", linking_module=__name__)
session.activate(db_prefix + "session", linking_module=__name__)
Session = session.Session

ephys.activate(db_prefix + "ephys", db_prefix + "probe", linking_module=__name__)
ProbeInsertion = ephys.ProbeInsertion
electrode_localization.activate(
    db_prefix + "electrode_localization",
    db_prefix + "coordinate_framework",
    linking_module=__name__,
)
