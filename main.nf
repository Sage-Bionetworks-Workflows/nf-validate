// Ensure DSL2
nextflow.enable.dsl = 2

//path to exmaple csv
params.input = "${projectDir}/data/input_ome.csv"
//parents synapse folder for output csv file upload
params.parent_folder = "syn45704314"

//checks metadata, and passes relavent fields along through .json
process SYNAPSE_CHECK {

    cache false
        
    container "sagebionetworks/synapsepythonclient:v2.7.0"
    
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
    val(meta)

    output:
    tuple val(meta), path('*')

    script:
    """    
    synapse get ${meta.synapse_id} --version ${meta.version_number}
    shopt -s nullglob
    for f in *\\ *; do mv "\${f}" "\${f// /_}"; done
    """
}

// calculates MD5 Checksum from contents of downloaded Synapse file and checks it against
// the one provided in the input CSV file
process MD5_VALIDATE {

    container "python:3.10.4"

    input:
    tuple val(meta), path(path)
    
    output:
    tuple val(meta), path(path), path('*.json')

    script:
    """
    md5_checksum.py '${meta.synapse_id}' '${meta.type}' '${meta.version_number}' '${meta.md5_checksum}' '${path}'
    """

}

// checks if the downloaded Synapse file extension is either 'ome.tiff' or 'ome.tif'
process FILE_EXT_VALIDATE {

    container "python:3.10.4"

    input:
    tuple val(meta), path(path), path(prev_json)
    
    output:
    tuple val(meta), path(path), path('*.json')

    script:
    """
    file_extension.py '${meta.synapse_id}' '${meta.type}' '${meta.version_number}' '${meta.md5_checksum}' '${path}'
    """

}

// checks if Bio-Formats can inspect the file with showinf
process SHOWINF_VALIDATE {

    container "openmicroscopy/bftools:latest"

    input:
    tuple val(meta), path(path), path(prev_json)
    
    output:
    tuple val(meta), path(path), path('*.json')

    shell:
    '''
    export PATH="/opt/bftools:$PATH"
    
    if showinf -nopix -novalid -nocore !{path} ; then
        showinf_status="pass"
    else
        showinf_status="fail"
    fi
    package_validate.py '!{meta.synapse_id}' '!{meta.type}' '!{meta.version_number}' '!{meta.md5_checksum}' '!{path}' ${showinf_status} 'bioformats_info_test'
    '''

}

// checks for valid xml data
process XMLVALID_VALIDATE {

    container "openmicroscopy/bftools:latest"

    input:
    tuple val(meta), path(path), path(prev_json)
    
    output:
    tuple val(meta), path(path), path('*.json')

    shell:
    '''
    export PATH="/opt/bftools:$PATH"
    #check if xmlvalid can run, if so save string, if not create string that will result in failed test
    if xmlvalid !{path} ; then
        string="\$(xmlvalid !{path})"
    else
        string="command failed"
    fi
    #check string for substring which indicates successful test, create xmlvalid_status variable with result of test
    if [[ ${string} == *"No validation errors found."* ]] ; then
        xmlvalid_status="pass"
    else
        xmlvalid_status="fail"
    fi
    package_validate.py '!{meta.synapse_id}' '!{meta.type}' '!{meta.version_number}' '!{meta.md5_checksum}' '!{path}' ${xmlvalid_status} 'xmlvalid_test'
    ''' 

}

// aggregates output data and exports output csv
process CSV_OUTPUT {

    debug true

    container "python:3.10.4"

    input:
    tuple path(json_list), val(input)

    output:
    path("*.csv")

    script:
    """
    csv_output.py '${input}' *.json
    """
}

// uploads csv file to Synapse
process SYNAPSE_STORE {

  container "sagebionetworks/synapsepythonclient:v2.6.0"

  secret "SYNAPSE_AUTH_TOKEN"

  input:
  path(validation_results)

  script:
  """
  synapse store --parentId ${params.parent_folder} ${validation_results}
  """

}

workflow {
    //Channel from csv rows
    Channel.fromPath(params.input) \
    | splitCsv(header:true) \
    | map { row -> tuple(row.synapse_id, row.md5_checksum) } \
    // metadata validation
    | SYNAPSE_CHECK \
        // filter by files only from json
        | map { parseJson(it[2]) } \
        | map { it.input } \
        | filter { it.type == "FileEntity" } \
        | SYNAPSE_GET \
        | MD5_VALIDATE \
        | FILE_EXT_VALIDATE \
        | SHOWINF_VALIDATE \
        | XMLVALID_VALIDATE \
            | mix( SYNAPSE_CHECK.out, MD5_VALIDATE.out, FILE_EXT_VALIDATE.out, SHOWINF_VALIDATE.out ) \
            | map { it[2] } \
            | collect \
            | map { tuple(it, params.input) } \
            | CSV_OUTPUT
            | SYNAPSE_STORE

}

// Utility Functions

def parseJson(file) {
    def parser = new groovy.json.JsonSlurper()
    return parser.parseText(file.text)
}
