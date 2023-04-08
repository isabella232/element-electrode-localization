# Concepts

## Modeling the Brain

Studies of brain anatomy and cellular morphology were once confined to single-subject
studies wherein in vitro slices were compared to develop a complete model of the brain.
With dyes, researchers could compare recordings to the reconstructed location of a given
recording device. Through clever experimental design, researchers could further
associate highly localized regions to their task-dependent function. Advances in 3D
modeling have permitted parallel advances in multi-subject averaged anatomical models.
An atlas serves as a shared reference frame for a given species.
[The Allen Institute](https://mouse.brain-map.org/) has been a leader in the development
of mouse atlases since 2007[^1], with regular
updates[^2] that provide researchers with a shared reference
frame in the study of functional neuroanatomy.

## Key Partnerships

Labs have developed project-specific DataJoint pipelines for pairing the coordinates of recording electrodes with the location in published atlases. The DataJoint team collaborated with several and interviewed these teams to understand their experiment workflow, associated tools, and interfaces. These teams include:

+ Mesoscale Activity Project
+ International Brain Lab

## Element Architecture

Each of the DataJoint Elements are a set of tables for common neuroinformatics
modalities to organize, preprocess, and analyze data. Each node in the following diagram
is either a table in the Element itself or a table that would be connected to the
Element.

![pipeline](https://raw.githubusercontent.com/datajoint/element-electrode-localization/main/images/pipeline.svg)

The Element is separated into two schemas:

+ `coordinate_framework` ingests standard atlases and retains voxel-based lookup tables,
  including references to brain region information, acronyms and standardized color
  codes.
+ `electrode_localization` pairs the above reference tables with Neuropixels probe
  location data in a `probe` schema, optionally from
  [Element Array Ephys](https://github.com/datajoint/element-array-ephys)

## Key Partnerships

In coordination with both the Mesoscale Activity Project and the International Brain
Lab, DataJoint developed mechanisms for pairing recording coordinates with the published
atlases in project-specific cases that have since been generalized.

## Pipeline Development and Limitations

The Element's table architecture was generalized from existing project-specific
pipelines such as International Brain Laboratory's
[iblapps](https://github.com/int-brain-lab/iblapps/wiki/) as well as the Allen
Institute's
[atlas files](https://community.brain-map.org/t/allen-mouse-ccf-accessing-and-using-related-data-and-tools/359).

One notable consession was made in development: acronyms in DataJoint do not perfectly
map on to the Allen Institute's published standard. By default, DataJoint databases are
not case sensitive. Instead, acronyms are converted to
[snake case](https://en.wikipedia.org/wiki/Snake_case) to avoid naming collisions. While
we depart from the standard, preliminary interviews with users indicate no bias toward
the official standard. Visit our
[localization notebook](https://github.com/datajoint/workflow-array-ephys/blob/main/notebooks/08-electrode-localization.ipynb)
for a demonstration of converting between the case sensitive and snake case standards.

## Roadmap

Further development of this Element is community driven. Upon user requests we will
continue adding features to this Element, such as improved region- and subregion-based
topological referencing.
