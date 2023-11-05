"""Main module."""
import logging
import os

from fw_core_client import CoreClient
from flywheel_gear_toolkit import GearToolkitContext
import flywheel

from .run_level import get_analysis_run_level_and_hierarchy

import nibabel as nib
import numpy as np

log = logging.getLogger(__name__)

fw_context = flywheel.GearContext()
fw = fw_context.client

def process(input_path, seg_filename):
    """Process `file_path` and returns a `flywheel.FileEntry` and its corresponding meta.

    Args:
        input_path (Path-like): Path to input-file.
        seg_filename
    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
    """

    file_dictionary = {'TumorSegIntensity':{}}

    im = nib.load(input_path).get_fdata()
    im = np.rint(im)

    mask = nib.load(seg_filename).get_fdata()
    mask = np.rint(mask)

    enhancing_mask = np.logical_and(mask >= 1, mask <= 1)
    nonenhancing_mask = np.logical_and(mask >= 2, mask <= 2)
    wt_mask = np.logical_and(mask >= 1, mask <= 3)

    im_enhancing = im * enhancing_mask
    enhancing_voxels = im_enhancing[im_enhancing!=0]
    if len(enhancing_voxels) > 0: # if there are remaining voxels
        file_dictionary['TumorSegIntensity']['enhancing_mean'] = np.mean(enhancing_voxels)
        file_dictionary['TumorSegIntensity']['enhancing_median'] = np.median(enhancing_voxels)
        file_dictionary['TumorSegIntensity']['enhancing_stdev'] = np.std(enhancing_voxels)

    im_nonenhancing = im * nonenhancing_mask
    nonenhancing_voxels = im_nonenhancing[im_nonenhancing!=0]
    if len(nonenhancing_voxels) > 0: # if there are remaining voxels
        file_dictionary['TumorSegIntensity']['nonenhancing_mean'] = np.mean(nonenhancing_voxels)
        file_dictionary['TumorSegIntensity']['nonenhancing_median'] = np.median(nonenhancing_voxels)
        file_dictionary['TumorSegIntensity']['nonenhancing_stdev'] = np.std(nonenhancing_voxels)

    im_wt = im * wt_mask
    wt_voxels = im_wt[im_wt!=0]
    if len(wt_voxels) > 0: # if there are remaining voxels
        file_dictionary['TumorSegIntensity']['wt_mean'] = np.mean(wt_voxels)
        file_dictionary['TumorSegIntensity']['wt_median'] = np.median(wt_voxels)
        file_dictionary['TumorSegIntensity']['wt_stdev'] = np.std(wt_voxels)

    fe = {"info": file_dictionary}
    return fe

def run(input_path, seg_filename):
    """Processes file at file_path.

    Args:
        file_type (str): String defining file type.
        file_path (AnyPath): A Path-like to file input.
        project (flywheel.Project): The flywheel project the file is originating
            (Default: None).

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.

    """
    fe = process(
        input_path, seg_filename
    )
    return fe