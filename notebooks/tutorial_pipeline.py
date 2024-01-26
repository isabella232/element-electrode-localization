import os
import pathlib
import datajoint as dj
from element_animal import subject
from element_animal.subject import Subject
from element_interface.utils import find_full_path
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

dj.config["custom"]["ephys_root_data_dir"] = os.getenv(
    "EPHYS_ROOT_DATA_DIR", dj.config["custom"].get("ephys_root_data_dir", "")
)

db_prefix = dj.config["custom"].get("database.prefix", "")


# Declare functions for retrieving data
def get_ephys_root_data_dir():
    """Retrieve ephys root data directory."""
    ephys_root_dirs = dj.config.get("custom", {}).get("ephys_root_data_dir", None)
    if not ephys_root_dirs:
        return None
    elif isinstance(ephys_root_dirs, (str, pathlib.Path)):
        return [ephys_root_dirs]
    elif isinstance(ephys_root_dirs, list):
        return ephys_root_dirs
    else:
        raise TypeError("`ephys_root_data_dir` must be a string, pathlib, or list")


def get_electrode_localization_dir(probe_insertion_key: dict) -> str:
    """Return root directory of localization data for a given probe

    Args:
        probe_insertion_key (dict): key uniquely identifying one ephys.EphysRecording

    Returns:
        path (str): Full path to localization data for either SpikeGLX or OpenEphys
    """

    acq_software = (ephys.EphysRecording & probe_insertion_key).fetch1("acq_software")

    if acq_software == "SpikeGLX":
        spikeglx_meta_filepath = pathlib.Path(
            (
                ephys.EphysRecording.EphysFile
                & probe_insertion_key
                & 'file_path LIKE "%.ap.meta"'
            ).fetch1("file_path")
        )
        probe_dir = find_full_path(
            get_ephys_root_data_dir(), spikeglx_meta_filepath.parent
        )
    elif acq_software == "Open Ephys":
        probe_path = (ephys.EphysRecording.EphysFile & probe_insertion_key).fetch1(
            "file_path"
        )
        probe_dir = find_full_path(
            get_ephys_root_data_dir(), probe_path
        )

    return probe_dir


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
    db_prefix + "electrode_localization", db_prefix + "ccf", linking_module=__name__
)

ccf_id = 0  # Atlas ID
voxel_resolution = 100

nrrd_filepath = find_full_path(
    get_ephys_root_data_dir(), f"annotation_{voxel_resolution}.nrrd"
)
ontology_csv_filepath = find_full_path(get_ephys_root_data_dir(), "query.csv")


if (
    not (coordinate_framework.CCF & {"ccf_id": ccf_id})
    and nrrd_filepath.exists()
    and ontology_csv_filepath.exists()
):
    coordinate_framework.load_ccf_annotation(
        ccf_id=ccf_id,
        version_name="ccf_2017",
        voxel_resolution=voxel_resolution,
        nrrd_filepath=nrrd_filepath,
        ontology_csv_filepath=ontology_csv_filepath,
    )
