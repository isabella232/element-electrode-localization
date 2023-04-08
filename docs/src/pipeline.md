# Data Pipeline

Each of the DataJoint Elements are a set of tables for common neuroinformatics
modalities to organize, preprocess, and analyze data. Each node in the following diagram
is either a table in the Element itself or a table that would be connected to the
Element.

![pipeline](https://raw.githubusercontent.com/datajoint/element-electrode-localization/main/images/pipeline.svg)

The Element is separated into two schemas:

+ `coordinate_framework` ingests standard atlases and retains voxel-based lookup tables,
  including references to brain regions, acronyms, and standardized color
  codes.

+ `electrode_localization` pairs the above reference tables with Neuropixels electrode
  location data from the Element Array Ephys [probe schema](https://datajoint.com/docs/elements/element-array-ephys/0.2/concepts/#probe-schema-api-docs).

## `coordinate_framework` schema ([API docs](../api/element_electrode_localization/coordinate_framework))

| Table | Description |
| --- | --- |
| CCF | Common coordinate framework (CCF) identifier, version, resolution, and description. |
| CCF.Voxel | CCF voxel coordinates. |
| BrainRegionAnnotation | Name and voxels of each brain region associated with an atlas. |
| BrainRegionAnnotation.BrainRegion | Brain region name, acronym, identifier, and color code. |
| BrainRegionAnnotation.Voxel | Voxels associated with each brain region. |
| ParentBrainRegion | Hierarchical structure between the brain regions. |

- Note: Acronyms in DataJoint do not perfectly map on to the Allen Institute's published standard. By default, DataJoint databases are not case sensitive. Instead, acronyms are converted to [snake case](https://en.wikipedia.org/wiki/Snake_case) to avoid naming collisions. While we depart from the standard, preliminary interviews with users indicate no bias toward the official standard. Visit the [tutorial Jupyter notebook](./tutorials/08-electrode-localization.ipynb) for a demonstration of converting between the case sensitive and snake case standards.

## `electrode_localization` schema ([API docs](../api/element_electrode_localization/electrode_localization))

| Table | Description |
| --- | --- |
| ElectrodePosition | CCF voxels associated with a given probe insertion. |
| ElectrodePosition.Electrode | CCF voxels associated with each electrode. |
