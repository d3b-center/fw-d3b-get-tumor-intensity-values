# SDK gear to extract slide metadata

This gear uses OpenSlide to extract file metadata from a pathology slide file and inject it as file-level metadata on Flywheel.

## Usage

Run at the file-level.

### Inputs

* input-file: File to process 

### Configuration

* __debug__ (boolean, default False): Include debug statements in output.

### Limitations

Current limitations of the gear are as follows:

* this gear was tested with Aperio SVS files only, future testing may be necessary for additional file types (although OpenSlide can handle multiple file types)
