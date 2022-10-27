// Ensure DSL2
nextflow.enable.dsl = 2

process download_file {

    input:
    val params.syn_id

    output:
    // will eventually output synapse ids and locations to carry into
    // validation step

    script:
    // gets synapse file using cli
    """
    synapse get $params.syn_id
    """
}

workflow {
    download_file(params.syn_id)
}