# Concepts

## Modeling the Brain

Studies of brain anatomy and cellular morphology were once confined to single-subject
studies wherein in vitro slices were compared to develop a complete model of the brain.
With dyes, researchers could compare recordings to the reconstructed location of a given
recording device. Through clever experimental design, researchers could further
associate highly localized regions to their task-dependent function. Advances in 3D
modeling have permitted parallel advances in multi-subject averaged anatomical atlases, 
which serve as a shared reference frame to study functional neuroanatomy.
The [Allen Institute](https://mouse.brain-map.org/){:target="_blank"} has been a leader in the development of such mouse atlases since 2007 
([Lein et al., Nature 2007](https://doi.org/10.1038/nature05453){:target="_blank"}; 
[Wang et al., Cell 2020](https://doi.org/10.1016/j.cell.2020.04.007){:target="_blank"}).

## Key Partnerships

Labs have developed project-specific DataJoint pipelines for pairing the coordinates of recording electrodes with the location in published atlases. The DataJoint team collaborated with several and interviewed these teams to understand their experiment workflow, associated tools, and interfaces. These teams include:

+ Mesoscale Activity Project
+ International Brain Lab

## Element Roadmap

Through our interviews and direct collaboration on the key projects, we identified the common motifs to create Element Electrode Localization with the repository hosted on [GitHub](https://github.com/datajoint/element-electrode-localization){:target="_blank"}.
Further development of this Element is community driven. Upon user requests we will
continue adding features to this Element, such as improved region- and subregion-based
topological referencing.

- [x] Generalize the table architecture from existing project-specific pipelines:

  - [x] International Brain Laboratory's 
[iblapps](https://github.com/int-brain-lab/iblapps/wiki/){:target="_blank"}

  - [x] Allen Institute's [atlas files](https://community.brain-map.org/t/allen-mouse-ccf-accessing-and-using-related-data-and-tools/359){:target="_blank"}
