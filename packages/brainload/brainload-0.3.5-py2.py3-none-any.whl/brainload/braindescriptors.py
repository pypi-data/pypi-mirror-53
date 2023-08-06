"""
Collect various brain descriptors.

Functions to collect brain descriptors from neuroimaging data preprocessed with FreeSurfer.
"""

import os, sys
import numpy as np
import nibabel.freesurfer.io as fsio
from . import nitools as nit
from . import freesurferdata as fsd
from . import stats as blst
from . import annotations as blant
import logging
import collections

class BrainDescriptors:
    """
    Collects brain descriptors for one or more subjects.

    This class can parse all standard statistics files which are written by FreeSurfer when a subject is preprocessed using the recon-all pipeline. This includes
    brain segmentation stats (volume-based, like the ```stats/aseg.stats``` file), brain parcellation stats (surface-based, like ```?h.aparc.a2009s.stats```) and special stats file like the ```curv.stats``` files.

    It can also compute stats based on a parcellation atlas and any custom morphometry measure that you may have computed (e.g., local gyrifiaction index or some arbitrary vertex-wise measure you have computed yourself).

    You can export the resulting data to a CSV file so you can load them in your favorite statistical software later. (No, I did not mention AI.) If that favorite software happens to be python, you can just access the ```descriptor_names``` and ```descriptor_values``` properties of the class instead.
    """
    def __init__(self, subjects_dir, subjects_list, hemi='both'):
        self.subjects_dir = subjects_dir
        self.subjects_list = subjects_list
        self.descriptor_names = []
        self.descriptor_values = np.zeros((len(self.subjects_list), 0))
        self.fail_on_missing_files = False

        if hemi not in ('lh', 'rh', 'both'):
            raise ValueError("ERROR: hemi must be one of {'lh', 'rh', 'both'} but is '%s'." % hemi)
        if hemi == 'both':
            self.hemis = ['lh', 'rh']
        else:
            self.hemis = [hemi]
        logging.info("BrainDescriptors instance initialized, handling %s subjects in subjects_dir '%s'." % (len(self.subjects_list), self.subjects_dir))


    def add_parcellation_stats(self, atlas_list):
        """
        Add brain parcellation stats.

        Add brain parcellation stats for a list of atlases, i.e., annotation files.

        Parameters
        ----------
        atlas_list: list of strings
            The atlas names. E.g., ```['aparc', 'aparc.a2009s']```.
        """
        for hemi in self.hemis:
            for atlas in atlas_list:
                logging.info("Adding parcellation stats for atlas '%s', hemi '%s'." % (atlas, hemi))
                self._add_single_parcellation_stats(atlas, hemi)


    def _add_single_parcellation_stats(self, atlas, hemi):
        """
        Add brain parcellation atlas stats.

        Compute and add brain parcellation atlas stats for one hemisphere for all subjects, e.g., 'aparc' for stats/?h.aparc.annot. (Note that this function is not for segmentation stats like aseg.)

        Parameters
        ----------
        atlas: string
            The atlas name, e.g., 'aparc' for the annotation file 'stats/?h.aparc.annot'.

        hemi: string, one if 'lh' or 'rh'
            The hemisphere.
        """
        stats_filename = '%s.%s.stats' % (hemi, atlas)
        stats_table_type_list = blst.typelist_for_aparc_atlas_stats()
        logging.info("Getting group stats by row for atlas '%s' hemi '%s'." % (atlas, hemi))
        all_subjects_measures_dict, all_subjects_table_data_dict_by_region = blst.group_stats_by_row(self.subjects_list, self.subjects_dir, stats_filename, stats_table_type_list=stats_table_type_list)
        logging.info("Getting table column names.")
        table_column_names = blst.get_stats_table_column_names(self.subjects_dir, stats_filename, subject=self.subjects_list[0])

        # Add a prefix for the atlas and hemi to the keys in the dictionary, as these will become descriptor names (which should be unique).
        all_subjects_measures_dict_new = dict()
        for key in all_subjects_measures_dict:
            new_key = "%s_%s_%s" % (hemi, atlas, key)
            all_subjects_measures_dict_new[new_key] = all_subjects_measures_dict[key]
        all_subjects_measures_dict = all_subjects_measures_dict_new

        self._add_measure_dict_stats(all_subjects_measures_dict, atlas)
        self._add_all_subjects_table_data_stats_by_region(all_subjects_table_data_dict_by_region, atlas, table_column_names, hemi_tag=hemi)


    def _add_measure_dict_stats(self, all_subjects_measures_dict, atlas):
        for measure_unique_name in list(all_subjects_measures_dict.keys()):
            measure_data_all_subjects = all_subjects_measures_dict[measure_unique_name]
            self.descriptor_values = np.hstack((self.descriptor_values, np.expand_dims(measure_data_all_subjects, axis=1)))
            self.descriptor_names.append("stats_%s_measure_%s" % (atlas, measure_unique_name))


    def _add_all_subjects_table_data_stats(self, all_subjects_table_data_dict, atlas, ignore_columns=None, hemi_tag=None):
        if hemi_tag is None:
            hemi_tag = ""
        else:
            hemi_tag = "%s_" % (hemi_tag)

        if ignore_columns is None:
            ignore_columns = []
        region_colum_name = blst.stats_table_region_label_column_name()
        region_names = [rname.decode('utf-8') for rname in all_subjects_table_data_dict[region_colum_name][0]]

        for table_column_name in all_subjects_table_data_dict.keys():
            if table_column_name not in ignore_columns and table_column_name != region_colum_name:
                all_subjects_all_region_data = all_subjects_table_data_dict[table_column_name]
                self.descriptor_values = np.hstack((self.descriptor_values, all_subjects_all_region_data))
                for region_name in region_names:
                    self.descriptor_names.append("%sstats_%s_table_%s_%s" % (hemi_tag, atlas, table_column_name, region_name))


    def _add_all_subjects_table_data_stats_by_region(self, all_subjects_table_data_dict_by_region, atlas, table_column_names, hemi_tag=None):
        if hemi_tag is None:
            hemi_tag = ""
        else:
            hemi_tag = "%s_" % (hemi_tag)

        num_columns = len(table_column_names)
        num_regions = len(all_subjects_table_data_dict_by_region)
        logging.info("Parsing %s stats, handling %d table columns and %d rows (regions) for %d subjects." % (atlas, num_columns, num_regions, len(self.subjects_list)))

        all_subjects_all_region_data = np.zeros((len(self.subjects_list), num_columns * num_regions))  # init empty only

        for subject_index, subject_id in enumerate(self.subjects_list):
            all_data_for_subject = []
            for region_name in all_subjects_table_data_dict_by_region:
                logging.info("Adding data for region '%s', subject '%s' containing %d descriptor values" % (region_name, subject_id, len(all_subjects_table_data_dict_by_region[region_name][subject_id])))
                all_data_for_subject.extend(all_subjects_table_data_dict_by_region[region_name][subject_id])
            logging.info("Atlas %s: Descriptor data for subject '%s' contains %d values total over all regions." % (atlas, subject_id, len(all_data_for_subject)))
            all_subjects_all_region_data[subject_index,:] = np.array(all_data_for_subject)

        self.descriptor_values = np.hstack((self.descriptor_values, all_subjects_all_region_data))

        for region_name in all_subjects_table_data_dict_by_region:
            for table_column_name in table_column_names:
                self.descriptor_names.append("%sstats_%s_table_%s_%s" % (hemi_tag, atlas, table_column_name, region_name))


    def add_standard_stats(self):
        """
        Convenience function to add all descriptors which are computed by default when running Freesurfer v6 recon-all on a subject.
        """
        self.add_parcellation_stats(['aparc', 'aparc.a2009s'])
        self.add_segmentation_stats(['aseg', 'wmparc'])
        self.add_custom_measure_stats(['aparc'], ['area'])
        self.add_curv_stats()

        self.check_for_parcellation_stats_files(['aparc', 'aparc.a2009s'])
        self.check_for_segmentation_stats_files(['aseg', 'wmparc'])
        self.check_for_custom_measure_stats_files(['aparc'], ['area'])
        self.check_for_curv_stats_files()


    def check_for_custom_measure_stats_files(self, annot_list, morph_list, morph_file_format="curv"):
        """
        Check for custom annotation files.

        Check for the existence of custom annotation and morphometry files.

        Parameters
        ----------
        annot_list: list of strings
            The annotations (atlas file names), a typical entry in the list would be "aparc" or "aparc.a2009s".

        morph_list: list of strings
            The morphometry data, a typical entry in the list would be "area" or "thickness".

        morph_file_format: string, one of 'curv', 'mgh', or 'mgz'. Defaults to 'curv'.
        """
        for annot in annot_list:
            parts = ['label', "%s.annot" % (annot)]
            self.check_for_hemi_dependent_file(parts)

        if morph_file_format not in ('curv', 'mgh', 'mgz'):
            raise ValueError("ERROR: morph_file_format must be one of {'curv', 'mgh', 'mgz'} but is '%s'." % morph_file_format)

        if morph_file_format == "curv":
            morph_file_ext = ""
        else:
            morph_file_ext = ".%s" % (morph_file_format)

        for morphometry_measure in morph_list:
            parts = ['surf', "%s%s" % (morphometry_measure, morph_file_ext)]
            self.check_for_hemi_dependent_file(parts)


    def report_descriptors(self):
        """
        Print some information on descriptors to stdout.
        """
        print("subject_id " + " ".join(self.descriptor_names))
        for sidx, subject_id in enumerate(self.subjects_list):
            print("%s " % (subject_id), end="")
            for i in range(len(self.descriptor_names)):
                print("%.2f" % (self.descriptor_values[sidx,i]), end=" ")
            print("")
        logging.debug("self.descriptor_values has shape %s" % (str(self.descriptor_values.shape)))
        logging.debug("Found %d descriptor names." % (len(self.descriptor_names)))

        if len(self.descriptor_names) != self.descriptor_values.shape[1]:
            logging.error("Mismatch between number of descriptor names and values.")


    def check_for_parcellation_stats_files(self, atlas_list):
        for atlas in atlas_list:
            parts = ['stats', "%s.stats" % (atlas)]
            self.check_for_hemi_dependent_file(parts)

    def check_for_segmentation_stats_files(self, segmentation_list):
        for seg in segmentation_list:
            parts = ['stats', "%s.stats" % (seg)]
            self.check_for_hemi_independent_file(parts)


    def check_for_curv_stats_files(self):
        parts = ['stats', "curv.stats"]
        self.check_for_hemi_dependent_file(parts)


    def check_for_hemi_independent_file(self, parts):
        ok = []
        missing = []
        for subject_id in self.subjects_list:
            sfile = os.path.join(self.subjects_dir, subject_id, *parts)
            self._assign_file_state(sfile, ok, missing)
        self._report_on_file(sfile, ok, missing)


    def check_for_hemi_dependent_file(self, parts):
        """
        Check for hemi-dependent file.

        Check for the existence of a file that has an lh and an rh version.

        Parameters
        ----------
        parts: list of strings
            Path to file, relative to the subject's directory. The last list element should be the file name (all other ones are directories). The last element must NOT contain the prefix "lh." or "rh.", as these will be added automatically.
        """
        if len(parts) == 0:
            return
        for hemi in self.hemis:
            ok = []
            missing = []
            hemi_parts = parts.copy()
            hemi_parts[-1] = "%s.%s" % (hemi, hemi_parts[-1])
            for subject_id in self.subjects_list:
                sfile = os.path.join(self.subjects_dir, subject_id, *hemi_parts)
                self._assign_file_state(sfile, ok, missing)
            self._report_on_file(sfile, ok, missing)


    def _assign_file_state(self, sfile, ok, missing):
        """
        Assign file to dict.

        Assign the file to one of the two given dictionaries, depending on whether or not it exists.

        Parameters
        ----------
        sfile: string
            Path to a file.

        ok: list of strings
            The file name passed as `sfile` will be appended to this if the file exists.

        missing: list of strings
            The file name passed as `sfile` will be appended to this if the file does not exist.
        """
        if os.path.isfile(sfile):
            ok.append(sfile)
        else:
            missing.append(sfile)


    def _report_on_file(self, sfile, ok, missing):
        """
        Print file status.

        Print the number of missing and the number of OK instances of the file over all subjects.

        Parameters
        ----------
        sfile: string
            Path to a file.

        ok: list of strings
            The file name passed as `sfile` will be appended to this if the file exists.

        missing: list of strings
            The file name passed as `sfile` will be appended to this if the file does not exist.
        """
        print("%d MISSING, %d OK for file '%s'" % (len(missing), len(ok), sfile))



    def add_segmentation_stats(self, segmentation_list):
        """
        Add brain parcellation stats.

        Add brain parcellation stats. This add the data from the stats/aseg.stats file.

        Parameters
        ----------
        segmentation_list: list of string
            Each entry should be a valid FreeSurfer segmentation name, like ```aseg```. A file with that name has to exist in the subjects directory under ```stats/```, e.g., ```stats/aseg.stats``` for ```aseg```.
        """
        for seg in segmentation_list:
            logging.info("Adding segmenation stats for '%s'." % (seg))
            self.add_single_segmentation_stats(seg)


    def add_curv_stats(self):
        """
        Add surface curvature stats.

        Add brain surface curvature stats. This add the data from the ```stats/?h.curv.stats``` files.
        """
        for hemi in self.hemis:
            logging.info("Adding curv stats for hemi '%s'." % (hemi))
            all_subject_data_this_hemi = None
            for subject_id in self.subjects_list:
                curv_stat_names, curv_stat_values = blst.parse_curve_stats(subject_id, self.subjects_dir, hemi)
                if all_subject_data_this_hemi is None:
                    all_subject_data_this_hemi = curv_stat_values
                else:
                    all_subject_data_this_hemi = np.vstack((all_subject_data_this_hemi, curv_stat_values))
            self.descriptor_values = np.hstack((self.descriptor_values, all_subject_data_this_hemi))
            self.descriptor_names.extend(curv_stat_names)


    def add_single_segmentation_stats(self, atlas):
        """
        Add brain parcellation stats.

        Add brain parcellation stats. This add the data from the stats/aseg.stats file.

        Parameters
        ----------
        atlas: string
            A valid FreeSurfer segmentation name, like ```aseg```. A file with that name has to exist in the subjects directory under ```stats/```, e.g., ```stats/aseg.stats``` for ```aseg```.
        """
        all_subjects_measures_dict, all_subjects_table_data_dict = blst.group_stats_aseg(self.subjects_list, self.subjects_dir)

        self._add_measure_dict_stats(all_subjects_measures_dict, atlas)
        self._add_all_subjects_table_data_stats(all_subjects_table_data_dict, atlas, ignore_columns=['Index', 'SegId'])


    def add_custom_measure_stats(self, atlas_list, measure_list):
        """
        Add custom stats for a measure and atlas.

        Add custom stats for a measure and atlas. E.g., compute descriptive stats (min, max, mean, ...) for a measure like 'pial_lgi' in all regions of an atlas like 'aparc'.

        Parameters
        ----------
        atlas_list: list of string
            Each entry should be a valid FreeSurfer segmentation name, like ```aseg```. A file with that name has to exist in the subjects directory under ```stats/```, e.g., ```stats/aseg.stats``` for ```aseg```.

        measure_list: list of string
            A list of vertex-wise morphometry measurements, like ```volume```, ```thickness```, or ```area```. A hemisphere-dependent file with that name has to exist in the subjects directory under ```surf/```, e.g., ```surf/lh.area``` and ```surf/rh.area``` for the two hemispheres is the given string is ```area```.
        """
        for hemi in self.hemis:
            for atlas in atlas_list:
                for measure in measure_list:
                    logging.info("Adding custom measure stats for atlas '%s', measure '%s', hemi '%s'." % (atlas, measure, hemi))
                    self._add_custom_measure_stats_single(atlas, measure, hemi)


    def _add_custom_measure_stats_single(self, atlas, measure, hemi):
        """
        Add single custom measure stats.

        Add single custom measure stats.

        Parameters
        ----------
        atlas: string
            A valid FreeSurfer parcellation name, like ```aparc```.

        measure: string
            A vertex-wise morphometry measurement, like ```volume```, ```thickness```, or ```area```. A hemisphere-dependent file with that name has to exist in the subjects directory under ```surf/```, e.g., ```surf/lh.area``` and ```surf/rh.area``` for the two hemispheres is the given string is ```area```.

        hemi: string, one of 'lh' or 'rh'
            The hemisphere, given as 'lh' for left or 'rh' for right.
        """
        all_subjects_data = None
        label_name_subject = self.subjects_list[0]
        label_names = blant.get_atlas_region_names(atlas, self.subjects_dir, subject_id=label_name_subject)
        if label_names is None:
            raise ValueError("Loading region names for atlas '%s' failed, tried reading from annot file for subject '%s' in subjects directory '%s'." % (atlas, label_name_subject, self.subjects_dir))
        for subject_id in self.subjects_list:
            morphometry_data, morphometry_meta_data = fsd.subject_data_native(subject_id, self.subjects_dir, measure, hemi)
            try:
                region_data_per_hemi, _ = blant.region_data_native(subject_id, self.subjects_dir, atlas, hemi, morphometry_data, morphometry_meta_data)
            except Exception as e:
                region_data_per_hemi = dict()
                region_data_per_hemi[hemi] = dict()
            am_descriptor_data, am_descriptor_names = blant.region_stats(region_data_per_hemi, label_names)
            am_descriptor_names = ["%s_%s_%s" % (atlas, measure, n) for n in am_descriptor_names]
            if all_subjects_data is None:
                all_subjects_data = am_descriptor_data
            else:
                all_subjects_data = np.vstack((all_subjects_data, am_descriptor_data))
        self.descriptor_values = np.hstack((self.descriptor_values, all_subjects_data))
        self.descriptor_names.extend(am_descriptor_names)


    def _check_for_duplicate_descriptor_names(self):
        """
        Check for duplicate descriptor names.

        Debug function to check for duplicate descriptor names.

        Returns
        -------
        list of str
            The descriptor names that occur more than once. The list should be empty.
        """
        dups = [item for item, count in collections.Counter(self.descriptor_names).items() if count > 1]
        if dups:
            logging.warning("Duplicate descriptor names detected: %s" % (" ".join(dups)))
        return dups


    def check_for_NaNs(self, threshold=0.6):
        """
        Check for descriptors and subjects with all NaN values.

        Parameters
        ----------
        threshold: float
            The NaN threshold, subjects and descriptors for which the share of NaN values exceeds this threshold are reported. Must be between .0 and 1.0 to make sense. Defaults to 0.6.

        Returns
        -------
        subjects_over_threshold: list of string
            The subjects

        descriptors_over_threshold: list of string
            The descriptors

        nan_share_per_subject: numpy float array
            The share of NaN values for each subject. Numpy array with length n for the n subjects.

        nan_share_per_descriptor: numpy float array
            The share of NaN values for each descriptor. Numpy array with length m for the m descriptor.
        """
        if self.descriptor_values.shape[0] == 0 or self.descriptor_values.shape[1] == 0:
            return [], [], np.zeros((0, )), np.zeros((0, ))
        all_nan_subject_indices = np.all(np.isnan(self.descriptor_values), axis=0)[0]
        all_nan_subjects = np.array(self.subjects_list)[all_nan_subject_indices]
        logging.info("There are %d subjects which have only NaN descriptors values: %s" % (all_nan_subjects.shape[0], ", ".join(all_nan_subjects)))

        nan_share_per_subject = np.isnan(self.descriptor_values).sum(axis=0) / self.descriptor_values.shape[0]
        subjects_over_threshold = [s for s, n in zip(self.subjects_list, nan_share_per_subject) if n > threshold]
        logging.info("%d/%d Subjects over NaN threshold %f: %s" % (len(subjects_over_threshold), len(self.subjects_list), threshold, ", ".join(subjects_over_threshold)))

        all_nan_descriptor_indices = np.all(np.isnan(self.descriptor_values), axis=1)[0]
        all_nan_descriptors = np.array(self.descriptor_names)[all_nan_descriptor_indices]
        logging.info("There are %d descriptors for which all subjects have only NaN values: %s" % (all_nan_descriptors.shape[0], ", ".join(all_nan_descriptors)))

        nan_share_per_descriptor = np.isnan(self.descriptor_values).sum(axis=1) / self.descriptor_values.shape[1]
        descriptors_over_threshold = [d for d, n in zip(self.descriptor_names, nan_share_per_descriptor) if n > threshold]
        logging.info("%d/%d Descriptors over NaN threshold %f: %s" % (len(descriptors_over_threshold), len(self.descriptor_names), threshold, ", ".join(descriptors_over_threshold)))

        logging.info("In total, %d of the %d descriptor values are NaN." % (np.isnan(self.descriptor_values).sum(), np.ravel(self.descriptor_values).shape[0]))
        return subjects_over_threshold, descriptors_over_threshold, nan_share_per_subject, nan_share_per_descriptor


    def save(self, stats_file, subjects_file=None, delim=","):
        """
        Save the descriptors to files.

        Save the descriptors to text files in CSV format.

        Parameters
        ----------

        stats_file: string
            Path and file name for the CSV file that will hold the descriptor data.

        subjects_file: string, optional
            Path a filename of a text file. If given, the subject IDs will be written to this file, one per line. The order of the subjects matches the order of the data in the stats_file.

        delim: str
            Delimiter for stats_file, defaults to ",".

        Examples
        --------
        >>> bd.save("braindescriptors.csv", subjects_file="subjects.txt")
        """
        if subjects_file is not None:
            nit.write_subjects_file(subjects_file, self.subjects_list)

        np.savetxt(stats_file, self.descriptor_values, delimiter=delim, header=delim.join(self.descriptor_names))
