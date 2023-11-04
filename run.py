#!/usr/bin/env python
"""The run script."""
import logging
import sys
import typing as t
import os

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_functions.main import run
from fw_gear_functions.parser import parse_config
from fw_gear_functions.util import create_metadata

log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parse config and run."""
    fw, file_path, file_type, config = parse_config(context)
    file_ = context.get_input("input-file")

    # get parent project
    acq = context.client.get_acquisition(file_["hierarchy"]["id"])
    # project = context.client.get(acquisition.parents.project)

    # download the tumor segmentation file from the same acquisition
    for file in acq.files:
        if 'ManualSeg' in file.name:
            seg_filename = file.name
            acq.download_file(seg_filename, seg_filename)

    # process
    fe = run( 
        file_path,
        seg_filename,
    )

    # Tag file
    tag = config.get("tag")
    context.metadata.add_file_tags(file_, t.cast(str, tag))

    # create .metadata.json
    create_metadata(context, fe)

    # clean up temp files
    os.remove(seg_filename)

    return 0

if __name__ == "__main__":
    with GearToolkitContext(fail_on_validation=False) as context:
        try:
            context.init_logging()
            status = main(context)
        except Exception as exc:
            log.exception(exc)
            status = 1

    sys.exit(status)
