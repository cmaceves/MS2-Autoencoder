import xmltodict
import struct
import os
import time
import zlib
import binascii
import spectrum_alignment
import ming_psm_library
import ming_numerical_utilities
from collections import defaultdict

class Spectrum:
    def __init__(self, filename, scan, index, peaks, mz, charge, ms_level, collision_energy=0.0, fragmentation_method="NO_FRAG", precursor_intensity=0.0, totIonCurrent=0.0):
        self.filename = filename
        self.scan = scan
        self.peaks = peaks
        self.mz = mz
        self.charge = charge
        self.index = index
        self.ms_level = ms_level
        self.retention_time = 0.0
        self.collision_energy = collision_energy
        self.fragmenation_method = fragmentation_method
        self.precursor_intensity = precursor_intensity
        self.totIonCurrent = totIonCurrent

    def get_mgf_string(self):
        output_lines = []
        output_lines.append("BEGIN IONS")
        output_lines.append("SCANS=" + str(self.scan))
        output_lines.append("PEPMASS=" + str(self.mz))
        output_lines.append("CHARGE=" + str(self.charge))
        output_lines.append("COLLISION_ENERGY=" + str(self.collision_energy))
        output_lines.append(self.get_mgf_peak_string())
        output_lines.append("END IONS")

        return "\n".join(output_lines)

    def get_mgf_peak_string(self):
        output_string = ""
        for peak in self.peaks:
            output_string += str(peak[0]) + "\t" + str(peak[1]) + "\n"

        return output_string

    @staticmethod
    def get_tsv_header():
        return "filename\tspectrumindex\tspectrumscan\tcharge\tmz"

    def get_max_mass(self):
        max_mass = 0.0
        for peak in self.peaks:
            max_mass = max(max_mass, peak[0])
        return max_mass

    #Straight up cosine between two spectra
    def cosine_spectrum(self, other_spectrum, peak_tolerance):
        total_score, reported_alignments = spectrum_alignment.score_alignment(self.peaks, other_spectrum.peaks, self.mz * self.charge, other_spectrum.mz * other_spectrum.charge, peak_tolerance, self.charge)
        return total_score, len(reported_alignments)

    #Looks at windows of a given size, and picks the top peaks in there
    def window_filter_peaks(self, window_size, top_peaks):
        new_peaks = window_filter_peaks(self.peaks, window_size, top_peaks)
        self.peaks = new_peaks

    def filter_to_top_peaks(self, top_k_peaks):
        sorted_peaks = sorted(self.peaks, key=lambda peak: peak[1], reverse=True)
        sorted_peaks = sorted_peaks[:top_k_peaks]
        sorted_peaks = sorted(sorted_peaks, key=lambda peak: peak[0], reverse=False)
        self.peaks = sorted_peaks

    def filter_precursor_peaks(self):
        new_peaks = filter_precursor_peaks(self.peaks, 20.0, self.mz)
        self.peaks = new_peaks

    def filter_noise_peaks(self, min_snr):
        average_noise_level = ming_numerical_utilities.calculate_noise_level_in_peaks(self.peaks)
        new_peaks = []
        for peak in self.peaks:
            if peak[1] > average_noise_level * min_snr:
                new_peaks.append(peak)
        self.peaks = new_peaks

    def filter_peak_mass_range(self, lower, higher):
        new_peaks = []
        for peak in self.peaks:
            if peak[0] < lower or peak[0] > higher:
                new_peaks.append(peak)
        self.peaks = new_peaks

    def generated_spectrum_vector(self, peptide=None, attenuation_ratio=0.0, tolerance=0.5, bin_size=1):
        peaks_to_vectorize = self.peaks
        max_mass = 1500

        if peptide != None:
            charge_set = range(1, self.charge + 1)
            theoretical_peaks = ming_psm_library.create_theoretical_peak_map(self.peptide, ["b", "y", "b-H2O", "b-NH3", "y-H2O", "y-NH3", "a"], charge_set=charge_set)
            annotated_peaks, unannotated_peaks = ming_psm_library.extract_annotated_peaks(theoretical_peaks, self.peaks, tolerance)
            new_peaks = annotated_peaks
            if attenuation_ratio > 0:
                for unannotated_peak in unannotated_peaks:
                    unannotated_peak[1] *= attenuation_ratio
                    new_peaks.append(unannotated_peak)
            peaks_to_vectorize = sorted(new_peaks, key=lambda peak: peak[0])

        #Doing
        peak_vector = ming_numerical_utilities.vectorize_peaks(self.peaks, max_mass, bin_size)

        return peak_vector

    def get_number_of_signal_peaks(self, SNR_Threshold=5):
        return ming_numerical_utilities.calculate_signal_peaks_in_peaklist(self.peaks, SNR_Threshold)

    def get_number_of_peaks_within_percent_of_max(self, percent=1.0):
        max_peak_intensity = 0.0
        for peak in self.peaks:
            max_peak_intensity = max(peak[1], max_peak_intensity)

        intensity_threshold = percent / 100.0 * max_peak_intensity

        number_of_peaks = 0
        for peak in self.peaks:
            if peak[1] > intensity_threshold:
                number_of_peaks += 1

        return number_of_peaks

    """Gives sum of intensity of all spectrum peaks"""
    def get_total_spectrum_intensity(self):
        total_peak_intensity = 0
        for peak in self.peaks:
            total_peak_intensity += peak[1]
        return total_peak_intensity

