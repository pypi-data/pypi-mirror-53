"""
OXASL plugin for processing multiphase ASL data

Copyright (c) 2019 Univerisity of Oxford
"""
import numpy as np

from maskslic import perfslic

from fsl.wrappers import LOAD
from fsl.data.image import Image

from oxasl import basil
from oxasl.options import OptionCategory, IgnorableOptionGroup
from oxasl.reporting import Report
from oxasl.wrappers import fabber

from ._version import __version__

def _run_fabber(wsp, options, desc):
    """
    Run Fabber and write the output to a workspace
    """
    wsp.log.write("  - %s     " % desc)
    result = fabber(options, output=LOAD, progress_log=wsp.log, log=wsp.fsllog)
    wsp.log.write(" - DONE\n")

    for key, value in result.items():
        setattr(wsp, key, value)

    if result["logfile"] is not None and wsp.savedir is not None:
        wsp.set_item("logfile", result["logfile"], save_fn=str)
    return result

def _get_mean_signal(data, roi):
    """
    :return: Data array same shape as data but where each value or timeseries
             takes the mean value of all other voxels in the same ROI label
    """
    out_data = np.zeros(data.shape)
    for region in np.unique(roi):
        if data.ndim > 3:
            out_data[roi == region] = np.mean(data[roi == region], axis=0)
        else:
            out_data[roi == region] = np.mean(data[roi == region])
    return out_data

def _mp_fabber_options(wsp):
    """
    :return: General Fabber options for multiphase decoding
    """
    # General options. note that the phase is always PSP number 1
    options = {
        "method" : "vb",
        "noise" : "white",
        "model" : "asl_multiphase",
        "data" : wsp.asldata,
        "mask" : wsp.rois.mask,
        "nph" : wsp.asldata.nphases,
        "ntis" : wsp.asldata.ntis,
        "repeats" : wsp.asldata.rpts[0], # We have already checked repeats are fixed
        "save-mean" : True,
        "save-model-fit" : True,
        "max-iterations": 30,
        "PSP_byname1" : "phase",
        "PSP_byname1_prec" : 0.2,
    }

    # Spatial mode
    if wsp.mp_spatial:
        options.update({
            "method" : "spatialvb",
        })

        if wsp.mp_spatial_phase:
            # Make the phase a spatial prior
            options["PSP_byname1_type"] = "M"
        else:
            # Make the magnitudes and offsets spatial priors
            prior = 2
            for pld_idx in range(wsp.asldata.ntis):
                options.update({
                    "PSP_byname%i" % prior: "mag%i" % (pld_idx+1),
                    "PSP_byname%i_type" % prior : "M",
                    "PSP_byname%i" % (prior+1): "offset%i" % (pld_idx+1),
                    "PSP_byname%i_type" % (prior+1) : "M",
                })

            # Special case if we have only 1 PLD the magnitude and offset
            # parameters are named differently for compatibility
            options["PSP_byname2"] = "mag"
            options["PSP_byname3"] = "offset"

    # Additional user-specified multiphase fitting options override the above
    options.update(wsp.ifnone("mp_options", {}))

    return options

