test:
	python ./bin/main.py test_data/Cholesterol_130uM_GB1_01_6914.mzXML output_dir

test_workflow:
	nextflow run extract_data.nf -resume

test_cluster:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084286/ccms_peak/GNPS00001/*" -resume

83825:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/**.mzML" -resume

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

mass_data:
#84287:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084287/ccms_peak/raw/**.mzML" -with-trace -resume
#84286:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084286/ccms_peak/GNPS00002/**.mzML" -with-trace -resume
#84237:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084237/peak/mzML/*" -with-trace -resume
#84118:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084118/ccms_peak/raw/**.mzML" -with-trace -resume
#84117:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084117/ccms_peak/mzxml/**.mzML" -with-trace -resume
#84102:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084102/ccms_peak/1907_Caps_Contaminant/**.mzML" -with-trace -resume
#84100:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084100/peak/mzML/**.mzML" -with-trace -resume
#84092:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084092/ccms_peak/**.mzML" -with-trace -resume
#84030:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084030/ccms_peak/*" -with-trace -resume
#84020:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084020/ccms_peak/data_raw/*/**.mzML" -with-trace -resume
#83835:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083835/ccms_peak/EtOAc_Pos_RAW/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083835/ccms_peak/MeOH_Pos_RAW/*" -with-trace -resume
#83825:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/Fecal/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/Plasma/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/Serum/*" -with-trace -resume
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/**.mzML" -with-trace -resume