#######
def load_mzxml_file(filename, drop_ms1=False):
    output_ms1 = []
    output_ms2 = []

    struct_iter_ok = True
    canary = True

    with open(filename) as fd:
        xmltodict_start = time.time()
        mzxml = xmltodict.parse(fd.read())
        xmltodict_end = time.time()
        print("XML time: " + str(xmltodict_end - xmltodict_start))
        read_scans = mzxml['mzXML']['msRun']['scan']
        filename_output = os.path.split(filename)[1]
        index = 1
        for scan in read_scans:
            # print(scan)
            ms_level, spectrum, struct_iter_ok, canary = read_mzxml_scan(scan, index, filename_output, struct_iter_ok, canary, drop_ms1)
            index += 1
            if ms_level == 1:
                if drop_ms1 == False:
                    output_ms1.append(spectrum)
            if ms_level == 2:
                output_ms2.append(spectrum)
            nested_scans = scan.get('scan',[])
            if not isinstance(nested_scans,list):
                nested_scans = [nested_scans]
            for nested_scan in nested_scans:
                ms_level, spectrum, struct_iter_ok, canary = read_mzxml_scan(nested_scan, index, filename_output, struct_iter_ok, canary, drop_ms1)
                index += 1
                output_ms2.append(spectrum)
    return output_ms1 + output_ms2
#######

