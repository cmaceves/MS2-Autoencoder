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

84072:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084072/ccms_peak/positive/**.mzML" -with-trace -resume

84492:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084492/peak/mzXML/*" -with-trace -resume

84479:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084479/peak/mzXML/*" -with-trace -resume

84289:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084289/peak/**.mzML" -with-trace -resume

84496:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084496/ccms_peak/raw/**.mzML" -with-trace -resume

84495:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084495/peak/mzXML/*" -with-trace -resume

84494:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084484/peak/mzXML/*" -with-trace -resume

84493:
	nextflow run extract_data.nf -c cluster.config --inputSpectra="/data/massive/MSV000084493/peak/mzXML/*" -with-trace -resume


