#!/usr/bin/env python3

import sys
import hashlib

from reusable import json_dump, package_validation_dict


def md5_checksum_test(file_path: str) -> str:
    """
    1. Opens the downloaded file and calculates MD5 Checksum from file contents
    2. Compares calculated MD5 Checksum to the one provided in the original input csv file
    3. Returns result of MD5 Checksum test ("pass" or "fail")

    Args:
        file_path (str): Path to the downloaded file

    Returns:
        str: Result of MD5 Checksum test
    """
    with open(file_path, "rb") as file_to_check:
        data = file_to_check.read()
        md5_generated = hashlib.md5(data).hexdigest()
    
    md5_test = md5_generated == md5_input
    md5_status = "pass" if md5_test else "fail"
    return md5_status


if __name__ == '__main__':
    syn_id = sys.argv[1]
    entity_type = sys.argv[2]
    version_number = sys.argv[3]
    md5_input = sys.argv[4]
    file_path = sys.argv[5]
    md5_status = md5_checksum_test(file_path)
    md5_check_data = package_validation_dict(
        syn_id,
        entity_type,
        version_number,
        md5_input,
        md5_status,
        "md5_checksum_test"
    )
    json_dump(syn_id, "md5_checksum_test", md5_check_data)
