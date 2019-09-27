test:
	python ./bin/main.py test_data/Cholesterol_130uM_GB1_01_6914.mzXML output_dir

test_workflow:
	nextflow run extract_data.nf -resume

test_cluster:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084286/ccms_peak/GNPS00001/*" -resume
