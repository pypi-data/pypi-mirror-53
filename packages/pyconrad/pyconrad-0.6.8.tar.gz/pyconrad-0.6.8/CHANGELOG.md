# CHANGELOG

## 0.6.8

* [x] Automatically download newest ImageJ on installation

## 0.6.6

* [x] Lock jpype version to 0.7 (0.8 will bring breaking changes)

## 0.6.1

* [x] Re-enable access to private Java members

## 0.6

* [x] Fix breaking API changes in JPype 0.7 (JPype 0.7 is required now)

## 0.5.1

* [x] Fix loading of filter (requires CONRAD patch `8674665`)
* [x] Allow omitting `--dev-dirs` argument for `pyconrad_run`

## 0.4.4

* [x] Set imagej calibration to grid.spacing/origin in pyconrad.imshow
* [x] Improve warnig when `import pyopencl` fails

## 0.4

* [x] Update to CONRAD version 1.1.10

## 0.3

* [x] Update to CONRAD version 1.0.9
* [x] Add pyconrad.config.get_projection_matrices()

## 0.2.6

* [x] Let environment variable `CONRAD_DEV_DIRS` change CONRAD development directories
* [x] Fix broken `procbridge` import

## 0.2.5

* [x] Make `Grays` the default LUT again

## 0.2.4

* [x] Apply LUT to correct ImagePlus and make 'Fire' default LUT for pyconrad.imshow

## 0.2.2 -- 0.2.3

* [x] Fix `README.rst`

## 0.2.1

* [x]  Improve `pyconrad.imshow`:
        -  Add `lut` and `run` parameter to run ImageJ commands
        -  Automatically try to guess if channel information is in fastest index and swap axes accordingly

## 0.1.7

* [x]  Add OpenVDB support to conrad_imagej

## 0.1.6

* [x]  Revert single instance mode as it is causing problems on some computers
* [x]  Add origin and spacing parameter to pyconrad.imshow

## 0.1.5

* [x]  Single instance mode for `conrad_imagej`
* [x]  More dynamic defaults for launched JVM

## 0.1.4

* [x]  Fix `pyconrad.imshow`

## 0.1.3

* [x]  Add convinience methods:
        - pyconrad.close_all_windows,
        - pyconrad.imshow
        - pyconrad.to_conrad_grid

## 0.1.2

* [x]  Fix issue #12: Getting rid of the raw data opener
* [x]  Fix issue with cl.array.shape that changed to be of type list[np.int32] instead of list[int]

## 0.1.0

* [x]  Full support of VTK files (also reading)
* [x]  Improvements for conrad_imagej (support of relative paths, support for .npy-files)

## 0.0.9

* Conrad 1.0.8
* Example for custom pyopencl kernel on OpenCLGrids

## 0.0.8.3

* fix problem with MultiChannelGrid

## 0.0.8

* [x]  OpenCL support:
  * [x]  Get CONRAD's OpenCL device, command queue, context
  * [x]  Create OpenCLGrids from Numpy
  * [x]  Upload/Download numpy
  * [x]  Efficient OpenCLMemory/create OpenCLGrid from pyopencl.array.Array
  * [x]  Add example
* [x]  More convenience functions in pyopencl.config
* [x]  Better desktop integration for conrad_imagej:
  * [x]  Add .desktop files
  * [x]  Support for .vtk, .np and  .npz support
