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

process SYNAPSE_VALIDATE {

    container "python:3.10.4"

    input:
    tuple val(syn_id), path(path)

    output:
    tuple val(syn_id), path(path), stdout
    // tuple val(syn_id), path(path), emit: file
    // stdout emit: status

    script:
    // validates file
    """
    #!/usr/bin/env python3
    
    with open('${path}') as f:
        text = f.read()
    if text[-1] == '\\n':
        print(True)
    else:
        print(False)
    """
}

workflow {
    // pre-process inputs
    syn_ids = params.syn_ids.tokenize(',')
    ch_syn_ids = Channel.fromList(syn_ids)
    // download file(s)
    SYNAPSE_GET(ch_syn_ids)
    // validate file(s)
    SYNAPSE_VALIDATE(SYNAPSE_GET.output)

    SYNAPSE_VALIDATE.output.view()
}
