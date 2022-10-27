// Ensure DSL2
nextflow.enable.dsl = 2

process SYNAPSE_GET {

    container "sagebionetworks/synapsepythonclient:v2.7.0"

    input:
    val params.syn_id

    output:
    tuple val(params.syn_id), path('*')

    script:
    // gets synapse file using cli
    """
    synapse get ${params.syn_id}

    shopt -s nullglob
    for f in *\\ *; do mv "\${f}" "\${f// /_}"; done
    """
}

workflow {
    SYNAPSE_GET(params.syn_id)
}