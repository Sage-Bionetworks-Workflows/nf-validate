#!/usr/bin/env python3

import sys

from utils import json_dump, package_validation_dict

"""
This script should be used when the validation test is happening outside of a python script and the only remaining
steps for a validation process are:

1. Package up the validation result and metadat into a JSON-friendly format
2. Export the data into a JSON output file
"""

if __name__ == "__main__":
    syn_id = sys.argv[1]
    entity_type = sys.argv[2]
    version_number = sys.argv[3]
    md5_input = sys.argv[4]
    file_path = sys.argv[5]
    test_result = sys.argv[6]
    test_name = sys.argv[7]
    check_data = package_validation_dict(
        syn_id=syn_id,
        entity_type=entity_type,
        version_number=version_number,
        md5_input=md5_input,
        validation_status=test_result,
        test_name=test_name,
    )
    json_dump(syn_id, test_name, check_data)
