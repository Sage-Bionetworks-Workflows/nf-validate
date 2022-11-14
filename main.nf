// Ensure DSL2
nextflow.enable.dsl = 2

//path to exmaple csv
params.csv_path = "data/input_ome.csv"

//checks metadata, and passes relavent fields along through .json
process SYNAPSE_CHECK {

    cache false
        
    container "python:3.10.4"
    
    secret 'SYNAPSE_AUTH_TOKEN'

    input:
    tuple val(syn_id), val(md5_checksum)

    output:
    tuple val(syn_id), val(md5_checksum), path('*.json')

    script:
    """
    metadata_validation.py '${syn_id}' '${md5_checksum}'
    """

}

//downloads synapse file given Synapse ID and version number
process SYNAPSE_GET {

    container "sagebionetworks/synapsepythonclient:v2.7.0"
    
    secret 'SYNAPSE_AUTH_TOKEN'

    input:
    tuple val(syn_id), val(type), val(version), val(md5_checksum)

    output:
    tuple val(syn_id), val(type), val(version), val(md5_checksum), path('*')

    script:
    """    
    synapse get ${syn_id} --version ${version}

    shopt -s nullglob
    for f in *\\ *; do mv "\${f}" "\${f// /_}"; done
    """
}

// calculates MD5 Checksum from contents of downloaded Synapse file and checks it against
// the one provided in the input CSV file
process MD5_VALIDATE {

    container "python:3.10.4"

    input:
    tuple val(syn_id), val(type), val(version), val(md5_checksum), path(path)
    
    output:
    tuple val(syn_id), val(type), val(version), val(md5_checksum), path(path)

    script:
    """
    md5_checksum.py '${syn_id}' '${type}' '${version}' '${md5_checksum}' '${path}'
    """

}

// checks if the downloaded Synaspe file extension is either 'ome.tiff' or 'ome.tif'
process FILE_EXT_VALIDATE {

    container "python:3.10.4"

    input:
    tuple val(syn_id), val(type), val(version), val(md5_checksum), path(path)
    
    output:
    tuple val(syn_id), val(type), val(version), val(md5_checksum), path(path)

    script:
    """
    file_extension.py '${syn_id}' '${type}' '${version}' '${md5_checksum}' '${path}'
    """

}


workflow {
    //Channel from csv rows
    Channel.fromPath(params.csv_path) \
    | splitCsv(header:true) \
    | map { row -> tuple(row.synapse_id, row.md5_checksum) } \
    // metadata validation
    | SYNAPSE_CHECK \
        // filter by files only from json
        | map { parseJson(it[2]) } \
        | map { it.input } \
        | filter { it.type == "FileEntity" } \
        // provides input for SYNAPSE_GET
        | map {tuple(it.synapse_id, it.type, it.version_number, it.md5_checksum)} \
        | SYNAPSE_GET \
        | MD5_VALIDATE \
        | FILE_EXT_VALIDATE
}

// Utility Functions

def parseJson(file) {
    def parser = new groovy.json.JsonSlurper()
    return parser.parseText(file.text)
}
