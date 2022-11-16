#!/usr/bin/env python3

import sys

from utils import json_dump, package_validation_dict

if __name__ == "__main__":
    syn_id = sys.argv[1]
    entity_type = sys.argv[2]
    version_number = sys.argv[3]
    md5_input = sys.argv[4]
    file_path = sys.argv[5]
    showinf_status = sys.argv[6]
    showinf_check_data = package_validation_dict(
        syn_id=syn_id,
        entity_type=entity_type,
        version_number=version_number,
        md5_input=md5_input,
        validation_status=showinf_status,
        test_name="bioformats_info_test",
    )
    json_dump(syn_id, "bioformats_info_test", showinf_check_data)
