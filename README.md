# DataJoint Element - Electrode Localization

This repository is currently a work in progress.

See [Background](Background.md) for the background information and development timeline.

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

    + `element-interface` is a dependency of `element-electrode-localization`, however it is not contained within `requirements.txt`.
     
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
    + get_session_directory(): Returns the path of the session data relative to the root.

For more details, check the docstring of the `element-electrode-localization`:

    help(electrode.activate)

### Example usage

See the [workflow-array-ephys project](https://github.com/datajoint/workflow-array-ephys) for an example usage of this Element.