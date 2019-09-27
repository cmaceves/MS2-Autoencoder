#!/usr/bin/env nextflow

params.inputSpectra = "./test_data/*.mzXML"

TOOL_FOLDER = "$baseDir/bin"

process extractPairs {

    input:
    set file_id, extension, file(inputFile) from Channel.fromPath( params.inputSpectra ).map { file -> tuple(file.baseName, file.extension, file) }

    // output:
    // file 'seq_*' into records

    """
    mkdir ${file_id}_outdir
    python $TOOL_FOLDER/main.py $inputFile ${file_id}_outdir
    """

}