#!/usr/bin/env python3

import os
import sys

import json

import synapseclient
from synapseclient import Entity


def get_synaspe_file(syn_id):
    """
    Initializes synapseclient session and retrieves file metadata
    """
    syn = synapseclient.Synapse()
    syn.login(authToken=os.environ["SYNAPSE_AUTH_TOKEN"])
    syn_file = syn.get(syn_id)
    return syn_file

def json_dump(syn_id, test, data):
    """
    Dumps dictionary into json file
    """
    with open(r'{0}-{1}.json'.format(syn_id, test), "w") as outfile:
        json.dump(data, outfile)

def execute_file_entity_test(syn_id, syn_file, md5_checksum):
    """
    1. Creates file_entity_test dictionary for eventual json dump
    2. Checks synapse file for concreteType if FileEntity
    3. Calls json_dump to create json file with validation result and input metadata
    """
    file_entity_test = {
        "input": {
            "synapse_id": syn_id,
            "type": syn_file.get("concreteType"),
            "version_number": syn_file.properties.get("versionNumber"),
            "md5_checksum": md5_checksum,
        },
        "test": {
            "name": "file_entity_test", 
            "status": "",
            "reason": None}
    }

    if syn_file.get("concreteType") == "org.sagebionetworks.repo.model.FileEntity":
        file_entity_test["test"]["status"] = "pass"
    else:
        file_entity_test["test"]["status"] = "fail"

    json_dump(syn_id, "file_entity_test", file_entity_test)


if __name__ == '__main__':
    syn_id = sys.argv[1]
    md5_checksum = sys.argv[2]
    syn_file = get_synaspe_file(syn_id)
    execute_file_entity_test(syn_id, syn_file, md5_checksum)
