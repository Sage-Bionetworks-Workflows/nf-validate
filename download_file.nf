// Ensure DSL2
nextflow.enable.dsl = 2

process SYNAPSE_GET {

    container "sagebionetworks/synapsepythonclient:v2.7.0"

    input:
    val syn_id

    output:
    tuple val(syn_id), path('*')

    script:
    // gets synapse file using cli
    """
    synapse get ${syn_id}

    shopt -s nullglob
    for f in *\\ *; do mv "\${f}" "\${f// /_}"; done
    """
}

workflow {
    syn_ids = params.syn_ids.tokenize(',')
    ch_syn_ids = Channel.fromList(syn_ids)
    SYNAPSE_GET(ch_syn_ids)
}
