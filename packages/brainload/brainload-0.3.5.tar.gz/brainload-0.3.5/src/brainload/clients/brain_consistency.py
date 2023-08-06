#!/usr/bin/env python
from __future__ import print_function
import sys
import brainload.nitools as nit
import brainload.qa as brainqa
import brainload.nitools as nit
import argparse
import logging

# To run this in dev mode (in virtual env, pip -e install of brainload active) from REPO_ROOT:
# PYTHONPATH=./src/brainload python src/brainload/clients/brain_consistency.py $SUBJECTS_DIR $SUBJECTS_DIR/subjects.txt -m area:volume:thickness:pial_lgi -v

def brain_consistency():
    """
    Brain data consistency checks.

    Simple script to check brain data consistency.
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Check brain data consistency.")
    parser.add_argument("subjects_dir", help="The directory that contains your subjects. Note: in most cases you can pass the environment variable SUBJECTS_DIR.")
    parser.add_argument("subjects_file", help="Text file containing all subjects that should be checked, one subject per line.")
    parser.add_argument("-m", "--measures-native", help="Which vertex-wise native space measure data to check (e.g., 'area' to check files 'surf/lh.area' and similar). Colon-separated string or 'None'. Defaults to 'area:volume:thickness'.", default="area:volume:thickness")
    parser.add_argument("-s", "--measures-standard", help="Which vertex-wise standard space measure data to check (e.g., 'area' to check files 'surf/lh.area.fwhmX.fsaverage.mgh' and similar). Colon-separated string or 'None'. Defaults to 'area:volume:thickness'.", default="area:volume:thickness")
    parser.add_argument("-a", "--average-subject", help="Name of the average subject (template) for standard space data (see '-s'). Defaults to 'fsaverage'.", default="fsaverage")
    parser.add_argument("-f", "--fwhm-list", help="The list of fwhm files to check for standard space data (see '-s'). Defaults to '0:5:10:15:20:25'.", default="0:5:10:15:20:25")
    parser.add_argument("-r", "--report", help="File name for the report in HTML format. If not given, no HTML report is written.", default=None)
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.", action="store_true")
    args = parser.parse_args()


    if args.verbose:
        print("---Brain Data Consistency Checks---")
        print("Using subjects_dir '%s' and subjects file '%s'." % (args.subjects_dir, args.subjects_file))
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)

    native_measures = args.measures_native.split(":")
    if args.measures_native == "None":
        native_measures = []
    standard_measures = args.measures_standard.split(":")
    if args.measures_standard == "None":
        standard_measures = []
    standard_fwhm_list = args.fwhm_list.split(":")
    subjects_list = nit.read_subjects_file(args.subjects_file)

    if args.verbose:
        print("Handling %d subjects." % (len(subjects_list)))
        print("Handling %d native space measures: %s" % (len(native_measures), ", ".join(native_measures)))
        print("Handling %d standard space measures using template subject '%s': %s" % (len(standard_measures), args.average_subject, ", ".join(standard_measures)))
        if len(standard_measures):
            print("Handling standard space measures at %d fwhm settings: %s" % (len(standard_fwhm_list), ", ".join(standard_fwhm_list)))



    bdc = brainqa.BrainDataConsistency(args.subjects_dir, subjects_list)
    bdc.average_subject = args.average_subject
    bdc.fwhm_list = standard_fwhm_list
    bdc.check_custom(native_measures, standard_measures)
    if args.report:
        bdc.save_html_report(args.report)

    sys.exit(0)


if __name__ == "__main__":
    brain_consistency()
