# DataJoint Element - Electrode Localization

+ This repository features a DataJoint pipeline design for localizing the Neuropixels 
electrodes within the 
[Allen Mouse Common Coordinate Framework (CCF)](http://atlas.brain-map.org).

+ The pipeline presented here is not a complete pipeline by itself, but rather a 
modular design of tables and dependencies specific to the electrode localization 
workflow. 

+ This modular pipeline element can be flexibly attached downstream 
to any particular design of an array electrophysiology pipeline, thus assembling a 
fully functional electrode localization pipeline.

+ See the [Element Electrode Localization documentation](https://elements.datajoint.org/description/electrode_localization/) for the background information and development timeline.

+ For more information on the DataJoint Elements project, please visit https://elements.datajoint.org.  This work is supported by the National Institutes of Health.

## Element architecture
<!-- ![element-electrode-localization](https://github.com/datajoint/element-electrode-localization/blob/main/images/diagram_electrode-localization.svg) -->

## Installation

+ Install `element-electrode-localization`
    ```
    pip install element-electrode-localization
    ```

+ Upgrade `element-electrode-localization` previously installed with `pip`
    ```
    pip install --upgrade element-electrode-localization
    ```

+ Install `element-interface`

    + `element-interface` is a dependency of `element-electrode-localization`, however
      it is not contained within `requirements.txt`.
     
    ```
    pip install "element-interface @ git+https://github.com/datajoint/element-interface"
    ```

## Usage

### Element activation

To activate the `element-electrode-localization`, ones need to provide:

1. Schema names
    + schema name for the `electrode` module

2. Upstream tables
     + 

3. Utility functions. See [example definitions](https://github.com/datajoint/workflow-array-ephys/blob/main/workflow_array_ephys/paths.py).
    + get_ephys_root_data_dir(): Returns your root data directory.
    + get_session_directory(): Returns the path of the session data relative to the
      root.

For more details, check the docstring of the `element-electrode-localization`:
```python
    help(electrode.activate)
```
### Example usage

See the [workflow-array-ephys project](https://github.com/datajoint/workflow-array-ephys) for an example usage of this Element.

## Citation

+ If your work uses DataJoint and DataJoint Elements, please cite the respective Research Resource Identifiers (RRIDs) and manuscripts.

+ DataJoint for Python or MATLAB
    + Yatsenko D, Reimer J, Ecker AS, Walker EY, Sinz F, Berens P, Hoenselaar A, Cotton RJ, Siapas AS, Tolias AS. DataJoint: managing big scientific data using MATLAB or Python. bioRxiv. 2015 Jan 1:031658. doi: https://doi.org/10.1101/031658

    + DataJoint ([RRID:SCR_014543](https://scicrunch.org/resolver/SCR_014543)) - DataJoint for `<Select Python or MATLAB>` (version `<Enter version number>`)

+ DataJoint Elements
    + Yatsenko D, Nguyen T, Shen S, Gunalan K, Turner CA, Guzman R, Sasaki M, Sitonic D, Reimer J, Walker EY, Tolias AS. DataJoint Elements: Data Workflows for Neurophysiology. bioRxiv. 2021 Jan 1. doi: https://doi.org/10.1101/2021.03.30.437358

    + DataJoint Elements ([RRID:SCR_021894](https://scicrunch.org/resolver/SCR_021894)) - Element Electrode Localization (version `<Enter version number>`)
