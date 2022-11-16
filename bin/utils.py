import json


def package_validation_dict(
    syn_id: str,
    entity_type: str,
    version_number: int,
    md5_input: str,
    validation_status: str,
    test_name: str,
) -> dict:
    """
    Packages data into JSON-friendly dictionary for creation of validation output file

    Args:
        syn_id (str): Synapse ID
        entity_type (str): Entity type of Synapse file
        version_number (int): Version number of Synapse file
        md5_input (str): MD5 Checksum originally supplied to the input csv file

    Returns:
        data (dict): JSON-friendly dictionary ready for writing to validation output
    """
    data = {
        "input": {
            "synapse_id": syn_id,
            "type": entity_type,
            "version_number": version_number,
            "md5_checksum": md5_input,
        },
        "test": {"name": test_name, "status": validation_status, "reason": None},
    }
    return data


def json_dump(syn_id: str, test_name: str, data: dict):
    """
    Dumps dictionary into JSON output file

    Args:
        syn_id (str): Synapse ID
        test_name (str): Validation test that was performed
        data (dict): Formatted dictionary to be dumped into output JSON file
    """
    with open(f"{syn_id}-{test_name}.json", "w") as outfile:
        json.dump(data, outfile)
