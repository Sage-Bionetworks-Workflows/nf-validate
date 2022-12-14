#!/usr/bin/env python3

import sys

from utils import json_dump, package_validation_dict


def file_extension_test(file_path: str) -> str:
    """
    1. Reads file extension from provided path
    2. Checks for valid file extension

    Args:
        file_path (str): Path to the downloaded file

    Returns:
        str: Result of File extension test
    """
    # TODO
    # hard-coded extension check for now, will introduce mapping when we have at least 2 file types to check
    file_ext_test = file_path.endswith(("ome.tiff", "ome.tif"))
    file_ext_status = "pass" if file_ext_test else "fail"
    return file_ext_status


if __name__ == "__main__":
    syn_id = sys.argv[1]
    entity_type = sys.argv[2]
    version_number = sys.argv[3]
    md5_input = sys.argv[4]
    file_path = sys.argv[5]
    file_ext_status = file_extension_test(file_path)
    file_extension_check_data = package_validation_dict(
        syn_id=syn_id,
        entity_type=entity_type,
        version_number=version_number,
        md5_input=md5_input,
        validation_status=file_ext_status,
        test_name="file_extension_test",
    )
    json_dump(syn_id, "file_extension_test", file_extension_check_data)
