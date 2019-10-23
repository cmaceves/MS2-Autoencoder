test:
	python ./bin/main.py test_data/Cholesterol_130uM_GB1_01_6914.mzXML output_dir

test_workflow:
	nextflow run extract_data.nf -resume

test_cluster:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084286/ccms_peak/GNPS00001/*" -resume

test_cluster_MSV000083825:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000083825/ccms_peak/Positive/**.mzML" -resume

test_cluster_Chemicalstandards:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000078556/ccms_peak/Chemicalstandards/*" -with-trace -resume

test_cluster_MSV000082049:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000082049/ccms_peak/**.mzML" -with-trace -resume

test_cluster_MSV000084072:
	nextflow run extract_data.nf -c cluster.config --inputSpectra='/data/massive/MSV000084072/ccms_peak/positive/**.mzML -with-trace -resume