def decode_mp(wsp):
    """
    Run multiphase decoding on a full multiphase data set
    """
    if wsp.mp is None:
        wsp.sub("mp")

    wsp.log.write("\nPerforming multiphase decoding:\n")
    if wsp.asldata.is_var_repeats():
        raise ValueError("Multiphase ASL data with variable repeats not currently supported")

    # Make sure phase cycles are together in the data and data for each PLD is in a block
    wsp.mp.asldata = wsp.asldata.reorder(out_order="lrt")

    # Prepare a data set to put each decoded PLD into
    diffdata = np.zeros(list(wsp.asldata.data.shape)[:3] + [wsp.asldata.ntis])

    # Get the Fabber options
    options = _mp_fabber_options(wsp)

    if wsp.mp_biascorr:
        nsv = wsp.ifnone("mp_biascorr_sv", 8)
        comp = wsp.ifnone("mp_biascorr_comp", 0.1)
        sigma = wsp.ifnone("mp_biascorr_sigma", 0.5)
        wsp.log.write("  - Using supervoxel-based bias correction\n")
        wsp.log.write("  - Number of supervoxels: %i" % nsv)
        wsp.log.write("  - Compactness: %f" % comp)
        wsp.log.write("  - Pre-smoothing width: %i" % sigma)

        # Initial biased Fabber run
        wsp.mp.sub("step1")
        _run_fabber(wsp.mp.step1, options, "Step 1: Running initial biased fit")

        # Supervoxel clustering on phase. Note that supervoxels are labelled from zero
        # with -1 for 'outside mask', but we add 1 so they can be interpreted as an ROI
        sv_roi = perfslic(wsp.mp.step1.mean_phase.data, wsp.rois.mask.data,
                          n_supervoxels=nsv, compactness=comp, sigma=sigma,
                          spacing=wsp.asldata.pixdim[:3], recompute_seeds=True,
                          seed_type='nplace')  + 1
        wsp.mp.step1.sv = Image(image=sv_roi, name="sv", header=wsp.asldata.header)

        if wsp.ifnone("mp_biascorr_simple", False):
            # Simple method - just use the mean phase in each supervoxel
            wsp.log.write("  - Using simplified form of bias correction\n")
            phase = wsp.mp.step1.mean_phase
            final_step = 2
        else:
            # Michael's suggested approach - average signal in ROI regions
            # to increase SNR and fit phase which should be less biased
            wsp.mp.sub("step2")
            wsp.mp.step2.asldata_sv = wsp.asldata.derived(_get_mean_signal(wsp.asldata.data, sv_roi))
            options["data"] = wsp.mp.step2.asldata_sv
            _run_fabber(wsp.mp.step2, options, "Step 2: Fitting mean signal in supervoxels")
            phase = wsp.mp.step2.mean_phase
            final_step = 3

        # Run Fabber finally with the phase fixed
        wsp.mp.sub("step%i" % final_step)
        phase_prior = Image(image=_get_mean_signal(phase.data, sv_roi), name="phase_prior", header=wsp.asldata.header)
        options.update({
            "data" : wsp.asldata,
            "PSP_byname1_type" : "I",
            "PSP_byname1_image" : phase_prior,
            "PSP_byname1_prec" : 1e12,
        })
        result = _run_fabber(getattr(wsp.mp, "step%i" % final_step), options, "Step %i: Running final fit with fixed phase" % final_step)
    else:
        # No bias correction - just basic fabber run
        result = _run_fabber(wsp.mp, options, "Performing multiphase decoding")

    # Combine final output as diffdata
    if wsp.asldata.ntis == 1:
        diffdata[..., 0] = result["mean_mag"].data
    else:
        for idx in range(wsp.asldata.ntis):
            diffdata[..., idx] = result["mean_mag%i" % (idx+1)].data

    # Set the full multiphase-decoded differenced data output on the workspace
    wsp.mp.asldata_decoded = wsp.mp.asldata.derived(diffdata, iaf='diff', order='rt', rpts=1)
    wsp.log.write("\nDONE multiphase decoding\n")

def model_mp(wsp):
    """
    Do modelling on multiphase ASL data

    :param wsp: Workspace object

    Required workspace attributes
    -----------------------------

      - ``asldata`` - ASLImage containing multiphase data

    Optional workspace attributes
    -----------------------------

    See ``MultiphaseOptions`` for other options

    Workspace attributes updated
    ----------------------------

      - ``mp``         - Sub-workspace containing multiphase decoding output
      - ``basil``      - Sub-workspace containing modelling of decoded output
      - ``output``     - Sub workspace containing native/structural/standard space
                         parameter maps
    """
    from oxasl import oxford_asl

    # Do multiphase decoding
    decode_mp(wsp)

    # Do conventional ASL modelling
    wsp.sub("basil")
    wsp.basil.asldata = wsp.mp.asldata_decoded
    basil.basil(wsp.basil, output_wsp=wsp.basil)

    # Write output
    wsp.sub("output")
    oxford_asl.output_native(wsp.output, wsp.basil)

    # Re-do registration using PWI map.
    oxford_asl.redo_reg(wsp, wsp.output.native.perfusion)

    # Write output in transformed spaces
    oxford_asl.output_trans(wsp.output)

    wsp.log.write("\nDONE processing\n")

class MultiphaseOptions(OptionCategory):
    """
    OptionCategory which contains options for preprocessing multiphase ASL data
    """
    def __init__(self, **kwargs):
        OptionCategory.__init__(self, "oxasl_mp", **kwargs)

    def groups(self, parser):
        groups = []
        group = IgnorableOptionGroup(parser, "Multiphase Options", ignore=self.ignore)
        group.add_option("--mp-spatial", help="Enable spatial smoothing on multiphase fitting step", action="store_true", default=False)
        group.add_option("--mp-spatial-phase", help="Perform spatial regularization on the phase rather than the magnitude", action="store_true", default=False)
        group.add_option("--mp-options", help="File containing additional options for multiphase fitting step", type="optfile")
        group.add_option("--mp-biascorr", help="Use supervoxel-based bias correction", action="store_true", default=False)
        group.add_option("--mp-biascorr-sv", help="Number of supervoxels to use in bias correction", type="int", default=8)
        group.add_option("--mp-biascorr-comp", help="Supervoxels compactness to use in bias correction", type="float", default=0.1)
        group.add_option("--mp-biascorr-sigma", help="Pre-supervoxel smoothing width in bias correction", type="float", default=0.5)
        group.add_option("--mp-biascorr-simple", help="Use simplified form of supervoxel-based bias correction", action="store_true", default=False)
        groups.append(group)
        return groups
