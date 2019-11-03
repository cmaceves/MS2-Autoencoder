test:
	python ./bin/main.py test_data/Cholesterol_130uM_GB1_01_6914.mzXML output_dir

test_workflow:
	nextflow run extract_data.nf -resume

test_cluster:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084286/ccms_peak/GNPS00001/*" -resume

#83825:
	#nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/**.mzML" -resume

test_cluster_Chemicalstandards:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000078556/ccms_peak/Chemicalstandards/*" -with-trace -resume

82049:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000082049/ccms_peak/**.mzML" -with-trace -resume

84072:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084072/ccms_peak/positive/**.mzML" -with-trace -resume

84496:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084496/ccms_peak/raw/**.mzML" -with-trace -resume

84495:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084495/peak/mzXML/*" -with-trace -resume

84494:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084484/peak/mzXML/*" -with-trace -resume

84493:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084493/peak/mzXML/*" -with-trace -resume

84492:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084492/peak/mzXML/*" -with-trace -resume

84479:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084479/peak/mzXML/*" -with-trace -resume

84289:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084289/peak/**.mzML" -with-trace -resume


84287:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084287/ccms_peak/raw/**.mzML" -with-trace -resume

84286:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084286/ccms_peak/GNPS00002/**.mzML" -with-trace -resume


84237:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084237/peak/mzML/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084118/ccms_peak/raw/**.mzML" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084117/ccms_peak/mzxml/**.mzML" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084102/ccms_peak/1907_Caps_Contaminant/**.mzML" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084100/peak/mzML/**.mzML" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084092/ccms_peak/**.mzML" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084030/ccms_peak/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084020/ccms_peak/data_raw/*/**.mzML" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083835/ccms_peak/EtOAc_Pos_RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083835/ccms_peak/MeOH_Pos_RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/Fecal/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/Plasma/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/Serum/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/**.mzML" -with-trace -resume

83756:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083756/ccms_peak/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083605/ccms_peak/mzXML/*/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083541/ccms_peak/raw_files/all_raw_data/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083490/peak/1902_Abagyan_screening/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083475/ccms_peak/RAW/*/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083473/ccms_peak/RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083472/ccms_peak/RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083471/ccms_peak/1902_NIH_Synthesis_v2_UV_RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083470/ccms_peak/NIH_NaturalProducts_RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083469/ccms_peak/NIST1950SRM_RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083449/ccms_peak/NIH_synthesis_UV_raw/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083396/ccms_peak/*/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083395/ccms_peak/RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083388/ccms_peak/Positive Mode/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083387/ccms_peak/Raw/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083383/ccms_peak/*/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083320/ccms_peak/data/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083306/ccms_peak/*/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083300/ccms_peak/Data_raw/Positive/*/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083297/ccms_peak/RawData/*" -with-trace -resume
	