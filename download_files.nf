// Ensure DSL2
nextflow.enable.dsl = 2
// Example ID array
// syn_ids = ["syn41864974","syn41864977"]
syn_ids = params.syn_ids.tokenize(',')
syn_id_channel = Channel.fromList(syn_ids)
// Uses Synapse CLI to download a file given the Synapse ID
process download_files {

    input:
    val syn_id

    output:
    // will eventually output synapse ids and locations to carry into
    // validation step

    script:
    // gets all synapse files from IDs provided, puts them in a directory
    // named by the synapse ID within the channel
    """
    synapse get --downloadLocation $syn_id $syn_id
    """
}

workflow {
    download_files(syn_id_channel)
}