def read_mzxml_scan(scan, index, filename_output, struct_iter_ok, canary, drop_ms1):
    ms_level = int(scan['@msLevel'])

    if drop_ms1 == True and ms_level == 1:
        return ms_level, None, struct_iter_ok, canary

    scan_number = int(scan['@num'])
    collision_energy = 0.0
    fragmentation_method = "NO_FRAG"

    try:
        collision_energy = float(scan['@collisionEnergy'])
    except KeyboardInterrupt:
        raise
    except:
        collision_energy = 0.0

    #Optional fields
    base_peak_intensity = 0.0
    base_peak_mz = 0.0
    base_peak_intensity = float(scan.get('@basePeakIntensity', 0.0))
    base_peak_mz = float(scan.get('@basePeakMz', 0.0))
    totIonCurrent = 0

    try:
        totIonCurrent = float(scan.get('@totIonCurrent', 0.0))
    except KeyboardInterrupt:
        raise
    except:
        fragmentation_method = "NO_FRAG"

    try:
        precursor_mz_tag = scan['precursorMz']
        precursor_mz = float(precursor_mz_tag['#text'])
        precursor_scan = int(precursor_mz_tag.get('@precursorScanNum', 0))
        precursor_charge = int(precursor_mz_tag.get('@precursorCharge', 0))
        precursor_intensity = float(precursor_mz_tag.get('@precursorIntensity', 0))

        try:
            fragmentation_method = precursor_mz_tag['@activationMethod']
        except KeyboardInterrupt:
            raise
        except:
            fragmentation_method = "NO_FRAG"

    except KeyboardInterrupt:
        raise
    except:
        if ms_level == 2:
            raise

    #Loading retention time
    retention_time = 0.0
    try:
        retention_time_string = scan['@retentionTime']
        #print(retention_time_string)
        retention_time = float(retention_time_string[2:-1])
    except KeyboardInterrupt:
        raise
    except:
        print("ERROR")
        retention_time = 0.0

    peaks_precision = float(scan['peaks'].get('@precision', '32'))
    peaks_compression = scan['peaks'].get('@compressionType', 'none')
    peak_string = scan['peaks'].get('#text', '')
    if canary and peak_string != '':
        try:
            decode_spectrum(peak_string, peaks_precision, peaks_compression, struct_iter_ok)
        except:
            struct_iter_ok = False
        canary = False
    if peak_string != '':
        peaks = decode_spectrum(peak_string, peaks_precision, peaks_compression, struct_iter_ok)
    else:
        peaks = []
    if ms_level == 1:
        output = Spectrum(
            filename_output,
            scan_number,
            index,
            peaks,
            0,
            0,
            ms_level
        )
    if ms_level == 2:
        output = Spectrum(
            filename_output,
            scan_number,
            index,
            peaks,
            precursor_mz,
            precursor_charge,
            ms_level,
            collision_energy=collision_energy,
            fragmentation_method=fragmentation_method,
            precursor_intensity=precursor_intensity,
            totIonCurrent=totIonCurrent
        )
        output.retention_time = retention_time
    return ms_level, output, struct_iter_ok, canary

def decode_spectrum(line, peaks_precision, peaks_compression, struct_iter_ok):

    """https://groups.google.com/forum/#!topic/spctools-discuss/qK_QThoEzeQ"""

    decoded = binascii.a2b_base64(line)
    number_of_peaks = 0
    unpack_format1 = ""


    if peaks_compression == "zlib":
        decoded = zlib.decompress(decoded)

    #Assuming no compression
    if peaks_precision == 32:
        number_of_peaks = len(decoded)/4
        unpack_format1 = ">%df" % number_of_peaks
    else:
        number_of_peaks = len(decoded)/8
        unpack_format1 = ">%dd" % number_of_peaks

    # peaks = []
    # if struct_iter_ok:
    #     peak_iter = struct.iter_unpack(unpack_format1,decoded)
    #     peaks = [
    #        pair for pair in zip(*[peak_iter] * 2)
    #     ]
    # else:
    peaks = [
       pair for pair in zip(*[iter(struct.unpack(unpack_format1,decoded))] * 2)
    ]
    return peaks
    # peaks_list = struct.unpack(unpack_format1,decoded)
    # return [
    #     (peaks_list[i*2],peaks_list[i*2+1])
    #     for i in range(0,int(len(peaks_list)/2))
    # ]

def window_filter_peaks(peaks, window_size, top_peaks):
    peak_list_window_map = defaultdict(list)
    for peak in peaks:
        mass = peak[0]
        mass_bucket = int(mass/window_size)
        peak_list_window_map[mass_bucket].append(peak)

    new_peaks = []
    for bucket in peak_list_window_map:
        peaks_sorted_by_intensity = sorted(peak_list_window_map[bucket], key=lambda peak: peak[1], reverse=True)
        peaks_to_keep = peaks_sorted_by_intensity[:top_peaks]
        new_peaks += peaks_to_keep

    new_peaks = sorted(new_peaks, key=lambda peak: peak[0])
    return new_peaks

def filter_precursor_peaks(peaks, tolerance_to_precursor, mz):
    new_peaks = []
    for peak in peaks:
        if abs(peak[0] - mz) > tolerance_to_precursor:
            new_peaks.append(peak)
    return new_peaks