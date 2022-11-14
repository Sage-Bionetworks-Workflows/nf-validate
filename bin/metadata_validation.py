#!/usr/bin/env python3

import sys
import re

import json

import synapseclient


def get_synapse_file(syn_id: str) -> synapseclient.entity.File:
    """
    1. Validates provided Synapse ID against regex pattern
    2. Initializes synapseclient session and retrieves file metadata

    Args:
        syn_id (str): Synapse ID
    """
    pattern = re.compile("syn[0-9]+")
    if not pattern.search(syn_id):
        raise ValueError(f"{syn_id} is an invalid Synapse ID")

    syn = synapseclient.login()
    syn_file = syn.get(syn_id, downloadFile=False)
    return syn_file


def json_dump(syn_id: str, test_name: str, data: dict):
    """
    Dumps dictionary into json file

    Args:
        syn_id (str): Synapse ID
        test_name (str): Validation test that was performed
        data (dict): Formatted dictionary to be dumped into output JSON file
    """
    with open(f'{syn_id}-{test_name}.json', "w") as outfile:
        json.dump(data, outfile)


def execute_file_entity_test(syn_id: str, syn_file: synapseclient.entity.File, md5_checksum: str):
    """
    1. Creates file_entity_test dictionary for eventual json dump
    2. Checks synapse file for concreteType if FileEntity
    3. Calls json_dump to create json file with validation result and input metadata

    Args:
        syn_id (str): Synapse ID
        syn_file (synapseclient.entity.File): Synapse file entity
        md5_checksum (str): MD5 Checksum from input CSV file, to be carried on for Tier 1 Valiation step
    """
    # Perform the file entity test
    concrete_type = syn_file.get("concreteType", "")
    entity_type = concrete_type.split(".")[-1]  # Last part of concrete type
    file_entity_test = entity_type == "FileEntity"
    file_entity_status = "pass" if file_entity_test else "fail"
    # Prepare the test data for output
    file_entity_data = {
        "input": {
            "synapse_id": syn_id,
            "type": entity_type,
            "version_number": syn_file.properties.get("versionNumber"),
            "md5_checksum": md5_checksum,
        },
        "test": {
            "name": "file_entity_test", 
            "status": file_entity_status,
            "reason": None
        }
    }
    # Output the test data
    json_dump(syn_id, "file_entity_test", file_entity_data)


if __name__ == '__main__':
    syn_id = sys.argv[1]
    md5_checksum = sys.argv[2]
    syn_file = get_synapse_file(syn_id)
    execute_file_entity_test(syn_id, syn_file, md5_checksum)
