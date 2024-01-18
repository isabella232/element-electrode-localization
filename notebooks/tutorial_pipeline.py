import os
import pathlib
import datajoint as dj
from element_animal import subject
from element_animal.subject import Subject
from element_array_ephys import probe, ephys_acute as ephys
from element_lab import lab
from element_lab.lab import Lab, Location, Project, Protocol, Source, User
from element_lab.lab import User as Experimenter
from element_session import session_with_datetime as session
from element_session.session_with_datetime import Session
from element_electrode_localization import electrode_localization, coordinate_framework

if "custom" not in dj.config:
    dj.config["custom"] = {}

# overwrite dj.config['custom'] values with environment variables if available

dj.config["custom"]["database.prefix"] = os.getenv(
    "DATABASE_PREFIX", dj.config["custom"].get("database.prefix", "")
)

if "custom" not in dj.config:
    dj.config["custom"] = {}

db_prefix = dj.config["custom"].get("database.prefix", "")


@lab.schema
class SkullReference(dj.Lookup):
    definition = """
    skull_reference   : varchar(60)
    """
    contents = zip(["Bregma", "Lambda"])


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
