#!/usr/bin/env python3

import sys

from reusable import json_dump, package_validation_dict


def file_extension_test(file_path: str) -> str:
    """
    1. Reads file extension from provided path
    2. Checks for valid file extension (.txt is used for now, future version will use ome.tiff and ome.tif)
    3. Returns result of File extension test ("pass" or "fail")

    Args:
        file_path (str): Path to the downloaded file

    Returns:
        str: Result of File extension test
    """
    ext = file_path.split(".", 1)[-1]
    # Do we want the extension check to be hard-coded like this or check against the file type data provided in the CSV?
    # We are not using that column of the CSV at the moment.
    file_ext_test = (ext == "ome.tiff" or ext == "ome.tif") 
    file_ext_status = "pass" if file_ext_test else "fail"
    return file_ext_status


if __name__ == '__main__':
    syn_id = sys.argv[1]
    entity_type = sys.argv[2]
    version_number = sys.argv[3]
    md5_input = sys.argv[4]
    file_path = sys.argv[5]
    file_ext_status = file_extension_test(file_path)
    file_extension_check_data = package_validation_dict(
        syn_id,
        entity_type,
        version_number,
        md5_input,
        file_ext_status,
        "file_extension_test"
    )
    json_dump(syn_id, "file_extension_test", file_extension_check_data)
