# SDK gear to calculate intensity value statistics for tumor regions

This gear extracts intensity value statistics from an input image, within enhancing, non-enhancing, and whole-tumor (enhancing+non-enhancing+cystic) regions and injects the results as file-level metadata on Flywheel.

## Usage

Run at the file-level.

### Inputs

* input-file: Image to process 

### Configuration

* __debug__ (boolean, default False): Include debug statements in output.

### Limitations

Current limitations of the gear are as follows:

* tumor segmentation file must be within same acquisition as input image and have "ManualSeg" in file name